CREATE KEYSPACE IF NOT EXISTS streaming_ks
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE streaming_ks;

CREATE TABLE IF NOT EXISTS watch_logs (
  user_id uuid,
  event_ts timestamp,
  action text,
  movie_id text,
  device_type text,
  city text,
  PRIMARY KEY (user_id, event_ts)
) WITH CLUSTERING ORDER BY (event_ts DESC);
