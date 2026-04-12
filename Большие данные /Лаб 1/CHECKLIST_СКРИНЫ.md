# Чек-лист скриншотов (делал по ходу выполнения)

Ниже фиксирую, какие скриншоты прикладываю как подтверждение реальной работы.

1. `01_start_services.png`  
Команды `start-dfs.sh` и `start-yarn.sh` в терминале под пользователем `hadoop`.

2. `02_jps_processes.png`  
Результат `jps` (видно `NameNode`, `DataNode`, `ResourceManager`, `NodeManager`).

3. `03_namenode_ui.png`  
Web UI NameNode: `http://localhost:9870`.

4. `04_hdfs_put_ls.png`  
Загрузка `train.csv` в HDFS и вывод `hdfs dfs -ls /user/hadoop/lab_01/input/`.

5. `05_schema.png`  
Вывод `printSchema()` из `lab_01.py`.

6. `06_null_checks.png`  
Проверка пропусков до и после очистки.

7. `07_peak_months.png`  
Результат таблицы пиковых месяцев (`peak_months.show(...)`).

8. `08_sql_seasonal_coeff.png`  
Результат Spark SQL с сезонными коэффициентами.

9. `09_seasonality_plot.png`  
Итоговый график сезонности по годам (`results/09_seasonality_by_year.png`).

10. `10_hdfs_output_files.png`  
Список выходных файлов в `/user/hadoop/lab_01/output/`.

11. `11_stop_services.png`  
Остановка `stop-yarn.sh` и `stop-dfs.sh`.

## Где храню
- Скриншоты: `screens/`
- Текстовые логи команд: `raw/`

## Формат
PNG, ширина 1400-1920 px, чтобы текст в терминале читался.
