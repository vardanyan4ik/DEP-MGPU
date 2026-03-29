USE streaming_ks;

SELECT user_id, event_ts, action, movie_id, city
FROM watch_logs
LIMIT 20;
