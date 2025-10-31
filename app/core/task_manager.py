import logging

class TaskManager:
    """Handles scheduled ETL orchestration and notifications."""

    def __init__(self, email_manager, raw_flight_data_service, dim_airport_service, dim_airline_service, fact_flight_service):
        self.raw_flight_data_service = raw_flight_data_service
        self.dim_airport_service = dim_airport_service
        self.dim_airline_service = dim_airline_service
        self.fact_flight_service = fact_flight_service
        self.email_manager = email_manager
        self.logger = logging.getLogger(__name__)

    def run_daily_flight_etl(self):
        """Run daily flight ETL tasks and send notifications."""
        try:
            self.logger.info("🚀 Starting daily flight ETL job...")

            # Step 1. Ingest new data
            self.raw_flight_data_service.ingest_flight_data()
            self.logger.info("✅ Ingestion completed successfully.")

            # Step 2. Clean up outdated data
            self.raw_flight_data_service.delete_outdated_data()
            self.logger.info("🧹 Outdated data cleanup done.")

            # Step 3. Populate fact and dimension tables.
            self.dim_airport_service.insert_new_airports()
            self.logger.info("✅ Ingestion dim_airport completed successfully.")

            self.dim_airline_service.insert_new_airlines()
            self.logger.info("✅ Ingestion dim_airline completed successfully.")

            self.fact_flight_service.insert_fact_flights()
            self.logger.info("✅ Ingestion fact_flight completed successfully.")

            # Step 4. Notify success
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
