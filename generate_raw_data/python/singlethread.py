import csv
from logger import *
from faker import Faker
import random
import os
import time


fake = Faker()

def random_float(min_value, max_value, decimal_places):
    value = random.uniform(min_value, max_value)
    return round(value, decimal_places)

def generate_random_transaction():
    return {
        "timestamp": fake.date_time_this_year().isoformat(), 
        "txn_amount": random_float(-10000, 10000, 8), 
        "small_description": fake.text(max_nb_chars=55).replace("\n", " "), 
        "accountid": str(fake.random_int(1000000000, 9999999999)), 
        "status": random.choice(["failed", "success", "pending"]), 
        "market_type": random.choice(["SPOT", "FUTURES", "MARGIN"]), 
        "symbol": fake.lexify("???").upper(), 
        "quantity": random_float(0.01, 1000, 8), 
        "symbol_price": random_float(0.01, 100000, 8), 
        "txn_fee": random_float(0.01, 50, 8), 
        "trade_type": random.choice(["BUY", "SELL"]), 
        "exchangeid": fake.random_int(1, 100), 
    }


def write_to_csv(file_name, data):
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if not file_exists:
            writer.writeheader() 
        writer.writerows(data)

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
TOTAL_ROWS = 500_000  # 1 billion rows
CHUNK_SIZE = 50_000


generate_transactions(OUTPUT_FILE, TOTAL_ROWS, CHUNK_SIZE)
