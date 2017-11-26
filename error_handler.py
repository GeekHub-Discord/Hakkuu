import functools
import logging


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(module)s:%(lineno)d: %(message)s')
        sh = logging.StreamHandler()
        fh = logging.FileHandler(f'{name}.log')
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.addHandler(fh)
        #logger.addHandler(gh)
    return logger


def logexcept(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger('auttaja')
        try:
            return await func(*args, **kwargs)
        except:
            logger.exception(f"Exception occured in {func.__name__}")

    return wrapper
