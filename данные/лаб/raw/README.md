# Логи команд (raw)

Рекомендуется сохранять текстовый вывод команд в эту папку, чтобы при необходимости приложить доказательства выполнения.

Пример:

```bash
jps > raw/02_jps.txt
hdfs dfs -ls /user/hadoop/lab_01/input/ > raw/04_hdfs_input_ls.txt
python3 lab_01.py > raw/05_pyspark_run.txt 2>&1
hdfs dfs -ls /user/hadoop/lab_01/output/ > raw/10_hdfs_output_ls.txt
```

После этого удобно делать скриншоты прямо из терминала по соответствующим шагам.
