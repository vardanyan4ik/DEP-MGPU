from pathlib import Path
from typing import List

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    coalesce,
    col,
    date_format,
    element_at,
    hour,
    lit,
    size,
    to_timestamp,
    when,
)


DEFAULT_INPUTS = [
    "data/endomondoHR.json",
    "data/endomondo_sample.json",
]


def build_spark() -> SparkSession:
    spark = SparkSession.builder.appName("Lab3_Variant9_Endomondo_RF").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def resolve_input_path(candidates: List[str]) -> str:
    for c in candidates:
        if Path(c).exists():
            return c
    raise FileNotFoundError(f"Input dataset not found. Checked: {candidates}")


def prepare_features(df: DataFrame) -> DataFrame:
    # Базовая очистка: спортивная категория и массив пульса должны быть валидными
    work = df.dropna(subset=["sport"]).filter(size(col("heart_rate")) > 0)

    # Источник времени: timestamp_start/timestamp_end (если есть) или timestamps[]
    start_ts = coalesce(
        to_timestamp(col("timestamp_start")),
        to_timestamp(element_at(col("timestamps"), 1)),
    )
    end_ts = coalesce(
        to_timestamp(col("timestamp_end")),
        to_timestamp(element_at(col("timestamps"), -1)),
    )

    duration_minutes = (
        (end_ts.cast("long") - start_ts.cast("long")) / lit(60.0)
    )

    work = (
        work.withColumn("start_ts", start_ts)
        .withColumn(
            "duration_minutes",
            when(duration_minutes > 0, duration_minutes).otherwise(size(col("heart_rate")).cast("double")),
        )
        .withColumn("start_hour", hour(col("start_ts")))
        .withColumn(
            "time_of_day",
            when(col("start_hour").between(5, 11), lit("morning"))
            .when(col("start_hour").between(12, 16), lit("day"))
            .when(col("start_hour").between(17, 22), lit("evening"))
            .otherwise(lit("night")),
        )
        .withColumn("day_of_week", coalesce(date_format(col("start_ts"), "E"), lit("unknown")))
    )

    # Сужаем задачу до наиболее популярных видов активности
    top_sports = [
        r["sport"]
        for r in work.groupBy("sport").count().orderBy(col("count").desc()).limit(4).collect()
    ]

    prepared = (
        work.filter(col("sport").isin(top_sports))
        .dropna(subset=["time_of_day", "day_of_week", "duration_minutes"])
        .filter(col("duration_minutes") > 0)
    )

    return prepared


def main() -> None:
    spark = build_spark()
    input_path = resolve_input_path(DEFAULT_INPUTS)

    print(f"Using input: {input_path}")
    df = spark.read.json(input_path)

    print("\n=== Schema ===")
    df.printSchema()

    prepared = prepare_features(df)

    print("\n=== Prepared sample ===")
    prepared.select("sport", "time_of_day", "day_of_week", "duration_minutes").show(10, truncate=False)

    # Индексация категорий
    tod_indexer = StringIndexer(
        inputCol="time_of_day", outputCol="time_of_day_idx", handleInvalid="keep"
    )
    dow_indexer = StringIndexer(
        inputCol="day_of_week", outputCol="day_of_week_idx", handleInvalid="keep"
    )
    label_indexer = StringIndexer(inputCol="sport", outputCol="label", handleInvalid="skip")

    assembler = VectorAssembler(
        inputCols=["time_of_day_idx", "day_of_week_idx", "duration_minutes"],
        outputCol="features",
    )

    rf = RandomForestClassifier(
        labelCol="label",
        featuresCol="features",
        numTrees=80,
        maxDepth=8,
        seed=42,
    )

    pipeline = Pipeline(stages=[tod_indexer, dow_indexer, label_indexer, assembler, rf])

    train_df, test_df = prepared.randomSplit([0.8, 0.2], seed=42)

    model = pipeline.fit(train_df)
    predictions = model.transform(test_df)

    acc_eval = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy"
    )
    f1_eval = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="f1"
    )

    accuracy = acc_eval.evaluate(predictions)
    f1_score = f1_eval.evaluate(predictions)

    print("\n=== Metrics ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-score: {f1_score:.4f}")

    print("\n=== Confusion Matrix (label -> prediction) ===")
    confusion = (
        predictions.groupBy("label", "prediction")
        .count()
        .orderBy(col("label"), col("prediction"))
    )
    confusion.show(truncate=False)

    # Feature importance
    rf_model = model.stages[-1]
    feature_names = ["time_of_day_idx", "day_of_week_idx", "duration_minutes"]
    values = list(rf_model.featureImportances.toArray())

    importance_rows = sorted(zip(feature_names, values), key=lambda x: x[1], reverse=True)

    print("\n=== Feature Importances ===")
    for name, score in importance_rows:
        print(f"{name}: {score:.4f}")

    # Артефакты
    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)

    confusion.coalesce(1).write.mode("overwrite").option("header", "true").csv(
        str(out_dir / "confusion_matrix_csv")
    )

    (out_dir / "metrics.txt").write_text(
        f"input={input_path}\naccuracy={accuracy:.6f}\nf1={f1_score:.6f}\n", encoding="utf-8"
    )

    (out_dir / "feature_importance.txt").write_text(
        "\n".join([f"{n},{v:.6f}" for n, v in importance_rows]) + "\n", encoding="utf-8"
    )

    spark.stop()


if __name__ == "__main__":
    main()
