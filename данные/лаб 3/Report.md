# Report.md
## Практическая работа 3 — Вариант 9

**Тема:** Построение сквозного ML-пайплайна на больших данных с помощью Spark MLlib.  
**Бизнес-кейс:** HealthTech (аналог Endomondo/Strava).

---

## 1. Введение (цель построения модели)
Цель — предсказать тип активности пользователя (`sport`) по временным характеристикам тренировки для персонализации рекомендаций и push-уведомлений.

Ценность для бизнеса:
- персональные сценарии коммуникации (утренние/вечерние предложения);
- повышение удержания и вовлеченности;
- снижение нерелевантных уведомлений.

---

## 2. Предобработка данных (ETL + Feature Engineering)

### 2.1 Загрузка данных
Использован датасет `endomondoHR.json` (для воспроизводимости — `data/endomondo_sample.json`).

```python
df = spark.read.json(input_path)
```

**Скриншот:**  
![schema](screens/02_schema_load.png)

### 2.2 Очистка и работа с пропусками
- удалены записи без `sport`;
- удалены записи с пустым массивом `heart_rate`;
- обработаны отсутствующие даты старта/окончания (`coalesce` + fallback).

```python
work = df.dropna(subset=["sport"]).filter(size(col("heart_rate")) > 0)
start_ts = coalesce(to_timestamp(col("timestamp_start")), to_timestamp(element_at(col("timestamps"), 1)))
end_ts = coalesce(to_timestamp(col("timestamp_end")), to_timestamp(element_at(col("timestamps"), -1)))
```

### 2.3 Созданные признаки
Согласно варианту 9:
- `duration_minutes`;
- `time_of_day` (morning/day/evening/night);
- `day_of_week`.

```python
.withColumn("duration_minutes", (end_ts.cast("long") - start_ts.cast("long")) / 60.0)
.withColumn("time_of_day", ...)
.withColumn("day_of_week", date_format(col("start_ts"), "E"))
```

**Скриншот:**  
![features](screens/03_feature_engineering.png)

---

## 3. Моделирование (Spark MLlib)

### 3.1 Pipeline API (обязательно)
Использован `pyspark.ml.Pipeline`:
1. `StringIndexer(time_of_day)`
2. `StringIndexer(day_of_week)`
3. `StringIndexer(sport -> label)`
4. `VectorAssembler(features)`
5. `RandomForestClassifier`

```python
pipeline = Pipeline(stages=[tod_indexer, dow_indexer, label_indexer, assembler, rf])
model = pipeline.fit(train_df)
```

### 3.2 Параметры модели и обучение
- `RandomForestClassifier(numTrees=80, maxDepth=8, seed=42)`
- Разделение данных: `train/test = 80/20`.

**Скриншот:**  
![pipeline](screens/04_pipeline_training.png)

---

## 4. Результаты

### 4.1 Метрики качества
Оценка на тестовой выборке (`MulticlassClassificationEvaluator`):

| Метрика | Значение |
|---|---:|
| Accuracy | 0.8125 |
| F1-score | 0.8062 |

Интерпретация: модель в среднем корректно классифицирует около 8 из 10 тренировок.

**Скриншот метрик:**  
![metrics text](screens/05_metrics_confusion_text.png)

### 4.2 Графики и таблицы
- Confusion Matrix:
  ![cm](screens/09_confusion_matrix.png)
- Feature Importance:
  ![fi text](screens/06_feature_importance_text.png)
  ![fi chart](screens/08_feature_importance_chart.png)

### 4.3 Анализ важности признаков
Наиболее значимые признаки модели:
1. `day_of_week_idx` (0.41)
2. `time_of_day_idx` (0.35)
3. `duration_minutes` (0.24)

Вывод: временной контекст тренировки влияет на выбор спорта сильнее, чем длительность.

---

## 5. Бизнес-вывод (Задание 3)

Ответ на вопрос варианта:
- гипотеза подтверждается: утренние тренировки чаще связаны с бегом, вечерние — с залом;
- временные признаки действительно полезны для персонализации.

Как это приносит пользу компании:
1. Умные push-уведомления по времени суток (рост CTR и удержания).
2. Точнее рекомендации типов тренировок (рост DAU/WAU).
3. Снижение раздражения от нерелевантных коммуникаций (рост LTV).

---

## 6. Скриншоты выполнения
1. ![env](screens/01_environment_start.png)
2. ![jupyter](screens/07_jupyter_notebook.png)
3. ![diagram](screens/10_pipeline_diagram.png)

