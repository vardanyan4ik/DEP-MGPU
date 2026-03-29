# Лабораторная работа 2 — Вариант 9 (Polyglot Persistence)

## Тема
Изучение и применение различных типов NoSQL баз данных на бизнес-кейсе стриминговой платформы.

## Вариант 9
1. **MongoDB**: агрегация количества пользователей по городам (`group by city`).
2. **GraphDB/SPARQL**:
   - найти фильмы с `>1000` комментариев;
   - найти фильмы до `1980`, где актер и режиссер совпадают.
3. **Business Insight**: сравнить вовлеченность аудитории в классических и современных фильмах.

## Структура
- `docker-compose.yml` — запуск сервисов MongoDB, Cassandra, GraphDB, Redis.
- `scripts/mongo/` — скрипты CRUD и агрегации для MongoDB.
- `scripts/cassandra/` — CQL-схема и загрузка логов.
- `scripts/sparql/` — SPARQL-запросы для GraphDB (вариант 9).
- `data/` — sample RDF-данные.
- `Report_Lab2.md` — подробный отчет со скриншотами.
- `screens/` — скриншоты шагов выполнения.
- `raw/` — текстовый вывод команд и результатов.
- `results/` — аналитические графики.

## Быстрый сценарий
```bash
cd ~/Downloads/dba/nonrel/graphdb
sudo docker compose stop
sudo docker compose start
```

Веб-интерфейсы:
- Mongo-Express: http://localhost:28203
- Admin Mongo: http://localhost:28204
- GraphDB: http://localhost:7200
- Redis Commander: http://localhost:28119

## Скрипты по варианту 9
- MongoDB: `scripts/mongo/02_variant9_city_aggregation.js`
- SPARQL #1: `scripts/sparql/01_movies_gt_1000_comments.rq`
- SPARQL #2: `scripts/sparql/02_pre1980_actor_director_same.rq`
- Аналитический SPARQL: `scripts/sparql/03_business_compare_classic_modern.rq`
