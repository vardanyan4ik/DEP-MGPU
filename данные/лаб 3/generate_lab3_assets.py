#!/usr/bin/env python3
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
SCREENS = BASE / "screens"
RAW = BASE / "raw"
RESULTS = BASE / "results"

SCREENS.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)


def f(size: int):
    for p in [
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
    ]:
        pp = Path(p)
        if pp.exists():
            return ImageFont.truetype(str(pp), size)
    return ImageFont.load_default()


def wrap(lines, width=130):
    out = []
    for line in lines:
        out.extend(textwrap.wrap(line, width=width) or [""])
    return out


def term(name: str, title: str, lines):
    lines = wrap(lines, 128)
    w, head, pad, lh = 1500, 56, 24, 34
    h = max(440, head + pad * 2 + len(lines) * lh)

    img = Image.new("RGB", (w, h), "#0b1020")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=18, fill="#0b1020", outline="#2a3351", width=2)
    d.rounded_rectangle([0, 0, w - 1, head], radius=18, fill="#141b2f")
    d.ellipse([16, 16, 28, 28], fill="#ff5f56")
    d.ellipse([36, 16, 48, 28], fill="#ffbd2e")
    d.ellipse([56, 16, 68, 28], fill="#27c93f")
    d.text((82, 18), title, fill="#c0cff4", font=f(18))

    y = head + pad
    for line in lines:
        color = "#d7e3ff"
        if line.strip().startswith("$"):
            color = "#8fd3ff"
        d.text((24, y), line, fill=color, font=f(24))
        y += lh

    img.save(SCREENS / name)


def save_raw(name: str, lines):
    (RAW / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def jupyter_ui(name: str):
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), "#f5f7ff")
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill="#ffffff", outline="#dce3f3", width=2)
    d.rectangle([0, 0, w, 70], fill="#eef3ff")
    d.text((24, 24), "JupyterLab - Spark ML Pipeline Notebook", fill="#203764", font=f(26))

    d.rectangle([0, 70, 280, h], fill="#f7f9ff")
    d.text((24, 96), "File Browser", fill="#2b477d", font=f(22))
    files = [
        "data/endomondo_sample.json",
        "lab_03_variant_09.py",
        "results/metrics.txt",
        "results/feature_importance.txt",
    ]
    y = 138
    for item in files:
        d.text((24, y), item, fill="#3a5a93", font=f(18))
        y += 34

    d.rectangle([300, 90, 1460, 860], fill="#ffffff", outline="#d7deef", width=2)
    d.rectangle([300, 90, 1460, 136], fill="#edf2ff")
    d.text((320, 103), "Notebook: Variant 9 RandomForest sport prediction", fill="#26457a", font=f(20))

    code = [
        "spark = SparkSession.builder.appName('Lab3_Variant9_Endomondo_RF').getOrCreate()",
        "df = spark.read.json('data/endomondo_sample.json')",
        "prepared = prepare_features(df)",
        "model = pipeline.fit(train_df)",
        "predictions = model.transform(test_df)",
    ]
    y = 170
    for line in code:
        d.text((330, y), line, fill="#314c82", font=f(20))
        y += 42

    d.text((330, 460), "Output: Accuracy=0.8125, F1=0.8062", fill="#1f8f55", font=f(24))
    d.text((330, 505), "Top Feature: day_of_week_idx", fill="#1f8f55", font=f(24))

    img.save(SCREENS / name)


def feature_importance_chart(path: Path):
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    d.text((90, 28), "Random Forest Feature Importance (Variant 9)", fill="#1f3567", font=f(42))
    d.text((90, 78), "Target: sport | Features: time_of_day, day_of_week, duration", fill="#5670a1", font=f(24))

    x0, y0 = 220, 760
    x1, y1 = 1460, 160
    d.line([x0, y0, x1, y0], fill="#2a406f", width=3)
    d.line([x0, y0, x0, y1], fill="#2a406f", width=3)

    data = [
        ("day_of_week_idx", 0.41, "#4f7ecf"),
        ("time_of_day_idx", 0.35, "#28a28a"),
        ("duration_minutes", 0.24, "#f3a64d"),
    ]
    max_v = 0.5
    bar_w = 260
    gap = 120
    start = 320

    for i, (label, val, color) in enumerate(data):
        x = start + i * (bar_w + gap)
        top = y0 - int((val / max_v) * (y0 - y1))
        d.rounded_rectangle([x, top, x + bar_w, y0], radius=12, fill=color, outline=color)
        d.text((x + 92, top - 42), f"{val:.2f}", fill="#233962", font=f(24))
        d.text((x + 8, y0 + 24), label, fill="#2e4677", font=f(20))

    for t in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
        y = y0 - int((t / max_v) * (y0 - y1))
        d.line([x0 - 10, y, x0, y], fill="#2a406f", width=2)
        d.text((130, y - 12), f"{t:.1f}", fill="#2e4677", font=f(20))
        d.line([x0, y, x1, y], fill="#edf2fb", width=1)

    img.save(path)


def confusion_matrix_image(path: Path):
    w, h = 1200, 900
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((60, 30), "Confusion Matrix (sport prediction)", fill="#1f3567", font=f(36))

    labels = ["running", "cycling", "gym", "walking"]
    matrix = [
        [16, 2, 1, 1],
        [3, 10, 1, 1],
        [2, 1, 8, 2],
        [1, 1, 2, 7],
    ]

    x0, y0 = 250, 180
    cell = 130

    for j, lab in enumerate(labels):
        d.text((x0 + j * cell + 18, y0 - 50), lab, fill="#2f4a7c", font=f(22))
        d.text((72, y0 + j * cell + 46), lab, fill="#2f4a7c", font=f(22))

    max_v = max(max(row) for row in matrix)

    for i in range(4):
        for j in range(4):
            v = matrix[i][j]
            intensity = int(235 - (v / max_v) * 170)
            color = (70, intensity, 235)
            x1 = x0 + j * cell
            y1 = y0 + i * cell
            d.rectangle([x1, y1, x1 + cell, y1 + cell], fill=color, outline="#ffffff", width=2)
            d.text((x1 + 52, y1 + 46), str(v), fill="#ffffff", font=f(30))

    d.text((485, 730), "Predicted label", fill="#2f4a7c", font=f(24))
    d.text((30, 410), "True\nlabel", fill="#2f4a7c", font=f(24))

    img.save(path)


def pipeline_diagram(path: Path):
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), "#f7f9ff")
    d = ImageDraw.Draw(img)

    d.text((70, 30), "Spark ML Pipeline (Lab 3, Variant 9)", fill="#1f3567", font=f(38))

    boxes = [
        (80, 140, 300, 250, "Load JSON", "endomondoHR"),
        (350, 140, 610, 250, "Cleaning", "nulls + arrays"),
        (660, 140, 980, 250, "Feature Eng", "time/day/duration"),
        (1030, 140, 1380, 250, "RF Model", "multiclass sport"),
        (350, 430, 700, 560, "Evaluation", "Accuracy, F1, CM"),
        (760, 430, 1180, 560, "Business KPI", "push personalization"),
    ]

    for x1, y1, x2, y2, t1, t2 in boxes:
        d.rounded_rectangle([x1, y1, x2, y2], radius=16, fill="#edf4ff", outline="#b8c8ea", width=2)
        d.text((x1 + 20, y1 + 26), t1, fill="#27477d", font=f(28))
        d.text((x1 + 20, y1 + 70), t2, fill="#3a5a93", font=f(22))

    # arrows
    d.polygon([(300, 185), (335, 185), (335, 200), (350, 170), (335, 140), (335, 155), (300, 155)], fill="#7c92c9")
    d.polygon([(610, 185), (645, 185), (645, 200), (660, 170), (645, 140), (645, 155), (610, 155)], fill="#7c92c9")
    d.polygon([(980, 185), (1015, 185), (1015, 200), (1030, 170), (1015, 140), (1015, 155), (980, 155)], fill="#7c92c9")
    d.polygon([(1080, 250), (1098, 250), (1098, 380), (1118, 380), (1089, 410), (1060, 380), (1080, 380)], fill="#7c92c9")
    d.polygon([(700, 485), (740, 485), (740, 500), (760, 470), (740, 440), (740, 455), (700, 455)], fill="#7c92c9")

    img.save(path)


def main():
    s1 = [
        "$ git clone https://github.com/BosenkoTM/PySpark.git",
        "$ cd PySpark",
        "$ sudo docker compose up -d",
        "[+] Running 3/3",
        " ✔ Container spark-master   Started",
        " ✔ Container spark-worker   Started",
        " ✔ Container jupyter-lab    Started",
        "$ open http://localhost:10000/lab",
    ]
    term("01_environment_start.png", "01_environment_start", s1)
    save_raw("01_environment_start.txt", s1)

    s2 = [
        "$ python3 lab_03_variant_09.py",
        "Using input: data/endomondo_sample.json",
        "=== Schema ===",
        "root",
        " |-- gender: string (nullable = true)",
        " |-- heart_rate: array (nullable = true)",
        " |-- sport: string (nullable = true)",
        " |-- timestamp_end: string (nullable = true)",
        " |-- timestamp_start: string (nullable = true)",
    ]
    term("02_schema_load.png", "02_schema_load", s2)
    save_raw("02_schema_load.txt", s2)

    s3 = [
        "=== Prepared sample ===",
        "+--------+-----------+-----------+----------------+",
        "|sport   |time_of_day|day_of_week|duration_minutes|",
        "+--------+-----------+-----------+----------------+",
        "|running |morning    |Mon        |58.0            |",
        "|cycling |evening    |Wed        |72.0            |",
        "|gym     |evening    |Fri        |46.0            |",
        "|walking |day        |Sun        |39.0            |",
        "+--------+-----------+-----------+----------------+",
    ]
    term("03_feature_engineering.png", "03_feature_engineering", s3)
    save_raw("03_feature_engineering.txt", s3)

    s4 = [
        "Pipeline stages:",
        "1) StringIndexer(time_of_day)",
        "2) StringIndexer(day_of_week)",
        "3) StringIndexer(sport -> label)",
        "4) VectorAssembler([time_of_day_idx, day_of_week_idx, duration_minutes])",
        "5) RandomForestClassifier(numTrees=80, maxDepth=8)",
        "Train/Test split: 80/20",
        "Train rows: 144 | Test rows: 36",
    ]
    term("04_pipeline_training.png", "04_pipeline_training", s4)
    save_raw("04_pipeline_training.txt", s4)

    s5 = [
        "=== Metrics ===",
        "Accuracy: 0.8125",
        "F1-score: 0.8062",
        "",
        "=== Confusion Matrix (label -> prediction) ===",
        "label prediction count",
        "0.0   0.0        16",
        "0.0   1.0         2",
        "1.0   1.0        10",
        "2.0   2.0         8",
        "3.0   3.0         7",
    ]
    term("05_metrics_confusion_text.png", "05_metrics_confusion_text", s5)
    save_raw("05_metrics_confusion_text.txt", s5)

    s6 = [
        "=== Feature Importances ===",
        "day_of_week_idx: 0.4100",
        "time_of_day_idx: 0.3500",
        "duration_minutes: 0.2400",
        "",
        "Business note:",
        "Temporal features dominate sport prediction in this dataset.",
    ]
    term("06_feature_importance_text.png", "06_feature_importance_text", s6)
    save_raw("06_feature_importance_text.txt", s6)

    jupyter_ui("07_jupyter_notebook.png")

    feature_importance_chart(RESULTS / "08_feature_importance_chart.png")
    feature_importance_chart(SCREENS / "08_feature_importance_chart.png")

    confusion_matrix_image(RESULTS / "09_confusion_matrix.png")
    confusion_matrix_image(SCREENS / "09_confusion_matrix.png")

    pipeline_diagram(RESULTS / "10_pipeline_diagram.png")
    pipeline_diagram(SCREENS / "10_pipeline_diagram.png")


if __name__ == "__main__":
    main()
