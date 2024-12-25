
# Bulk Import of CSV Data into MySQL

This guide outlines the steps to import large CSV data into a MySQL database using a staging table.

---
## Step 0: Create the Original Table

```sql
CREATE TABLE transactions (
    time_stamp TIMESTAMPTZ,  -- PostgreSQL uses TIMESTAMPTZ for timestamp with time zone
    txn_amount NUMERIC(20,8),  -- Use NUMERIC instead of DECIMAL in PostgreSQL (they are essentially the same, but NUMERIC is preferred in PostgreSQL)
    small_description VARCHAR(255),
    accountid BIGINT,
    status VARCHAR(50),
    market_type VARCHAR(50),
    symbol VARCHAR(10),
    quantity NUMERIC(20,8),  -- Use NUMERIC instead of DECIMAL
    symbol_price NUMERIC(20,8),  -- Use NUMERIC instead of DECIMAL
    txn_fee NUMERIC(20,8),  -- Use NUMERIC instead of DECIMAL
    trade_type VARCHAR(10),
    exchangeid INT
);
```


## Disable Indexing and Constraints

```sql
-- Disable foreign key checks (and triggers) to speed up the insert process
ALTER TABLE transactions DISABLE TRIGGER ALL;

-- Disable constraints (if any) to avoid enforcement during import
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS constraint_name;

```

##  PostgreSQL Settings for Optimal Performance

```
-- Disable fsync for faster writes (may risk data loss in the event of a crash)
SET fsync = off;

-- Disable synchronous commit for reduced I/O overhead
SET synchronous_commit = off;

-- Disable full page writes for faster writes
SET full_page_writes = off;

-- Increase maintenance work memory for efficient index creation if necessary later
SET maintenance_work_mem = '4GB';

-- Increase work memory for processing larger chunks of data
SET work_mem = '256MB';

-- Disable auto-commit to speed up the bulk load (handle manually if needed)
SET autocommit = off;

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

## Step 4: Cleanup

```
ALTER TABLE table_name ENABLE TRIGGER ALL;

-- Recreate constraints if they were dropped earlier
ALTER TABLE table_name ADD CONSTRAINT constraint_name;


```