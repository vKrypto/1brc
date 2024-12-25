# Bulk Import of CSV Data into MySQL

This guide outlines the steps to import large CSV data into a MySQL database using a staging table.
DEMO: 100 MIL rows
CSV file size: 24 GB
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

## Step 1: Create the Staging Table

```sql
CREATE UNLOGGED TABLE transactions_stagging (
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

---

## Step 2: Pre-process the CSV File

Split the CSV file into manageable chunks for processing:

ON LINUX:
```bash
mkdir -p /var/lib/mysql-files/transactions_chunks
split -l 1000000 /var/lib/mysql-files/100_mil_transactions.csv /var/lib/mysql-files/transactions_chunks/chunk_
```
ON WINDOWS:
```BASH
$filePath = "F:\export.csv"
$chunkSize = 1000000  

$counter = 1
Get-Content $filePath | 
ForEach-Object -Begin { 
    $chunk = @() 
    Write-Host "Starting processing file..."
} -Process {
    $chunk += $_
    
    if ($chunk.Count -ge $chunkSize) {
        $chunk | Set-Content "F:\temp\chunk$counter.csv"
        Write-Host "Created chunk$counter.csv with $($chunk.Count) lines"
        $counter++
        $chunk.Clear()
    }
} -End {
    if ($chunk.Count -gt 0) {
        $chunk | Set-Content "F:\temp\chunk$counter.csv"
        Write-Host "Created chunk$counter.csv with remaining lines ($($chunk.Count))"
    }
    Write-Host "Processing complete."
}

# Hold the screen at the end
Pause

```


---

## step 3: Tweak Postgres for better performance

```sql
-- Disable foreign key checks (and triggers) to speed up the insert process
ALTER TABLE transactions DISABLE TRIGGER ALL;

-- Disable constraints (if any) to avoid enforcement during import
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS constraint_name;

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

## Step 3: Import Data into the Staging Table

Use the following script to load data chunks into the staging table:

### 1:  /copy with bulk_file.csv, no optimization : 588 sec
### 2: / copy with chunks no optimization: 
### 3: / copy with chunks with optimization: 

```bash
#!/bin/bash

PGHOST="localhost"
PGUSER="your_username"
PGDATABASE="your_database"

for file in temp/*.csv; do
  psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -c "\COPY transactions_stagging FROM '$file' WITH (FORMAT csv);" &
done

wait
```

---

## Step 4: Migrate Data from Staging to Final Table

Transfer data from the staging table to the final table in batches:

```sql
DO $$ 
DECLARE
    batch_size INT := 10000;
    cur_ptr INT := 0;
    total_rows INT;
BEGIN
    -- Get the total number of rows in the source table
    SELECT COUNT(*) INTO total_rows FROM transactions_stagging;

    -- Process data in batches
    WHILE cur_ptr < total_rows LOOP
        -- Insert data in batches
        INSERT INTO transactions
        SELECT * FROM transactions_stagging
        LIMIT batch_size OFFSET cur_ptr;

        -- Increment the offset for the next batch
        cur_ptr := cur_ptr + batch_size;
    END LOOP;
END $$;
```
### 1: with optimization : took x sec 
### 1: without optimization : took x sec 

---

### Notes

1. Replace `trades_db` with your database name.
2. Update file paths as necessary to match your system.
3. Monitor and adjust batch size as needed for optimal performance.
