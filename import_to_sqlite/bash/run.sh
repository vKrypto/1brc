for file in /var/lib/mysql-files/transactions_chunks/chunk_*; do
    mysql -u root -p trades_db -e "
    LOAD DATA INFILE '$file'
    INTO TABLE transactions_staging
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"' 
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;";
done