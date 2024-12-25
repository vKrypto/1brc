import csv
from logger import *
import random
import os
import time
from random import uniform, choice, randint
from datetime import datetime, timedelta

# Pre-generate pools of random data to minimize calls to Faker and random functions
SYMBOL_POOL = ["BTC", "ETH", "XRP", "LTC", "ADA"]
STATUS_POOL = ["failed", "success", "pending"]
MARKET_TYPE_POOL = ["SPOT", "FUTURES", "MARGIN"]
TRADE_TYPE_POOL = ["BUY", "SELL"]
EXCHANGE_ID_POOL = [i for i in range(1, 101)]

# Generate a random date within the current year
START_DATE = datetime.now() - timedelta(days=365)
END_DATE = datetime.now()


def random_float(min_value, max_value, decimal_places):
    value = random.uniform(min_value, max_value)
    return round(value, decimal_places)

def random_date(start, end):
    delta = end - start
    random_days = randint(0, delta.days)
    random_seconds = randint(0, 86400)
    return (start + timedelta(days=random_days, seconds=random_seconds)).isoformat()

def random_text(max_length):
    return " ".join(f"word{i}" for i in range(randint(1, max_length // 5)))


def generate_random_transaction():
    return {
        "timestamp": random_date(START_DATE, END_DATE), 
        "txn_amount": round(uniform(-10000, 10000), 8),
        "small_description": random_text(11),  # Assuming ~5 chars per word + spaces
        "accountid": str(randint(1000000000, 9999999999)),
        "status": choice(STATUS_POOL),
        "market_type": choice(MARKET_TYPE_POOL),
        "symbol": choice(SYMBOL_POOL),
        "quantity": round(uniform(0.01, 1000), 8),
        "symbol_price": round(uniform(0.01, 100000), 8),
        "txn_fee": round(uniform(0.01, 50), 8),
        "trade_type": choice(TRADE_TYPE_POOL),
        "exchangeid": choice(EXCHANGE_ID_POOL),
    }

@timeit
def write_to_csv(file_name, data):
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if not file_exists:
            writer.writeheader() 
        writer.writerows(data)

@timeit
def generate_transactions(file_name, total_rows, chunk_size):
    rows_generated = 0
    buffer = []
    start_time = time.time()

    while rows_generated < total_rows:
        buffer.append(generate_random_transaction())
        rows_generated += 1

        if rows_generated % chunk_size == 0:
            write_to_csv(file_name, buffer)
            print(f"{len(buffer)}({round(rows_generated/total_rows*100, 2)}%) rows written to {file_name}, time elapsed: {round(time.time() - start_time, 2)} sec")
            buffer = [] 

    if buffer:
        write_to_csv(file_name, buffer)
        print(f"Final {len(buffer)} rows written to {file_name}")

OUTPUT_FILE = "transactions.csv"
TOTAL_ROWS = 100_000  # 1 billion rows
CHUNK_SIZE = 50_000


generate_transactions(OUTPUT_FILE, TOTAL_ROWS, CHUNK_SIZE)
