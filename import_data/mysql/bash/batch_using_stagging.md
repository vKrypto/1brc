
# Bulk Import of CSV Data into MySQL

This guide outlines the steps to import large CSV data into a MySQL database using a staging table.

---
## Step 0: Create the Original Table

```sql
CREATE TABLE transactions_staging (
    timestamp DATETIME(6) NOT NULL DEFAULT '1970-01-01 00:00:00.000000',
    txn_amount DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    small_description VARCHAR(255) NOT NULL DEFAULT '',
    accountid BIGINT NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'unknown',
    market_type VARCHAR(50) NOT NULL DEFAULT 'unknown',
    symbol VARCHAR(10) NOT NULL DEFAULT '',
    quantity DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    symbol_price DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    txn_fee DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    trade_type VARCHAR(10) NOT NULL DEFAULT 'unknown',
    exchangeid INT NOT NULL DEFAULT 0
) ENGINE=CSV;

ALTER TABLE transactions_staging DISABLE KEYS;
SET FOREIGN_KEY_CHECKS = 0;
```


## Step 1: Create the Staging Table

```sql
CREATE TABLE transactions_staging (
    timestamp DATETIME(6) NOT NULL DEFAULT '1970-01-01 00:00:00.000000',
    txn_amount DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    small_description VARCHAR(255) NOT NULL DEFAULT '',
    accountid BIGINT NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'unknown',
    market_type VARCHAR(50) NOT NULL DEFAULT 'unknown',
    symbol VARCHAR(10) NOT NULL DEFAULT '',
    quantity DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    symbol_price DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    txn_fee DECIMAL(20,8) NOT NULL DEFAULT 0.0,
    trade_type VARCHAR(10) NOT NULL DEFAULT 'unknown',
    exchangeid INT NOT NULL DEFAULT 0
) ENGINE=CSV;

ALTER TABLE transactions_staging DISABLE KEYS;
SET FOREIGN_KEY_CHECKS = 0;
```

---

## Step 2: Pre-process the CSV File

Split the CSV file into manageable chunks for processing:

```bash
mkdir -p /var/lib/mysql-files/transactions_chunks
split -l 1000000 /var/lib/mysql-files/100_mil_transactions.csv /var/lib/mysql-files/transactions_chunks/chunk_
```

---

## Step 3: Import Data into the Staging Table

Use the following script to load data chunks into the staging table:

```bash
for file in /var/lib/mysql-files/transactions_chunks/chunk_*; do
    mysql -u root -p trades_db -e "
    LOAD DATA INFILE '$file'
    INTO TABLE transactions_staging
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"' 
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;";
done
```

---

## Step 4: Migrate Data from Staging to Final Table

Transfer data from the staging table to the final table in batches:

```sql
ALTER TABLE transactions ENGINE=MyISAM;
ALTER TABLE transactions DISABLE KEYS;

SET @batch_size = 10000;
SET @offset = 0; -- Initialize the counter

-- Store total row count in a variable to avoid recalculating
SELECT COUNT(*) INTO @total_rows FROM transactions_load_from_csv;

-- Process data in batches
WHILE @offset < @total_rows DO
    INSERT INTO transactions 
    SELECT * FROM transactions_load_from_csv
    LIMIT @batch_size 
    OFFSET @offset
    SET @offset = @offset + @batch_size -- Increment the counter
END WHILE;

ALTER TABLE transactions ENGINE=InnoDB;
ALTER TABLE transactions ENABLE KEYS;
SET FOREIGN_KEY_CHECKS = 1;
```

---

### Notes

1. Replace `trades_db` with your database name.
2. Update file paths as necessary to match your system.
3. Monitor and adjust batch size as needed for optimal performance.