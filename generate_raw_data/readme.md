generate_date_python_v0 : 
`
About: using faker to generate data.
for 100_000 rows: total time: 4.1128 seconds

2024-12-22 00:49:43,692 - trade_logger - INFO - Function 'write_to_csv' took 0.1623 seconds to execute.
2024-12-22 00:49:43,692 - trade_logger - INFO - 50000(50.0%) rows written to transactions.csv, time elapsed: 2.05 sec
2024-12-22 00:49:45,745 - trade_logger - INFO - Function 'write_to_csv' took 0.1598 seconds to execute.
2024-12-22 00:49:45,745 - trade_logger - INFO - 50000(100.0%) rows written to transactions.csv, time elapsed: 4.11 sec
2024-12-22 00:49:45,752 - trade_logger - INFO - Function 'generate_transactions' took 4.1128 seconds to execute.
`

generate_date_python_v1 : 
`
optimization: (5x faster) using custom function to create random data

for 1_000_000 rows: took 7.7766 sec
for 100_000 rows: total time: 0.7984 seconds

2024-12-22 00:57:07,277 - trade_logger - INFO - started.....
2024-12-22 00:57:07,679 - trade_logger - INFO - Function 'write_to_csv' took 0.1477 seconds to execute.
2024-12-22 00:57:07,679 - trade_logger - INFO - 50000(50.0%) rows written to transactions.csv, time elapsed: 0.4 sec
2024-12-22 00:57:08,072 - trade_logger - INFO - Function 'write_to_csv' took 0.1467 seconds to execute.
2024-12-22 00:57:08,072 - trade_logger - INFO - 50000(100.0%) rows written to transactions.csv, time elapsed: 0.79 sec
2024-12-22 00:57:08,076 - trade_logger - INFO - Function 'generate_transactions' took 0.7984 seconds to execute.



generate_date_python_v2 : 
`
optimization: using tuple for data generation.
optimization: write into file asynchronously.
failed stategy: 
for 1_000_000 rows: took 6.4008 sec
for 100_000 rows: total time: 0.5670 seconds
for 100_000_000rows took 625.5717 seconds to execute.


2024-12-22 02:09:20,038 - trade_logger - INFO - Function 'generate_transactions' took 0.0488 seconds to execute.
2024-12-22 02:09:21,573 - trade_logger - INFO - Function 'main' took 6.4008 seconds to execute.