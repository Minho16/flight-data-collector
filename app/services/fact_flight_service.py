from app.repository.fact_flight_repository import FactFlightRepository
from sqlalchemy.orm import Session
from datetime import date


class FactFlightService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.repo = FactFlightRepository(self.db)

    def insert_fact_flights(self, target_date: date = None) -> None:
        """
        Insert new fact flights
        """
        return self.repo.insert_fact_flights()
