# Лабораторная работа №1 — Вариант 9 (Сезонность спроса)

В этой работе я решаю задачу сезонности спроса: загружаю исторические продажи в HDFS, выполняю ETL и аналитику в PySpark/Spark SQL, затем строю график сезонности по годам.

## Источник данных
Walmart Store Sales Forecasting (Kaggle):  
[https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data)

Файл для анализа: `train.csv`.

## Структура проекта
- `lab_01.py` — основной скрипт (ETL + Spark SQL + визуализация).
- `Report.md` — оформленный отчет по лабораторной (от моего имени).
- `CHECKLIST_СКРИНЫ.md` — пошаговый чек-лист, где именно делать скриншоты.
- `commands_for_screens.sh` — сценарий запуска с сохранением логов в `raw/`.
- `raw/` — текстовые доказательства выполнения команд.
- `screens/` — скриншоты выполнения.
- `results/` — итоговые графики.

Важно: в `screens/` и `raw/` могут лежать предыдущие примеры артефактов. Перед сдачей я перезаписываю их своими актуальными скриншотами и логами текущего запуска.

## Подготовка
1. Скопировал датасет в VM: `/home/hadoop/Downloads/data/train.csv`.
2. Перешел в папку лабораторной:
```bash
cd "/Users/robertvardanyan/Documents/Playground/апрель анализ данных, лаб 1"
```

## Запуск вручную (рекомендуется для скриншотов)
1. Запуск Hadoop/YARN:
```bash
sudo su - hadoop
start-dfs.sh
start-yarn.sh
jps
```

2. Загрузка данных в HDFS:
```bash
hdfs dfs -mkdir -p /user/hadoop/lab_01/input
hdfs dfs -chmod 775 /user/hadoop/lab_01
hdfs dfs -put -f /home/hadoop/Downloads/data/train.csv /user/hadoop/lab_01/input/
hdfs dfs -ls /user/hadoop/lab_01/input/
```

3. Запуск анализа:
```bash
cd "/Users/robertvardanyan/Documents/Playground/апрель анализ данных, лаб 1"
python3 lab_01.py
```

4. Проверка результатов в HDFS:
```bash
hdfs dfs -ls /user/hadoop/lab_01/output/
hdfs dfs -ls /user/hadoop/lab_01/output/monthly_total/
hdfs dfs -ls /user/hadoop/lab_01/output/seasonal_coefficients/
```

5. Остановка служб:
```bash
stop-yarn.sh
stop-dfs.sh
```

## Быстрый запуск с логами
```bash
cd "/Users/robertvardanyan/Documents/Playground/апрель анализ данных, лаб 1"
chmod +x commands_for_screens.sh
./commands_for_screens.sh
```

## Ожидаемый результат
- Определены месяцы с пиковым спросом.
- Рассчитаны сезонные коэффициенты по категориям (`Dept`).
- Построен график сезонности: `results/09_seasonality_by_year.png`.
- В ETL выполнены: обработка NULL, типизация полей и удаление дубликатов.
