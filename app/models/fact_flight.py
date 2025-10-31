from sqlalchemy import Column, Integer, Text, Date, UniqueConstraint, ForeignKey, TIMESTAMP
from app.core.database import Base


class FactFlight(Base):
    __tablename__ = "fact_flight"
    __table_args__ = (
        UniqueConstraint("flight_iata", "flight_date", name="uq_flight_iata_flight_date"),
        {"schema": "flight_schema"}
    )

    flight_date = Column(Date, nullable=False)
    flight_status = Column(Text, nullable=True)
    flight_iata = Column(Text, nullable=False)

    airline_id = Column(Integer, ForeignKey("flight_schema.dim_airline.id"), nullable=True)
    departure_airport_id = Column(Integer, ForeignKey("flight_schema.dim_airport.id"), nullable=True)
    departure_airport = Column(Text, nullable=True)
    arrival_airport_id = Column(Integer, ForeignKey("flight_schema.dim_airport.id"), nullable=True)
    arrival_airport = Column(Text, nullable=True)

    departure_delay = Column(Integer, nullable=True)
    departure_scheduled = Column(TIMESTAMP, nullable=True)
    departure_actual = Column(TIMESTAMP, nullable=True)
    arrival_delay = Column(Integer, nullable=True)
    arrival_scheduled = Column(TIMESTAMP, nullable=True)
    arrival_actual = Column(TIMESTAMP, nullable=True)