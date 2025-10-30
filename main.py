import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.email_notifier import EmailNotificationManager
from app.core.logging import setup_logging
from app.core.task_manager import TaskManager
from app.services.flight_data_service import FlightDataService
from app.core.database import Base, engine

import time


def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    logging.info("Database initialized.")


def run_scheduled_etl():
    flight_data_service = FlightDataService()
    email_manager = EmailNotificationManager()

    task_manager = TaskManager(
        flight_data_service=flight_data_service,
        email_manager=email_manager,
    )

    task_manager.run_daily_flight_etl()


if __name__ == "__main__":
    setup_logging()

    # Initialize the database
    init_db()

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(run_scheduled_etl, trigger="cron", hour=15, minute=0)
    scheduler.start()
    logging.info("Scheduler started. Waiting for daily ETL job at 15:00 UTC...")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")


# if __name__ == "__main__":
#     setup_logging()
#     init_db()
#     run_scheduled_etl()
