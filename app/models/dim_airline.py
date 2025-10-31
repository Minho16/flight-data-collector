from datetime import datetime

from sqlalchemy import Column, Integer, Text, TIMESTAMP
from app.core.database import Base


class DimAirline(Base):
    __tablename__ = "dim_airline"
    __table_args__ = {"schema": "flight_schema"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    airline_name = Column(Text, nullable=True)
    iata_code = Column(Text, nullable=True)
    icao_code = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)