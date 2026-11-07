"""Run after a successful DAG: docker compose exec superset python /app/lab/bootstrap_dashboard.py"""
import json
from superset.app import create_app
app=create_app()
with app.app_context():
 from superset import db
 from superset.models.core import Database
 from superset.connectors.sqla.models import SqlaTable
 from superset.models.slice import Slice
 from superset.models.dashboard import Dashboard
 from flask_appbuilder.security.sqla.models import User
 database=db.session.query(Database).filter_by(database_name='Student Analytics').first()
 if not database:
  database=Database(database_name='Student Analytics',sqlalchemy_uri='postgresql+psycopg2://analytics:analytics@analytics_postgres:5432/analytics')
  db.session.add(database); db.session.commit()
 dataset=db.session.query(SqlaTable).filter_by(table_name='student_datamart',database_id=database.id).first()
 if not dataset:
  dataset=SqlaTable(table_name='student_datamart',schema='public',database=database)
  db.session.add(dataset); db.session.commit(); dataset.fetch_metadata(); db.session.commit()
 owner=db.session.query(User).filter_by(username='admin').one()
 def metric(col,agg='AVG'):
  return {'expressionType':'SIMPLE','column':{'column_name':col},'aggregate':agg,'label':f'{agg}({col})','optionName':f'{agg}_{col}'}
 grade=metric('final_grade'); absent=metric('absences')
 common={'datasource':f'{dataset.id}__table','adhoc_filters':[],'row_limit':10000,'time_range':'No filter'}
 specs=[
 ('Mean final grade (0–20)','big_number_total',{'metric':grade,'subheader':'Mathematics · UCI','y_axis_format':'.2f'}),
 ('Final grade by weekly study time','echarts_timeseries_bar',{'x_axis':'study_time_group','metrics':[grade],'groupby':[],'x_axis_sort_asc':True,'x_axis_title':'Weekly study time','y_axis_title':'Mean grade (0–20)'}),
 ('Highest parental education','pie',{'groupby':['parent_education_level'],'metric':{'expressionType':'SQL','sqlExpression':'COUNT(*)','label':'Students','optionName':'count_students'},'show_labels':True,'show_legend':True,'label_type':'key_percent'}),
 ('Grades and absences by study time','mixed_timeseries',{'x_axis':'study_time_group','metrics':[grade],'metrics_b':[absent],'groupby':[],'groupby_b':[],'adhoc_filters_b':[],'seriesType':'bar','seriesTypeB':'line','y_axis_title':'Mean grade (0–20)','y_axis_title_secondary':'Mean absences','yAxisIndex':0,'yAxisIndexB':1,'show_legend':True,'x_axis_sort_asc':True}),
 ('Final grade by number of absences','echarts_timeseries_line',{'x_axis':'absences','metrics':[grade],'groupby':[],'x_axis_sort_asc':True,'x_axis_title':'Absences','y_axis_title':'Mean grade (0–20)','markerEnabled':True})]
 charts=[]
 for title,viz,params in specs:
  chart=db.session.query(Slice).filter_by(slice_name=title).first()
  if not chart: chart=Slice(slice_name=title, datasource_type='table', datasource_id=dataset.id, viz_type=viz); db.session.add(chart)
  chart.viz_type=viz; chart.datasource_id=dataset.id; chart.datasource_type='table'; chart.params=json.dumps(dict(common,viz_type=viz,**params)); chart.owners=[owner]
  db.session.commit(); charts.append(chart)
 dash=db.session.query(Dashboard).filter_by(slug='student-performance-08').first()
 if not dash: dash=Dashboard(dashboard_title='Variant 8 · Student Performance',slug='student-performance-08'); db.session.add(dash)
 dash.slices=charts; dash.owners=[owner]; dash.published=True
 pos={'DASHBOARD_VERSION_KEY':'v2','ROOT_ID':{'id':'ROOT_ID','type':'ROOT','children':['GRID_ID']},'GRID_ID':{'id':'GRID_ID','type':'GRID','children':['ROW-0','ROW-1','ROW-2'],'parents':['ROOT_ID']}}
 for n,indices in enumerate([[0],[1,2],[3,4]]):
  rid=f'ROW-{n}'; pos[rid]={'id':rid,'type':'ROW','children':[],'parents':['ROOT_ID','GRID_ID'],'meta':{'background':'BACKGROUND_TRANSPARENT'}}
  for i in indices:
   cid=f'CHART-{charts[i].id}'; pos[rid]['children'].append(cid)
   pos[cid]={'id':cid,'type':'CHART','children':[],'parents':['ROOT_ID','GRID_ID',rid],'meta':{'chartId':charts[i].id,'width':12 if n==0 else 6,'height':22 if n==0 else 45,'sliceName':charts[i].slice_name}}
 dash.position_json=json.dumps(pos)
 filters=[]
 for name,column in [('School','school'),('Weekly study time','study_time_group')]:
  filters.append({'id':'NATIVE_FILTER-'+column,'name':name,'filterType':'filter_select','targets':[{'datasetId':dataset.id,'column':{'name':column}}],'defaultDataMask':{'extraFormData':{},'filterState':{},'ownState':{}},'controlValues':{'enableEmptyFilter':False,'multiSelect':True,'searchAllOptions':False,'inverseSelection':False},'cascadeParentIds':[],'scope':{'rootPath':['ROOT_ID'],'excluded':[]},'type':'NATIVE_FILTER'})
 dash.json_metadata=json.dumps({'native_filter_configuration':filters,'color_scheme':'supersetColors'})
 db.session.commit()
 print('Dashboard: /superset/dashboard/student-performance-08/')
