import logging


def init_logger():

    global logger

    logger = logging.getLogger(name='core_logger')

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
    )
    filehandler = logging.FileHandler('logs/core.log')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(filehandler)

    return logger


def log_encode(name):
    return str(str(name).encode('utf-8'), 'utf-8')
