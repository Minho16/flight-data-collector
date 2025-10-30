import logging


class TaskManager:
    """Handles scheduled ETL orchestration and notifications."""

    def __init__(self, flight_data_service, email_manager):
        self.flight_data_service = flight_data_service
        self.email_manager = email_manager
        self.logger = logging.getLogger(__name__)

    def run_daily_flight_etl(self):
        """Run daily flight ETL tasks and send notifications."""
        try:
            self.logger.info("🚀 Starting daily flight ETL job...")

            # Step 1. Ingest new data
            self.flight_data_service.ingest_flight_data()
            self.logger.info("✅ Ingestion completed successfully.")

            # Step 2. Clean up outdated data
            self.flight_data_service.delete_outdated_data()
            self.logger.info("🧹 Outdated data cleanup done.")

            # Step 3. Notify success
            subject = "✅ Flight Data Job Success"
            body = "The scheduled ETL job finished successfully."
            self.email_manager.send_email(subject, body)

            self.logger.info("📧 Success email sent.")
            self.logger.info("🎯 Flight ETL job completed successfully.")

        except Exception as e:
            # Log and notify on failure
            self.logger.exception("❌ Flight ETL job failed.")
            subject = "❌ Flight Data Job Failed"
            body = f"The scheduled ETL job failed with error:\n\n{e}"
            self.email_manager.send_email(subject, body)
            raise
