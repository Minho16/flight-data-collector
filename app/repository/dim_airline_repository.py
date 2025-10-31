from sqlalchemy.orm import Session
from sqlalchemy import text

class DimAirlineRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_new_airlines(self):
        sql = text("""
            INSERT INTO flight_schema.dim_airline (airline_name, iata_code, icao_code)
            SELECT DISTINCT airline_name, airline_iata, airline_icao
            FROM flight_schema.raw_flight_data
            WHERE DATE_TRUNC('DAY', created_at) = CURRENT_DATE
              AND airline_iata IS NOT NULL
            ON CONFLICT (iata_code, icao_code) DO NOTHING;
        """)
        self.db.execute(sql)
        self.db.commit()
