import logging


def init_logger(path='core.log'):
    logger = logging.getLogger(name='core_logger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
    )
    filehandler = logging.FileHandler(path)
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


class Logger(logging.LoggerAdapter):
    def __init__(self, name: str, extra: None = None):
        super().__init__(logging.getLogger(name), extra or {})

    def log(self, level, msg: str, *args, **kwargs):
        if self.isEnabledFor(level):
            self.logger._log(level, msg.format(*args, **kwargs), ())
