import logging

level = logging.DEBUG

def custom_logger(name):
    #fomattingter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    fomattingter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - %(lineno)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(fomattingter)

    logger = logging.getLogger(name)

    logger.addHandler(handler)
    global level
    print(level)
    logger.setLevel(level)

    return logger
