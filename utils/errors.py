import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leave-manager")

def display_error(name, error):
    logger.exception("err-%s: %s", name, error)

def return_content(name, obj):
    logger.info("return-%s: %s", name, obj)
