import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.email_notifier import EmailNotificationManager
from app.core.logging import setup_logging
from app.core.task_manager import TaskManager
from app.services.dim_airline_service import DimAirlineService
from app.services.dim_airport_service import DimAirportService
from app.services.fact_flight_service import FactFlightService
from app.services.raw_flight_data_service import RawFlightDataService
from app.core.database import Base, engine, SessionLocal

import time

db = SessionLocal()



def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    logging.info("Database initialized.")


def run_scheduled_etl():
    email_manager = EmailNotificationManager()
    raw_flight_data_service = RawFlightDataService(db)
    airport_service = DimAirportService(db)
    airline_service = DimAirlineService(db)
    fact_service = FactFlightService(db)

    task_manager = TaskManager(
        email_manager=email_manager,
        raw_flight_data_service=raw_flight_data_service,
        dim_airport_service=airport_service,
        dim_airline_service=airline_service,
        fact_flight_service=fact_service,
    )

    task_manager.run_daily_flight_etl()


if __name__ == "__main__":
    setup_logging()

    # Initialize the database
    init_db()

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(run_scheduled_etl, trigger="cron", hour=22, minute=45)
    scheduler.start()
    logging.info("Scheduler started. Waiting for daily ETL job at 22:45 UTC...")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")
#
#
# if __name__ == "__main__":
#     setup_logging()
#     init_db()
#     run_scheduled_etl()
