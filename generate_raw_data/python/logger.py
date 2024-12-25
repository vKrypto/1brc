import logging
import builtins
import time
from functools import wraps


# Create logger
logger = logging.getLogger("trade_logger")
logger.setLevel(logging.INFO)  # Set the logging level

# Create a file handler
file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log a message
logger.info("started.....")


original_print = builtins.print

def custom_print(*args, **kwargs):
    message = " ".join(map(str, args))  # Combine all args into a single string
    logger.info(message)  # Log the message

builtins.print = custom_print



def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record end time
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper

def async_timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        result = await func(*args, **kwargs)  # Execute the async function
        end_time = time.time()  # Record end time
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper