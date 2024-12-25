delete from transactions

CREATE TABLE transactions (
    time_stamp DATETIME(6),
    txn_amount DECIMAL(20,8),
    small_description VARCHAR(255),
    accountid BIGINT,
    status VARCHAR(50),
    market_type VARCHAR(50),
    symbol VARCHAR(10),
    quantity DECIMAL(20,8),
    symbol_price DECIMAL(20,8),
    txn_fee DECIMAL(20,8),
    trade_type VARCHAR(10),
    exchangeid INT
);

