import logging
import math

from app.api_client.client_api import AviationStackFlightDataCollector
from app.repository.flight_repository import save_flights, delete_old_flights
from app.core.database import SessionLocal

DEPARTURE_AIRPORT_CODE = "ICN"


class FlightDataService:
    def __init__(self):
        self._db = SessionLocal()

    def ingest_flight_data(self) -> None:
        try:
            logging.info(f"Fetching departure flights of {DEPARTURE_AIRPORT_CODE} airport")

            # Fetch first page
            data_collector = AviationStackFlightDataCollector(
                departure_airport_code=DEPARTURE_AIRPORT_CODE
            )

            first_page = data_collector.fetch_flights()
            total = first_page["pagination"]["total"]
            save_flights(self._db, first_page["data"])

            logging.info(f"Fetched and saved {len(first_page['data'])}/{total} departure flights of {DEPARTURE_AIRPORT_CODE} airport")


            # Fetch remaining pages
            total_pages = math.ceil(total / data_collector.limit)
            for page in range(1, total_pages):
                data_collector.offset = page * data_collector.limit
                data = data_collector.fetch_flights()
                save_flights(self._db, data["data"])

                logging.info(f"Fetched and saved {data_collector.offset + len(data['data'])}/{total} departure flights of {DEPARTURE_AIRPORT_CODE} airport")

        finally:
            self._db.close()

    def delete_outdated_data(self) -> None:
        try:
            delete_old_flights(db=self._db)
        finally:
            self._db.close()
