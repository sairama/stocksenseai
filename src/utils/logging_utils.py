import logging


def log_message(level,message):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

    if level=='debug':
        logging.debug(message)
    elif level=='info':
        logging.info(message)
    elif level=='warning':
        logging.warning(message)
    elif level=='error':
        logging.error(message)
    elif level=='critical':
        logging.critical(message)
    else:
        raise ValueError(f"Invalid logging level: {level}")