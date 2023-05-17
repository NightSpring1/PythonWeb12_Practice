from multiprocessing import Pool, cpu_count, current_process

import time
import logging
from functools import wraps

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(processName)s %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Function {func.__name__} started')
        start = time.time()
        results = func(*args, **kwargs)
        finish = time.time()
        logger.info(f'Function {func.__name__} executed in {finish - start:.4f} seconds.')
        return results
    return wrapper


def factorize(number):
    logger.debug(f"{factorize.__name__} called. pid={current_process().pid}")
    result = []
    for i in range(1, number+1):
        if not number % i:
            result.append(i)
    return result


@time_it
def sync_calc(data: tuple) -> list:
    results = []
    for num in data:
        results.append(factorize(num))
    return results


@time_it
def async_calc(data: tuple) -> list:
    with Pool(cpu_count()) as pool:
        return pool.map(factorize, data)


if __name__ == "__main__":
    data1 = (300997311, 300997711, 300999111)
    a = sync_calc(data1)
    b = async_calc(data1)
    # logger.info(f"sync_calc result :{a}")
    # logger.info(f"async_calc result :{b}")





