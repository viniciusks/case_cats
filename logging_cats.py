import logging

def logging_cats(type_log, msg):
    log_console = logging

    # log_console.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
    log_console.basicConfig(filename='logs/api_cats.log', filemode='w', format='%(asctime)s:%(levelname)s:%(name)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')

    if type_log == 1:
        log_console.info(msg)
    elif type_log == 2:
        log_console.warning(msg)
    elif type_log == 3:
        log_console.error(msg)
    elif type_log == 4:
        log_console.critical(msg)