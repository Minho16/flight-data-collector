from app.repository.dim_airport_repository import DimAirportRepository
from sqlalchemy.orm import Session


class DimAirportService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.repo = DimAirportRepository(self.db)

    def insert_new_airports(self) -> None:
        """
        Insert new airports from raw data created today
        """

        return self.repo.insert_new_airports()
