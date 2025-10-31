from sqlalchemy.orm import Session
from sqlalchemy import text

class FactFlightRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_fact_flights(self):
        sql = text("""
            INSERT INTO flight_schema.fact_flight (
                flight_date,
                flight_status,
                flight_iata,
                airline_id,
                departure_airport_id,
                departure_airport,
                arrival_airport_id,
                arrival_airport,
                departure_delay,
                departure_scheduled,
                departure_actual,
                arrival_delay,
                arrival_scheduled,
                arrival_actual
            )
            SELECT 
                DATE_TRUNC('DAY', r.flight_date) AS flight_date, 
                r.flight_status, 
                r.flight_iata,
                a.id AS airline_id,
                da.id AS departure_airport_id,
                r.departure_iata AS departure_airport,
                da2.id AS arrival_airport_id,
                r.arrival_iata AS arrival_airport,
                r.departure_delay,
                r.departure_scheduled,
                r.departure_actual,
                r.arrival_delay,
                r.arrival_scheduled,
                r.arrival_actual
            FROM flight_schema.raw_flight_data r
            JOIN flight_schema.dim_airport da
                ON r.departure_iata = da.iata_code
            JOIN flight_schema.dim_airport da2
                ON r.arrival_iata = da2.iata_code
            JOIN flight_schema.dim_airline a
                ON r.airline_iata = a.iata_code
            WHERE DATE_TRUNC('DAY', r.created_at) = CURRENT_DATE
            ON CONFLICT (flight_iata, flight_date) DO NOTHING;
        """)
        self.db.execute(sql)
        self.db.commit()
