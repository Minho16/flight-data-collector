from sqlalchemy.orm import Session
from sqlalchemy import text

class DimAirportRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_new_airports(self):
        sql = text("""
            WITH airport_data AS (
                SELECT departure_airport AS airport,
                       departure_timezone AS timezone,
                       departure_iata AS iata_code,
                       departure_icao AS icao_code
                FROM flight_schema.raw_flight_data
                WHERE DATE_TRUNC('DAY', created_at) = CURRENT_DATE
                GROUP BY 1,2,3,4
                UNION ALL
                SELECT arrival_airport AS airport,
                       arrival_timezone AS timezone,
                       arrival_iata AS iata_code,
                       arrival_icao AS icao_code
                FROM flight_schema.raw_flight_data
                WHERE DATE_TRUNC('DAY', created_at) = CURRENT_DATE
                GROUP BY 1,2,3,4
            )
            INSERT INTO flight_schema.dim_airport (airport, timezone, iata_code, icao_code)
            SELECT DISTINCT airport, timezone, iata_code, icao_code
            FROM airport_data
            WHERE iata_code IS NOT NULL
            ON CONFLICT (iata_code, icao_code) DO NOTHING;
        """)
        self.db.execute(sql)
        self.db.commit()
