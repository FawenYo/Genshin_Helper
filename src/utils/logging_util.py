import logging
import os

# Set outside from the function to prevent re-initialization
IS_INITIALIZED = False


def get_logger() -> logging.Logger:
    global IS_INITIALIZED
    new_logger = logging.getLogger()

    # If the logger has been initialized, return the logger
    if IS_INITIALIZED:
        return new_logger

    log_level = os.environ.get("logLevel", default="DEBUG").upper()

    logging.basicConfig(level=log_level)

    # Set third party modules' logging level
    for module_name in ["urllib3"]:
        module_logger = logging.getLogger(module_name)
        # Only log warning and above
        module_logger.setLevel(logging.WARNING)
        module_logger.propagate = True

    # Set the logger to initialized
    IS_INITIALIZED = True

    return new_logger
