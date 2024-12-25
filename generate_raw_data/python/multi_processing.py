from logger import *  
import random  
import time  
from random import uniform, choice, randint  
from datetime import datetime, timedelta  
import multiprocessing  
import asyncio  
import aiofiles  
import pytz
import os


timezone = pytz.timezone('Asia/Kolkata')


COLS = [  
    "time_stamp",  
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
    random_date = start + timedelta(days=random_days, seconds=random_seconds)  
    # return (start + timedelta(days=random_days, seconds=random_seconds)).isoformat()  
    # return utc.localize(random_date.strftime('%Y-%m-%d %H:%M:%S.%f')
    return timezone.localize(random_date)

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
        while True:  
            batch = await queue.get()  
            if batch is None:  # Signal to exit  
                break  
            chunk = "\n".join([",".join(map(str, row)) for row in batch]) + "\n"  
            await file.write(chunk)  
            queue.task_done()  
            await asyncio.sleep(0)  

@async_timeit  
async def generate_transactions(queue, total_rows, chunk_size):  
    rows_generated = 0  
    buffer = []  
    start_time = time.time()  
    while rows_generated < total_rows: 
        data = generate_random_transaction() 
        if not all(data) and len(data) == 12:
            continue
        buffer.append(data)  
        rows_generated += 1  

        if len(buffer) >= chunk_size:  
            await queue.put(buffer)  
            print(f"{len(buffer)}({round(rows_generated/total_rows*100, 2)}%) rows pushed to write, time elapsed: {round(time.time() - start_time, 2)} sec")  
            buffer = []  

    if buffer:  
        await queue.put(buffer)  
    await queue.put(None)  

def main(total_rows, chunk_size, output_file):  
    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)  

    queue = asyncio.Queue(maxsize=1)  

    writer_task = loop.create_task(writer_to_file_task(output_file, queue))  
    generate_task = loop.create_task(generate_transactions(queue, total_rows, chunk_size))  

    loop.run_until_complete(asyncio.gather(writer_task, generate_task))  
    loop.close()  

def run_in_chunks(total_rows, chunk_size, output_file, num_chunks, write_header=True):  
    chunk_rows = total_rows // num_chunks  
    processes = []  
    with open(output_file, mode="w") as file:  
        if write_header:
            file.write(",".join(COLS) + "\n")  
        else:
            file.write("")
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    for i in range(num_chunks):  
        process = multiprocessing.Process(target=main, args=(chunk_rows, chunk_size, f"{temp_dir}/chunk_{i+1}.csv" ))  
        process.start()  
        processes.append(process)  

    for process in processes:  
        process.join()  
    
    print("mergin csv data")
    # combine all chunks into bunch csv
    merge_chunks(temp_dir, output_file)


def merge_chunks(chunk_dir, output_file):
    # Get all CSV files in the folder
    csv_files = [file for file in os.listdir(chunk_dir) if file.endswith('.csv')]

    with open(output_file, mode="w") as outfile:
        for file_name in csv_files:
            file_path = os.path.join(chunk_dir, file_name)
            with open(file_path, mode="r") as infile:
                outfile.write(infile.read())
            os.remove(file_path)
    print(f"Merged {len(csv_files)} CSV files into {output_file}")

if __name__ == "__main__":  
    OUTPUT_FILE = "transactions.csv"  
    TOTAL_ROWS = 100_000_000  # 1 million rows  
    CHUNK_SIZE = 1_000_000  
    workers = multiprocessing.cpu_count()  # Divide the work into 10 chunks  
    print(f"starting with {workers}")
    run_in_chunks(TOTAL_ROWS, CHUNK_SIZE, OUTPUT_FILE, workers, write_header=True)
