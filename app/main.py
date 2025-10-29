from app.scheduler import run_collector
from app.database import Base, engine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

def job():
    """Job to run the collector."""
    print(f"[{datetime.utcnow()} UTC] Running flight data collector...")
    run_collector()
    print(f"[{datetime.utcnow()} UTC] Collector finished.")

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Start the scheduler
    scheduler = BackgroundScheduler(timezone="UTC")
    # Schedule daily at 23:00 UTC
    scheduler.add_job(job, trigger='cron', hour=23, minute=0)
    scheduler.start()
    print("Scheduler started. Waiting for daily job at 23:00 UTC...")

    try:
        # Keep the script running so scheduler can trigger
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")
