from logger import *
import random
import time
from random import uniform, choice, randint
from datetime import datetime, timedelta

import asyncio
import aiofiles


COLS = [
        "timestamp",
        "txn_amount",
        "small_description",
        "accountid",
        "status",
        "market_type",
        "symbol",
        "quantity",
        "symbol_price",
        "txn_fee",
        "trade_type",
        "exchangeid",
]



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
    """
    schema reflects: COLS
    """
    return (
        random_date(START_DATE, END_DATE), 
        round(uniform(-10000, 10000), 8),
        random_text(11),  # Assuming ~5 chars per word + spaces
        str(randint(1000000000, 9999999999)),
        choice(STATUS_POOL),
        choice(MARKET_TYPE_POOL),
        choice(SYMBOL_POOL),
        round(uniform(0.01, 1000), 8),
        round(uniform(0.01, 100000), 8),
        round(uniform(0.01, 50), 8),
        choice(TRADE_TYPE_POOL),
        choice(EXCHANGE_ID_POOL),
    )

@async_timeit
async def writer_to_file_task(file_name, queue):
    async with aiofiles.open(file_name, mode="a") as file:
        await file.write(",".join(COLS) + "\n")
        while True:
            batch = await queue.get()
            if batch is None:  # Signal to exit
                break
            chunk = "\n".join([",".join(map(str, row)) for row in batch]) + "\n"
            await file.write(chunk)
            print("writing to file")
            queue.task_done()
            await asyncio.sleep(0) 

@async_timeit
async def generate_transactions(queue, total_rows, chunk_size):
    rows_generated = 0
    buffer = []
    start_time = time.time()
    while rows_generated < total_rows:
        buffer.append(generate_random_transaction())
        rows_generated += 1

        if len(buffer) >= chunk_size:
            await queue.put(buffer)
            print(f"{len(buffer)}({round(rows_generated/total_rows*100, 2)}%) rows pushed to write, time elapsed: {round(time.time() - start_time, 2)} sec")
            buffer = []

    if buffer:
        await queue.put(buffer)
    await queue.put(None)

@async_timeit
async def main():
    OUTPUT_FILE = "transactions.csv"
    TOTAL_ROWS = 1_000_000  # 1 billion rows
    CHUNK_SIZE = 100_000

    queue = asyncio.Queue(maxsize=1)  # shared memory along asyncio task
    
    writer_task = asyncio.create_task(writer_to_file_task(OUTPUT_FILE, queue))
    generate_task = asyncio.create_task(generate_transactions(queue, TOTAL_ROWS, CHUNK_SIZE))
    
    await asyncio.gather(
        writer_task, 
        generate_task,
    )

asyncio.run(main())