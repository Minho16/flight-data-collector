from sqlalchemy import Column, Integer, String, DateTime, Date
from app.database import Base

class FlightRaw(Base):
    __tablename__ = "raw_flight_data"
    __table_args__ = {"schema": "flight_schema"}

    id = Column(Integer, primary_key=True)

    flight_date = Column(Date)
    flight_status = Column(String)

    departure_airport = Column(String)
    departure_timezone = Column(String)
    departure_iata = Column(String)
    departure_icao = Column(String)
    departure_terminal = Column(String)
    departure_gate = Column(String)
    departure_delay = Column(Integer)
    departure_scheduled = Column(DateTime)
    departure_estimated = Column(DateTime)
    departure_actual = Column(DateTime)
    departure_estimated_runway = Column(String)
    departure_actual_runway = Column(String)

    arrival_airport = Column(String)
    arrival_timezone = Column(String)
    arrival_iata = Column(String)
    arrival_icao = Column(String)
    arrival_terminal = Column(String)
    arrival_gate = Column(String)
    arrival_delay = Column(Integer)
    arrival_scheduled = Column(DateTime)
    arrival_estimated = Column(DateTime)
    arrival_actual = Column(DateTime)
    arrival_estimated_runway = Column(String)
    arrival_actual_runway = Column(String)
    arrival_baggage = Column(String)

    airline_name = Column(String)
    airline_iata = Column(String)
    airline_icao = Column(String)

    flight_number = Column(String)
    flight_iata = Column(String)
    flight_icao = Column(String)

    aircraft_registration = Column(String)
    aircraft_iata = Column(String)
    aircraft_icao = Column(String)
    aircraft_icao24 = Column(String)

    created_at = Column(DateTime)
