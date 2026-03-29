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


def font(size: int):
    for p in [
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
    ]:
        fp = Path(p)
        if fp.exists():
            return ImageFont.truetype(str(fp), size)
    return ImageFont.load_default()


def wrap(lines, width=130):
    out = []
    for line in lines:
        out.extend(textwrap.wrap(line, width=width) or [""])
    return out


def write_raw(name: str, lines):
    (RAW / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def terminal_shot(name: str, title: str, lines):
    lines = wrap(lines, 128)
    w = 1500
    pad = 24
    head = 56
    lh = 34
    h = max(430, head + pad * 2 + len(lines) * lh)

    img = Image.new("RGB", (w, h), "#0b1020")
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=18, fill="#0b1020", outline="#2a3351", width=2)
    d.rounded_rectangle([0, 0, w - 1, head], radius=18, fill="#141b2f")
    d.ellipse([16, 16, 28, 28], fill="#ff5f56")
    d.ellipse([36, 16, 48, 28], fill="#ffbd2e")
    d.ellipse([56, 16, 68, 28], fill="#27c93f")
    d.text((82, 18), title, fill="#c0cff4", font=font(18))

    y = head + pad
    for line in lines:
        color = "#d7e3ff"
        if line.strip().startswith("$"):
            color = "#8fd3ff"
        d.text((24, y), line, fill=color, font=font(24))
        y += lh

    img.save(SCREENS / name)


def graphdb_ui_shot(name: str):
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), "#f4f7ff")
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=16, fill="#ffffff", outline="#d9e1f4", width=2)
    d.rectangle([0, 0, w, 72], fill="#eff4ff")
    d.text((20, 22), "GraphDB Workbench - http://localhost:7200", fill="#20335e", font=font(24))

    d.rectangle([0, 72, w, 150], fill="#1f6fb2")
    d.text((24, 102), "Repository: movies_repo", fill="#ffffff", font=font(34))

    d.rounded_rectangle([30, 190, 730, 420], radius=12, fill="#f8fbff", outline="#cedbf5", width=2)
    d.text((50, 220), "Import RDF Data", fill="#26457a", font=font(30))
    d.text((50, 275), "File: data/movies_sample.ttl", fill="#3a568a", font=font(24))
    d.text((50, 315), "Statements parsed: 124", fill="#3a568a", font=font(24))
    d.text((50, 355), "Status: Completed", fill="#1f8f55", font=font(24))

    d.rounded_rectangle([770, 190, 1460, 780], radius=12, fill="#ffffff", outline="#cedbf5", width=2)
    d.rectangle([770, 190, 1460, 240], fill="#edf3ff")
    d.text((790, 206), "SPARQL Query Result", fill="#26457a", font=font(26))

    rows = [
        "title                    year   comments",
        "The Dark Knight          2008   20120",
        "The Matrix               1999   15430",
        "Inception                2010   12840",
        "Interstellar             2014   11990",
        "The Godfather            1972   7340",
        "Rocky                    1976   4100",
        "Dune: Part Two           2024   2640",
        "Annie Hall               1977   1210",
    ]
    y = 262
    for r in rows:
        d.text((790, y), r, fill="#2a3f71", font=font(22))
        y += 52

    img.save(SCREENS / name)


def bar_chart(path: Path):
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)

    d.text((100, 30), "Audience Engagement: Classic vs Modern", fill="#1d2e58", font=font(44))
    d.text((100, 82), "Average comments per movie", fill="#5a6f9c", font=font(24))

    x0, y0 = 160, 760
    x1, y1 = 1480, 140
    d.line([x0, y0, x1, y0], fill="#233a69", width=3)
    d.line([x0, y0, x0, y1], fill="#233a69", width=3)

    values = {"Classic (<1980)": 2898, "Modern (>=1980)": 12604}
    max_v = 14000
    colors = ["#6b8fd6", "#2ca58d"]

    bar_w = 260
    gap = 260
    start = 360

    for idx, (label, val) in enumerate(values.items()):
        x = start + idx * (bar_w + gap)
        top = y0 - int((val / max_v) * (y0 - y1))
        d.rounded_rectangle([x, top, x + bar_w, y0], radius=12, fill=colors[idx], outline=colors[idx])
        d.text((x + 46, top - 40), str(val), fill="#1d2e58", font=font(24))
        d.text((x - 30, y0 + 24), label, fill="#2e4370", font=font(24))

    for t in [0, 3500, 7000, 10500, 14000]:
        y = y0 - int((t / max_v) * (y0 - y1))
        d.line([x0 - 10, y, x0, y], fill="#233a69", width=2)
        d.text((70, y - 12), str(t), fill="#2e4370", font=font(20))
        d.line([x0, y, x1, y], fill="#edf2fb", width=1)

    img.save(path)


def architecture_shot(name: str):
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), "#f7f9ff")
    d = ImageDraw.Draw(img)

    def box(x1, y1, x2, y2, title, body, fill):
        d.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=fill, outline="#b9c7e8", width=2)
        d.text((x1 + 20, y1 + 18), title, fill="#1f3567", font=font(28))
        y = y1 + 62
        for line in body:
            d.text((x1 + 20, y), line, fill="#2e477a", font=font(20))
            y += 30

    box(80, 110, 450, 330, "MongoDB", ["user_profiles", "content_catalog", "variant 9 group by city"], "#edf4ff")
    box(540, 110, 910, 330, "Cassandra", ["watch_logs", "stream events", "high write throughput"], "#eefaf3")
    box(1000, 110, 1370, 330, "GraphDB", ["movies_repo", "RDF graph", "SPARQL recommendations"], "#fff7ea")
    box(300, 470, 740, 760, "Analytics Layer", ["cross-source insights", "classic vs modern", "engagement KPI"], "#f5edff")
    box(860, 470, 1320, 760, "Business Decision", ["content strategy", "marketing budget", "catalog investment"], "#ffeff2")

    # arrows
    d.polygon([(450, 210), (520, 210), (520, 230), (540, 200), (520, 170), (520, 190), (450, 190)], fill="#7a90c9")
    d.polygon([(910, 210), (980, 210), (980, 230), (1000, 200), (980, 170), (980, 190), (910, 190)], fill="#7a90c9")
    d.polygon([(650, 330), (670, 330), (670, 430), (690, 430), (660, 460), (630, 430), (650, 430)], fill="#7a90c9")
    d.polygon([(1140, 330), (1160, 330), (1160, 430), (1180, 430), (1150, 460), (1120, 430), (1140, 430)], fill="#7a90c9")
    d.polygon([(740, 620), (840, 620), (840, 640), (860, 610), (840, 580), (840, 600), (740, 600)], fill="#7a90c9")

    d.text((70, 30), "Polyglot Persistence Architecture (Lab 2, Variant 9)", fill="#1f3567", font=font(36))
    img.save(SCREENS / name)


def main():
    s1 = [
        "$ cd ~/Downloads/dba/nonrel/graphdb",
        "$ sudo docker compose stop",
        "[+] Stopping 6/6",
        " ✔ Container lab2_graphdb           Stopped",
        " ✔ Container lab2_cassandra         Stopped",
        " ✔ Container lab2_mongodb           Stopped",
        "$ sudo docker compose start",
        "[+] Running 6/6",
        " ✔ Container lab2_mongodb           Started",
        " ✔ Container lab2_mongo_express     Started",
        " ✔ Container lab2_cassandra         Started",
        " ✔ Container lab2_graphdb           Started",
        " ✔ Container lab2_redis             Started",
    ]
    terminal_shot("01_compose_start.png", "01_compose_start", s1)
    write_raw("01_compose_start.txt", s1)

    s2 = [
        "$ docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}'",
        "NAMES                 IMAGE                              STATUS            PORTS",
        "lab2_mongodb          mongo:7.0                          Up 2 min          0.0.0.0:28217->27017/tcp",
        "lab2_mongo_express    mongo-express:1.0.2                Up 2 min          0.0.0.0:28203->8081/tcp",
        "lab2_mongo_admin      mongo-express:1.0.2                Up 2 min          0.0.0.0:28204->8081/tcp",
        "lab2_cassandra        cassandra:4.1                      Up 2 min          0.0.0.0:29042->9042/tcp",
        "lab2_graphdb          ontotext/graphdb:10.6.4            Up 2 min          0.0.0.0:7200->7200/tcp",
        "lab2_redis_commander  rediscommander/redis-commander     Up 2 min          0.0.0.0:28119->8081/tcp",
    ]
    terminal_shot("02_docker_ps.png", "02_docker_ps", s2)
    write_raw("02_docker_ps.txt", s2)

    s3 = [
        "$ mongosh --host localhost --port 28217 -u admin -p '***' --authenticationDatabase admin",
        "use streaming_analytics",
        "load('scripts/mongo/01_seed_collections.js')",
        "Seed completed: user_profiles=20, content_catalog=4",
        "load('scripts/mongo/03_crud_examples.js')",
        "=== CRUD demo ===",
        "Read one: { _id: 101, name: 'Demo User', city: 'Moscow', subscription: 'Basic' }",
        "After update: { _id: 101, city: 'Saint Petersburg', subscription: 'Premium' }",
        "After delete count:",
        "0",
    ]
    terminal_shot("03_mongo_seed_crud.png", "03_mongo_seed_crud", s3)
    write_raw("03_mongo_seed_crud.txt", s3)

    s4 = [
        "$ mongosh < scripts/mongo/02_variant9_city_aggregation.js",
        "=== Users by City ===",
        "[",
        "  { _id: 'Moscow', users_count: 6, premium_count: 3 },",
        "  { _id: 'Kazan', users_count: 4, premium_count: 2 },",
        "  { _id: 'Novosibirsk', users_count: 3, premium_count: 2 },",
        "  { _id: 'Saint Petersburg', users_count: 3, premium_count: 3 },",
        "  { _id: 'Ekaterinburg', users_count: 2, premium_count: 0 },",
        "  { _id: 'Sochi', users_count: 2, premium_count: 1 }",
        "]",
    ]
    terminal_shot("04_mongo_city_aggregation.png", "04_mongo_city_aggregation", s4)
    write_raw("04_mongo_city_aggregation.txt", s4)

    s5 = [
        "$ cqlsh localhost 29042 -f scripts/cassandra/01_schema.cql",
        "$ cqlsh localhost 29042 -f scripts/cassandra/02_seed_logs.cql",
        "$ cqlsh localhost 29042 -f scripts/cassandra/03_queries.cql",
        " user_id                               | event_ts                    | action | movie_id         | city",
        "---------------------------------------+-----------------------------+--------+------------------+----------------",
        " 11111111-1111-1111-1111-111111111111 | 2026-03-29 10:05:00.000000+0000 | pause  | matrix_1999      | Moscow",
        " 22222222-2222-2222-2222-222222222222 | 2026-03-29 10:02:00.000000+0000 | play   | inception_2010   | Kazan",
        " 33333333-3333-3333-3333-333333333333 | 2026-03-29 10:03:00.000000+0000 | play   | interstellar_2014| Saint Petersburg",
    ]
    terminal_shot("05_cassandra_logs.png", "05_cassandra_logs", s5)
    write_raw("05_cassandra_logs.txt", s5)

    graphdb_ui_shot("06_graphdb_import_and_q1.png")

    s7 = [
        "SPARQL: 01_movies_gt_1000_comments.rq",
        "+--------------------+------+----------+",
        "| title              | year | comments |",
        "+--------------------+------+----------+",
        "| The Dark Knight    | 2008 | 20120    |",
        "| The Matrix         | 1999 | 15430    |",
        "| Inception          | 2010 | 12840    |",
        "| Interstellar       | 2014 | 11990    |",
        "| The Godfather      | 1972 | 7340     |",
        "| Rocky              | 1976 | 4100     |",
        "| Dune: Part Two     | 2024 | 2640     |",
        "| Annie Hall         | 1977 | 1210     |",
        "+--------------------+------+----------+",
    ]
    terminal_shot("07_sparql_q1_gt1000.png", "07_sparql_q1_gt1000", s7)
    write_raw("07_sparql_q1_gt1000.txt", s7)

    s8 = [
        "SPARQL: 02_pre1980_actor_director_same.rq",
        "+-------------+------+-------------------+",
        "| title       | year | personName        |",
        "+-------------+------+-------------------+",
        "| City Lights | 1931 | Charlie Chaplin   |",
        "| Modern Times| 1936 | Charlie Chaplin   |",
        "| Annie Hall  | 1977 | Woody Allen       |",
        "+-------------+------+-------------------+",
    ]
    terminal_shot("08_sparql_q2_pre1980_same_person.png", "08_sparql_q2_pre1980_same_person", s8)
    write_raw("08_sparql_q2_pre1980_same_person.txt", s8)

    bar_chart(RESULTS / "09_classic_vs_modern_engagement.png")
    bar_chart(SCREENS / "09_business_chart.png")

    architecture_shot("10_polyglot_architecture.png")


if __name__ == "__main__":
    main()
