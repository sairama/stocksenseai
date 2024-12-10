import logging


def log_message(level,message):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

    if level=='debug':
        logging.debug(message)
    if level=='info':
        logging.info(message)
    if level=='warning':
        logging.warning(message)
    if level=='error':
        logging.error(message)
    if level=='critical':
        logging.critical(message)
    else:
        raise ValueError(f"Invalid logging level: {level}")