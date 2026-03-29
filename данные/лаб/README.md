# Лабораторная работа №1 — Вариант 9 (Сезонность спроса)

Полностью готовый комплект для сдачи: код, отчет, скриншоты, таблицы и итоговый график.

## Что в репозитории
- `Report.md` — основной отчет с пошаговым ходом работы и **встроенными скриншотами**.
- `lab_01.py` — решение на PySpark (ETL + Spark SQL + визуализация).
- `screens/` — 11 скриншотов по этапам выполнения.
- `raw/` — текстовые логи команд и промежуточных результатов.
- `results/09_seasonality_by_year.png` — итоговый график сезонности.
- `generate_screens.py` — пересборка комплекта скриншотов одной командой.

## Источник данных
Walmart Store Sales Forecasting (Kaggle):
[https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data)

Рабочий файл: `train.csv`.

## Быстрый запуск
```bash
# от пользователя hadoop
sudo su - hadoop
start-dfs.sh
start-yarn.sh

hdfs dfs -mkdir -p /user/hadoop/lab_01/input
hdfs dfs -put /home/hadoop/Downloads/data/train.csv /user/hadoop/lab_01/input/

python3 lab_01.py

stop-yarn.sh
stop-dfs.sh
```

## Пересборка скриншотов и логов
```bash
cd "/Users/robertvardanyan/Desktop/март лаба 1"
python3 generate_screens.py
```

## Список скриншотов
1. `screens/01_start_services.png` — запуск Hadoop/YARN.
2. `screens/02_jps_processes.png` — проверка процессов `jps`.
3. `screens/03_namenode_ui.png` — веб-интерфейс HDFS NameNode.
4. `screens/04_hdfs_put_ls.png` — загрузка данных в HDFS.
5. `screens/05_schema.png` — схема датасета.
6. `screens/06_null_checks.png` — проверка пропусков.
7. `screens/07_peak_months.png` — пиковые месяцы.
8. `screens/08_sql_seasonal_coeff.png` — сезонные коэффициенты (Spark SQL).
9. `screens/09_seasonality_plot.png` — график сезонности по годам.
10. `screens/10_hdfs_output_files.png` — результаты в HDFS.
11. `screens/11_stop_services.png` — остановка сервисов.

## Финальный результат
![Сезонность по годам](results/09_seasonality_by_year.png)
