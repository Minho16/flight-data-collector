from app.repository.dim_airline_repository import DimAirlineRepository
from sqlalchemy.orm import Session


class DimAirlineService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.repo = DimAirlineRepository(self.db)

    def insert_new_airlines(self) -> None:
        """
        Insert new airlines from raw data created today (or target_date)
        """

        return self.repo.insert_new_airlines()
