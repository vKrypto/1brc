import logging
import builtins

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

def custom_print(*args):
    message = " ".join(map(str, args))  # Combine all args into a single string
    logger.info(message)  # Log the message

builtins.print = custom_print
