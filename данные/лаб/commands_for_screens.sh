#!/usr/bin/env bash
set -euo pipefail

# Скрипт-памятка для получения выводов под скриншоты.
# Запускать от пользователя hadoop.

mkdir -p raw

{
  echo '== START DFS/YARN =='
  date
  start-dfs.sh
  start-yarn.sh
} > raw/01_start_services.txt 2>&1

jps > raw/02_jps_processes.txt 2>&1

{
  hdfs dfs -mkdir -p /user/hadoop/lab_01/input
  hdfs dfs -chmod 775 /user/hadoop/lab_01
  hdfs dfs -put -f /home/hadoop/Downloads/data/train.csv /user/hadoop/lab_01/input/
  hdfs dfs -ls /user/hadoop/lab_01/input/
} > raw/04_hdfs_put_ls.txt 2>&1

python3 lab_01.py > raw/05_08_pyspark_run.txt 2>&1

{
  hdfs dfs -ls /user/hadoop/lab_01/output/
  hdfs dfs -ls /user/hadoop/lab_01/output/monthly_total/
  hdfs dfs -ls /user/hadoop/lab_01/output/seasonal_coefficients/
} > raw/10_hdfs_output_files.txt 2>&1

{
  stop-yarn.sh
  stop-dfs.sh
} > raw/11_stop_services.txt 2>&1

echo "Готово. Текстовые логи сохранены в папку raw/."
