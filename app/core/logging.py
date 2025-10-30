import logging
import os


def setup_logging():
    """
    Configure application logging.
    - Logs to console only (stdout)
    - Includes timestamps, log levels, and module names
    - Respects LOG_LEVEL env variable
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    log_format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Clear any existing handlers (useful in tests or notebooks)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure basic logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler()],
    )

    # Reduce noise from external libraries
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logging.info("✅ Logging initialized (console only)")
