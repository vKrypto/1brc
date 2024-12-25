mv /home/ashutosh/github/1brc/generate_raw_data/python/100_k_transactions.csv /var/lib/mysql-files/

delete from transactions


LOAD DATA INFILE '/var/lib/mysql-files/100_mil_transactions.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(timestamp, txn_amount, small_description, accountid, status, market_type, symbol, quantity, symbol_price, txn_fee, trade_type, exchangeid);
