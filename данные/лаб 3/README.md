# Практическая работа 3 — Spark MLlib Pipeline

## Вариант
**Вариант 9**: предсказание типа активности `sport` по временным признакам тренировки.

## Постановка задачи
Построить сквозной ML-пайплайн в `pyspark.ml` для бизнес-кейса HealthTech:
- подготовить данные из `endomondoHR.json`;
- сделать feature engineering (`time_of_day`, `day_of_week`, `duration_minutes`);
- обучить модель `RandomForestClassifier`;
- оценить качество и объяснить бизнес-ценность.

## Состав репозитория
- `lab_03_ml.ipynb` — основной ноутбук (Setup -> ETL -> Features -> ML -> Eval).
- `lab_03_variant_09.py` — эквивалентный скрипт запуска пайплайна.
- `Report.md` — отчет по работе.
- `data/endomondo_sample.json` — sample-данные для воспроизводимого запуска.
- `scripts/generate_endomondo_sample.py` — генерация sample-датасета.
- `screens/`, `raw/`, `results/` — скриншоты, логи и графики.

## Окружение и запуск
### Вариант 1 (рекомендуется): образ `ds_mgpu_Hadoop3+spark_3_4`
- Spark 3.4.x
- Python 3.10+
- JupyterLab

### Вариант 2: Docker-окружение из курса
```bash
git clone https://github.com/BosenkoTM/PySpark.git
cd PySpark
sudo docker compose up -d
# Jupyter: http://localhost:10000/lab
```

### Библиотеки
- `pyspark==3.4.3`
- `Pillow>=10.0` (для генерации изображений в отчете)

Установка:
```bash
pip install -r requirements.txt
```

## Источник данных
- Основной датасет: `endomondoHR.json` (материалы курса).
- Репозиторий курса/зеркало: [https://github.com/BosenkoTM/PySpark](https://github.com/BosenkoTM/PySpark)

## Быстрый запуск решения
```bash
python3 scripts/generate_endomondo_sample.py
python3 lab_03_variant_09.py
```

## Пересборка скриншотов и графиков отчета
```bash
python3 generate_lab3_assets.py
```
