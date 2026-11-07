"""Variant 8. UCI mathematics; one row is one student in this course."""
import csv
import hashlib
import io
import json
import logging
from pathlib import Path
import urllib.request
import zipfile
from datetime import datetime, timedelta
from psycopg2.extras import execute_values, RealDictCursor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag, task

ROOT = Path('/opt/airflow/dags')
DATA = ROOT / 'data'
URL = 'https://archive.ics.uci.edu/static/public/320/student%2Bperformance.zip'
CONNECTION_ID = 'analytics_postgres'

def database_connection():
    return PostgresHook(postgres_conn_id=CONNECTION_ID).get_conn()

def source_rows():
    return list(csv.DictReader(io.StringIO((DATA/'student-mat.csv').read_text()), delimiter=';'))

@dag(dag_id='student_performance_variant_08', start_date=datetime(2024,1,1),
     schedule=None, catchup=False, max_active_runs=1, default_args={'retries':2,'retry_delay':timedelta(seconds=30)},
     tags=['variant_08','UCI'])
def pipeline():
    @task
    def extract():
        DATA.mkdir(exist_ok=True)
        with urllib.request.urlopen(URL, timeout=120) as response:
            payload=response.read()
        (DATA/'source.zip').write_bytes(payload)
        with zipfile.ZipFile(io.BytesIO(payload)) as outer:
            if 'student-mat.csv' in outer.namelist():
                content=outer.read('student-mat.csv')
            else:
                with zipfile.ZipFile(io.BytesIO(outer.read('student.zip'))) as inner:
                    content=inner.read('student-mat.csv')
        (DATA/'student-mat.csv').write_bytes(content)
        logging.info('Source SHA256=%s',hashlib.sha256(payload).hexdigest())
        return len(source_rows())

    @task
    def load_raw(expected):
        ok, message = PostgresHook(postgres_conn_id=CONNECTION_ID).test_connection()
        logging.info('Connection Test %s: %s', CONNECTION_ID, message)
        if not ok:
            raise ConnectionError(message)
        rows=source_rows()
        if not rows or len(rows)!=expected: raise ValueError('Unexpected row count')
        fields=list(rows[0])
        # Source column names are fixed by this published dataset, all values stay TEXT.
        cols=', '.join('"'+f+'" TEXT' for f in fields)
        with database_connection() as conn, conn.cursor() as cur:
            cur.execute('DROP VIEW IF EXISTS student_datamart; DROP TABLE IF EXISTS stg_students; DROP TABLE IF EXISTS raw_students;')
            cur.execute('CREATE TABLE raw_students (row_id INTEGER PRIMARY KEY, '+cols+')')
            execute_values(cur,'INSERT INTO raw_students VALUES %s',[(i,*r.values()) for i,r in enumerate(rows,1)])
        return expected

    @task
    def transform(expected):
        valid=[]; rejected=[]
        with database_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT row_id, school, studytime, absences, "Medu", "Fedu", "G3" FROM raw_students ORDER BY row_id')
            raw_rows = cur.fetchall()
        if len(raw_rows) != expected:
            raise ValueError('RAW row count differs from extract')
        for r in raw_rows:
            i = r['row_id']
            try:
                vals=[int(r[k]) for k in ['studytime','absences','Medu','Fedu','G3']]
                st,ab,me,fe,g=vals
                if not (1<=st<=4 and 0<=ab<=93 and 0<=me<=4 and 0<=fe<=4 and 0<=g<=20):
                    raise ValueError('Outside documented range')
                valid.append((i,r['school'].strip(),*vals))
            except (ValueError,KeyError) as error:
                rejected.append((i,str(error)))
        with database_connection() as conn, conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS stg_students CASCADE')
            cur.execute('CREATE TABLE stg_students (row_id INTEGER PRIMARY KEY REFERENCES raw_students(row_id), school TEXT, studytime INTEGER, absences INTEGER, medu INTEGER, fedu INTEGER, g3 INTEGER)')
            cur.execute('CREATE TABLE IF NOT EXISTS etl_audit (loaded_at TIMESTAMPTZ DEFAULT now(), source_count INTEGER, accepted_count INTEGER, rejected_count INTEGER, rejected_rows JSONB)')
            if valid: execute_values(cur,'INSERT INTO stg_students VALUES %s',valid)
            cur.execute('INSERT INTO etl_audit(source_count,accepted_count,rejected_count,rejected_rows) VALUES (%s,%s,%s,%s)',(expected,len(valid),len(rejected),json.dumps(rejected)))
        logging.info('RAW=%s STG=%s rejected=%s reasons=%s',expected,len(valid),len(rejected),rejected)
        if len(valid)+len(rejected)!=expected or not valid: raise ValueError('Row reconciliation failed')
        return len(valid)

    @task
    def create_datamart(count):
        with database_connection() as conn, conn.cursor() as cur:
            cur.execute((ROOT/'datamart_variant_08.sql').read_text())
            cur.execute('SELECT count(*), avg(final_grade), avg(absences) FROM student_datamart')
            result=cur.fetchone()
            if result[0]!=count: raise ValueError('View reconciliation failed')
            logging.info('Datamart count, grade, absences: %s',result)
    create_datamart(transform(load_raw(extract())))
pipeline()
