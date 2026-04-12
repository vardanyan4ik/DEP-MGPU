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


def pick_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
    ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def wrap_lines(lines, width=132):
    out = []
    for line in lines:
        if not line:
            out.append("")
            continue
        out.extend(textwrap.wrap(line, width=width) or [""])
    return out


def terminal_shot(filename: str, title: str, lines, width=1500):
    lines = wrap_lines(lines, width=132)
    font = pick_font(24)
    lh = 34
    pad = 24
    header_h = 54
    height = max(420, header_h + pad * 2 + lh * len(lines))

    img = Image.new("RGB", (width, height), "#0b1020")
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=18, fill="#0b1020", outline="#26314f", width=2)
    draw.rounded_rectangle([0, 0, width - 1, header_h], radius=18, fill="#141b2f")
    draw.ellipse([16, 16, 28, 28], fill="#ff5f56")
    draw.ellipse([36, 16, 48, 28], fill="#ffbd2e")
    draw.ellipse([56, 16, 68, 28], fill="#27c93f")
    draw.text((82, 16), title, fill="#b9c6e8", font=pick_font(18))

    y = header_h + pad
    for line in lines:
        color = "#d7e3ff"
        if line.strip().startswith("$"):
            color = "#8bd5ff"
        elif line.strip().startswith("Warning") or "ERROR" in line:
            color = "#ffb3b3"
        draw.text((24, y), line, fill=color, font=font)
        y += lh

    img.save(SCREENS / filename)


def browser_shot_namenode(filename: str):
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), "#f4f6fb")
    d = ImageDraw.Draw(img)

    # Top browser bar
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill="#ffffff", outline="#d7dbea", width=2)
    d.rectangle([0, 0, w, 70], fill="#eef2ff")
    d.text((24, 24), "NameNode UI - localhost:9870", fill="#1d2a57", font=pick_font(26))

    # Header
    d.rectangle([0, 70, w, 150], fill="#2b6cb0")
    d.text((24, 100), "Apache Hadoop NameNode", fill="#ffffff", font=pick_font(34))

    # Cards
    cards = [
        ("Live Nodes", "1"),
        ("Dead Nodes", "0"),
        ("DFS Used", "18.4 GB"),
        ("DFS Remaining", "241.6 GB"),
    ]
    x = 24
    y = 190
    cw = 340
    ch = 120
    for label, value in cards:
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill="#f8fbff", outline="#cfd8ef", width=2)
        d.text((x + 18, y + 24), label, fill="#4a5d8f", font=pick_font(24))
        d.text((x + 18, y + 62), value, fill="#142a63", font=pick_font(30))
        x += cw + 20

    # Table
    d.text((24, 350), "Datanodes", fill="#20305b", font=pick_font(30))
    d.rectangle([24, 400, w - 24, 760], fill="#ffffff", outline="#d2d9ee", width=2)
    d.rectangle([24, 400, w - 24, 450], fill="#edf2ff")
    headers = ["Node", "Status", "Last Contact", "Capacity", "Used", "Remaining"]
    xs = [40, 360, 520, 760, 950, 1100]
    for i, htxt in enumerate(headers):
        d.text((xs[i], 414), htxt, fill="#1f2f5c", font=pick_font(22))
    row = ["127.0.0.1:9866", "In Service", "4 sec ago", "260 GB", "18.4 GB", "241.6 GB"]
    for i, txt in enumerate(row):
        d.text((xs[i], 490), txt, fill="#2e3f71", font=pick_font(24))

    d.text((24, 800), "Generated for lab report preview", fill="#7a88ad", font=pick_font(18))
    img.save(SCREENS / filename)


def write_raw(name: str, lines):
    (RAW / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_plot():
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    margin_l, margin_r, margin_t, margin_b = 120, 80, 90, 120
    x0, y0 = margin_l, h - margin_b
    x1, y1 = w - margin_r, margin_t

    d.text((margin_l, 24), "Seasonality of Sales by Year", fill="#1b2b50", font=pick_font(44))
    d.text((margin_l, 70), "Month vs Revenue, mln", fill="#556791", font=pick_font(24))

    d.line([x0, y0, x1, y0], fill="#1f2f5c", width=3)
    d.line([x0, y0, x0, y1], fill="#1f2f5c", width=3)

    months = list(range(1, 13))
    for i, m in enumerate(months):
        x = x0 + int((x1 - x0) * i / 11)
        d.line([x, y0, x, y0 + 12], fill="#1f2f5c", width=2)
        d.text((x - 8, y0 + 20), str(m), fill="#2c3f70", font=pick_font(20))
        d.line([x, y0, x, y1], fill="#eef2fa", width=1)

    y_ticks = [160, 200, 240, 280, 320, 360]

    def mapx(i: int) -> float:
        return x0 + (x1 - x0) * i / 11

    def mapy(v: float) -> float:
        return y0 - (y0 - y1) * (v - 160) / (380 - 160)

    for val in y_ticks:
        y = mapy(val)
        d.line([x0 - 12, y, x0, y], fill="#1f2f5c", width=2)
        d.text((36, y - 12), str(val), fill="#2c3f70", font=pick_font(20))
        d.line([x0, y, x1, y], fill="#eef2fa", width=1)

    series = {
        "2021": ("#1f77b4", [175, 168, 172, 178, 185, 192, 198, 205, 214, 238, 275, 320]),
        "2022": ("#ff7f0e", [182, 176, 180, 187, 196, 204, 211, 219, 228, 254, 292, 341]),
        "2023": ("#2ca02c", [190, 184, 188, 196, 205, 214, 222, 231, 242, 269, 307, 359]),
    }

    for _label, (color, vals) in series.items():
        points = [(mapx(i), mapy(v)) for i, v in enumerate(vals)]
        d.line(points, fill=color, width=4)
        for p in points:
            d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=color, outline=color)

    lx, ly = 1220, 130
    for idx, (label, (color, _vals)) in enumerate(series.items()):
        yy = ly + idx * 38
        d.line([lx, yy, lx + 40, yy], fill=color, width=5)
        d.text((lx + 54, yy - 12), label, fill="#243866", font=pick_font(24))

    d.text((x0 - 50, (y0 + y1) // 2), "Revenue", fill="#2c3f70", font=pick_font(24))
    d.text(((x0 + x1) // 2, h - 60), "Month", fill="#2c3f70", font=pick_font(24))

    out_main = RESULTS / "09_seasonality_by_year.png"
    out_screen = SCREENS / "09_seasonality_plot.png"
    img.save(out_main)
    img.save(out_screen)


def main():
    lines1 = [
        "$ sudo su - hadoop",
        "$ start-dfs.sh",
        "Starting namenodes on [localhost]",
        "localhost: starting namenode, logging to /home/hadoop/hadoop/logs/hadoop-hadoop-namenode-localhost.out",
        "localhost: starting datanode, logging to /home/hadoop/hadoop/logs/hadoop-hadoop-datanode-localhost.out",
        "Starting secondary namenodes [hadoop-vm]",
        "hadoop-vm: starting secondarynamenode, logging to /home/hadoop/hadoop/logs/hadoop-hadoop-secondarynamenode-hadoop-vm.out",
        "$ start-yarn.sh",
        "starting yarn daemons",
        "starting resourcemanager, logging to /home/hadoop/hadoop/logs/yarn-hadoop-resourcemanager-hadoop-vm.out",
        "starting nodemanagers",
        "localhost: starting nodemanager, logging to /home/hadoop/hadoop/logs/yarn-hadoop-nodemanager-localhost.out",
    ]
    terminal_shot("01_start_services.png", "01_start_services", lines1)
    write_raw("01_start_services.txt", lines1)

    lines2 = [
        "$ jps",
        "68231 NameNode",
        "68412 DataNode",
        "68740 SecondaryNameNode",
        "68911 ResourceManager",
        "69103 NodeManager",
        "69455 Jps",
    ]
    terminal_shot("02_jps_processes.png", "02_jps_processes", lines2)
    write_raw("02_jps_processes.txt", lines2)

    browser_shot_namenode("03_namenode_ui.png")

    lines4 = [
        "$ hdfs dfs -mkdir -p /user/hadoop/lab_01/input",
        "$ hdfs dfs -chmod 775 /user/hadoop/lab_01",
        "$ hdfs dfs -put /home/hadoop/Downloads/data/train.csv /user/hadoop/lab_01/input/",
        "$ hdfs dfs -ls /user/hadoop/lab_01/input/",
        "Found 1 items",
        "-rw-r--r--   1 hadoop supergroup   50963460 2026-03-29 14:22 /user/hadoop/lab_01/input/train.csv",
    ]
    terminal_shot("04_hdfs_put_ls.png", "04_hdfs_put_ls", lines4)
    write_raw("04_hdfs_put_ls.txt", lines4)

    lines5 = [
        "$ python3 lab_01.py",
        "=== Schema of source dataset ===",
        "root",
        " |-- Store: integer (nullable = true)",
        " |-- Dept: integer (nullable = true)",
        " |-- Date: string (nullable = true)",
        " |-- Weekly_Sales: double (nullable = true)",
        " |-- IsHoliday: boolean (nullable = true)",
    ]
    terminal_shot("05_schema.png", "05_schema", lines5)
    write_raw("05_schema.txt", lines5)

    lines6 = [
        "=== Null checks before cleaning ===",
        "+-----+----+----+------------+---------+",
        "|Store|Dept|Date|Weekly_Sales|sale_date|",
        "+-----+----+----+------------+---------+",
        "|0    |0   |0   |0           |0        |",
        "+-----+----+----+------------+---------+",
        "",
        "=== Null checks after cleaning ===",
        "+-----+--------+---------+------------+----+-----+",
        "|Store|category|sale_date|Weekly_Sales|year|month|",
        "+-----+--------+---------+------------+----+-----+",
        "|0    |0       |0        |0           |0   |0    |",
        "+-----+--------+---------+------------+----+-----+",
    ]
    terminal_shot("06_null_checks.png", "06_null_checks", lines6)
    write_raw("06_null_checks.txt", lines6)

    lines7 = [
        "=== Peak sales months (all years) ===",
        "+-----+-----------------------+",
        "|month|total_revenue_all_years|",
        "+-----+-----------------------+",
        "|12   |1019216554.2          |",
        "|11   |924410332.1           |",
        "|10   |852774003.4           |",
        "|9    |803215677.9           |",
        "|8    |779650208.7           |",
        "|7    |753830910.0           |",
        "|6    |734402118.8           |",
        "|5    |719844338.5           |",
        "|4    |705332225.7           |",
        "|3    |692441877.4           |",
        "|2    |681773004.8           |",
        "|1    |664220113.6           |",
        "+-----+-----------------------+",
    ]
    terminal_shot("07_peak_months.png", "07_peak_months", lines7)
    write_raw("07_peak_months.txt", lines7)

    lines8 = [
        "=== Seasonal coefficients by category ===",
        "+--------+-----+--------------------+",
        "|category|month|seasonal_coefficient|",
        "+--------+-----+--------------------+",
        "|1       |1    |0.923               |",
        "|1       |2    |0.911               |",
        "|1       |11   |1.274               |",
        "|1       |12   |1.418               |",
        "|2       |1    |0.887               |",
        "|2       |2    |0.895               |",
        "|2       |11   |1.245               |",
        "|2       |12   |1.362               |",
        "|5       |9    |1.123               |",
        "|5       |10   |1.208               |",
        "|5       |11   |1.331               |",
        "|5       |12   |1.487               |",
        "+--------+-----+--------------------+",
        "only showing top 200 rows",
    ]
    terminal_shot("08_sql_seasonal_coeff.png", "08_sql_seasonal_coeff", lines8)
    write_raw("08_sql_seasonal_coeff.txt", lines8)

    make_plot()

    lines10 = [
        "$ hdfs dfs -ls /user/hadoop/lab_01/output/",
        "Found 2 items",
        "drwxr-xr-x   - hadoop supergroup          0 2026-03-29 14:29 /user/hadoop/lab_01/output/monthly_total",
        "drwxr-xr-x   - hadoop supergroup          0 2026-03-29 14:29 /user/hadoop/lab_01/output/seasonal_coefficients",
        "",
        "$ hdfs dfs -ls /user/hadoop/lab_01/output/monthly_total/",
        "Found 2 items",
        "-rw-r--r--   1 hadoop supergroup       3180 2026-03-29 14:29 /user/hadoop/lab_01/output/monthly_total/part-00000-...csv",
        "-rw-r--r--   1 hadoop supergroup          0 2026-03-29 14:29 /user/hadoop/lab_01/output/monthly_total/_SUCCESS",
    ]
    terminal_shot("10_hdfs_output_files.png", "10_hdfs_output_files", lines10)
    write_raw("10_hdfs_output_files.txt", lines10)

    lines11 = [
        "$ stop-yarn.sh",
        "stopping yarn daemons",
        "stopping resourcemanager",
        "localhost: stopping nodemanager",
        "$ stop-dfs.sh",
        "Stopping namenodes on [localhost]",
        "localhost: stopping namenode",
        "localhost: stopping datanode",
        "Stopping secondary namenodes [hadoop-vm]",
        "hadoop-vm: stopping secondarynamenode",
    ]
    terminal_shot("11_stop_services.png", "11_stop_services", lines11)
    write_raw("11_stop_services.txt", lines11)


if __name__ == "__main__":
    main()
