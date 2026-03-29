USE streaming_ks;

INSERT INTO watch_logs (user_id, event_ts, action, movie_id, device_type, city)
VALUES (11111111-1111-1111-1111-111111111111, '2026-03-29 10:00:00', 'play', 'matrix_1999', 'mobile', 'Moscow');
INSERT INTO watch_logs (user_id, event_ts, action, movie_id, device_type, city)
VALUES (11111111-1111-1111-1111-111111111111, '2026-03-29 10:05:00', 'pause', 'matrix_1999', 'mobile', 'Moscow');
INSERT INTO watch_logs (user_id, event_ts, action, movie_id, device_type, city)
VALUES (22222222-2222-2222-2222-222222222222, '2026-03-29 10:02:00', 'play', 'inception_2010', 'tv', 'Kazan');
INSERT INTO watch_logs (user_id, event_ts, action, movie_id, device_type, city)
VALUES (33333333-3333-3333-3333-333333333333, '2026-03-29 10:03:00', 'play', 'interstellar_2014', 'web', 'Saint Petersburg');
INSERT INTO watch_logs (user_id, event_ts, action, movie_id, device_type, city)
VALUES (44444444-4444-4444-4444-444444444444, '2026-03-29 10:06:00', 'stop', 'citylights_1931', 'tv', 'Novosibirsk');
