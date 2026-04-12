from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    coalesce,
    count,
    month,
    sum as _sum,
    to_date,
    when,
    year,
)


INPUT_PATH = "hdfs://localhost:9000/user/hadoop/lab_01/input/train.csv"
OUTPUT_BASE = "hdfs://localhost:9000/user/hadoop/lab_01/output"


def build_spark() -> SparkSession:
    spark = (
        SparkSession.builder.appName("Lab1_Variant9_Seasonality")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def main() -> None:
    spark = build_spark()

    # 1) Загрузка данных из HDFS
    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(INPUT_PATH)
    )

    print("\n=== Схема исходного датасета ===")
    df.printSchema()

    # 2) Приведение даты и очистка
    # На разных источниках дата может быть как yyyy-MM-dd, так и dd-MM-yyyy
    df = df.withColumn(
        "sale_date",
        coalesce(
            to_date(col("Date"), "yyyy-MM-dd"),
            to_date(col("Date"), "dd-MM-yyyy"),
        ),
    )

    print("\n=== Проверка пропусков до очистки ===")
    null_stats_before = df.select(
        [
            count(when(col(c).isNull(), c)).alias(c)
            for c in ["Store", "Dept", "Date", "Weekly_Sales", "sale_date"]
        ]
    )
    null_stats_before.show(truncate=False)

    cleaned_base = (
        df.filter(col("sale_date").isNotNull())
        .filter(col("Dept").isNotNull())
        .filter(col("Weekly_Sales").isNotNull())
        .filter(col("Weekly_Sales") > 0)
        .withColumn("Store", col("Store").cast("int"))
        .withColumn("Dept", col("Dept").cast("int"))
        .withColumn("Weekly_Sales", col("Weekly_Sales").cast("double"))
        .withColumn("year", year("sale_date"))
        .withColumn("month", month("sale_date"))
        .withColumn("category", col("Dept").cast("string"))
    )

    rows_before_dedup = cleaned_base.count()
    cleaned = cleaned_base.dropDuplicates(
        ["Store", "Dept", "sale_date", "Weekly_Sales", "IsHoliday"]
    )
    rows_after_dedup = cleaned.count()

    print("\n=== Удаление дубликатов ===")
    print(f"rows_before_dedup: {rows_before_dedup}")
    print(f"rows_after_dedup:  {rows_after_dedup}")
    print(f"duplicates_removed: {rows_before_dedup - rows_after_dedup}")

    print("\n=== Проверка пропусков после очистки ===")
    null_stats_after = cleaned.select(
        [
            count(when(col(c).isNull(), c)).alias(c)
            for c in ["Store", "category", "sale_date", "Weekly_Sales", "year", "month"]
        ]
    )
    null_stats_after.show(truncate=False)

    # 3) Задание 1: месяцы с пиковыми продажами
    monthly_total = (
        cleaned.groupBy("year", "month")
        .agg(_sum("Weekly_Sales").alias("revenue"))
        .orderBy("year", "month")
    )

    print("\n=== Выручка по месяцам и годам ===")
    monthly_total.show(100, truncate=False)

    peak_months = (
        cleaned.groupBy("month")
        .agg(_sum("Weekly_Sales").alias("total_revenue_all_years"))
        .orderBy(col("total_revenue_all_years").desc())
    )

    print("\n=== Пиковые месяцы продаж (по всем годам) ===")
    peak_months.show(12, truncate=False)

    # 4) Задание 2: Spark SQL и сезонные коэффициенты по категориям
    monthly_category = (
        cleaned.groupBy("category", "year", "month")
        .agg(_sum("Weekly_Sales").alias("month_revenue"))
        .orderBy("category", "year", "month")
    )
    monthly_category.createOrReplaceTempView("monthly_category")

    seasonal_coeff = spark.sql(
        """
        WITH cat_month_sum AS (
            SELECT
                category,
                month,
                SUM(month_revenue) AS month_revenue
            FROM monthly_category
            GROUP BY category, month
        ),
        cat_avg AS (
            SELECT
                category,
                AVG(month_revenue) AS avg_month_revenue
            FROM cat_month_sum
            GROUP BY category
        )
        SELECT
            s.category,
            s.month,
            ROUND(s.month_revenue / a.avg_month_revenue, 3) AS seasonal_coefficient
        FROM cat_month_sum s
        JOIN cat_avg a ON s.category = a.category
        ORDER BY s.category, s.month
        """
    )

    print("\n=== Сезонные коэффициенты по категориям ===")
    seasonal_coeff.show(200, truncate=False)

    # 5) Дополнительная бизнес-метрика: средний чек по категориям
    avg_check = (
        cleaned.groupBy("category")
        .agg(avg("Weekly_Sales").alias("avg_weekly_sales"))
        .orderBy(col("avg_weekly_sales").desc())
    )

    print("\n=== Средняя недельная выручка по категориям ===")
    avg_check.show(30, truncate=False)

    # 6) Сохранение результатов в HDFS
    monthly_total.write.mode("overwrite").option("header", "true").csv(
        f"{OUTPUT_BASE}/monthly_total"
    )
    seasonal_coeff.write.mode("overwrite").option("header", "true").csv(
        f"{OUTPUT_BASE}/seasonal_coefficients"
    )

    # 7) Визуализация (линейный график сезонности по годам)
    pdf = monthly_total.toPandas()
    pdf["year"] = pdf["year"].astype(int)
    pdf["month"] = pdf["month"].astype(int)

    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=pdf, x="month", y="revenue", hue="year", marker="o")
    plt.title("Сезонность продаж по годам")
    plt.xlabel("Месяц")
    plt.ylabel("Выручка")
    plt.xticks(range(1, 13))
    plt.tight_layout()

    out_plot = Path("results") / "09_seasonality_by_year.png"
    out_plot.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_plot, dpi=150)
    print(f"\nГрафик сохранен: {out_plot.resolve()}")

    spark.stop()


if __name__ == "__main__":
    main()
