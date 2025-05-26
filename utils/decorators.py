import time
from functools import wraps
from logger import logger

def log_command(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}, kwargs: {kwargs}")
        return await func(*args, **kwargs)
    return wrapper

def time_command(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Command {func.__name__} executed in {duration:.2f} seconds")
        return result
    return wrapper