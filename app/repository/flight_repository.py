import logging

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.flight_data import FlightRawData

RETENTION_DAYS = 365


def save_flights(db: Session, flights: list[dict]) -> None:
    """
    Persist a batch of flights using bulk_save_objects for performance.
    Expects flights as list of dicts mapped from the API.
    """

    records = []

    for flight_data in flights:
        dep = flight_data.get("departure") or {}
        arr = flight_data.get("arrival") or {}
        airline = flight_data.get("airline") or {}
        flight = flight_data.get("flight") or {}
        aircraft = flight_data.get("aircraft") or {}

        record = FlightRawData(
            flight_date=flight_data.get("flight_date"),
            flight_status=flight_data.get("flight_status"),
            departure_airport=dep.get("airport"),
            departure_timezone=dep.get("timezone"),
            departure_iata=dep.get("iata"),
            departure_icao=dep.get("icao"),
            departure_terminal=dep.get("terminal"),
            departure_gate=dep.get("gate"),
            departure_delay=dep.get("delay"),
            departure_scheduled=dep.get("scheduled"),
            departure_estimated=dep.get("estimated"),
            departure_actual=dep.get("actual"),
            departure_estimated_runway=dep.get("estimated_runway"),
            departure_actual_runway=dep.get("actual_runway"),
            arrival_airport=arr.get("airport"),
            arrival_timezone=arr.get("timezone"),
            arrival_iata=arr.get("iata"),
            arrival_icao=arr.get("icao"),
            arrival_terminal=arr.get("terminal"),
            arrival_gate=arr.get("gate"),
            arrival_delay=arr.get("delay"),
            arrival_scheduled=arr.get("scheduled"),
            arrival_estimated=arr.get("estimated"),
            arrival_actual=arr.get("actual"),
            arrival_estimated_runway=arr.get("estimated_runway"),
            arrival_actual_runway=arr.get("actual_runway"),
            arrival_baggage=arr.get("baggage"),
            airline_name=airline.get("name"),
            airline_iata=airline.get("iata"),
            airline_icao=airline.get("icao"),
            flight_number=flight.get("number"),
            flight_iata=flight.get("iata"),
            flight_icao=flight.get("icao"),
            aircraft_registration=aircraft.get("registration"),
            aircraft_iata=aircraft.get("iata"),
            aircraft_icao=aircraft.get("icao"),
            aircraft_icao24=aircraft.get("icao24"),
            created_at=datetime.utcnow(),
        )
        records.append(record)

    if not records:
        logging.info("No flights data to save.")
        return

    try:
        db.bulk_save_objects(records)
        db.commit()

    except Exception as e:
        logging.error(e)
        db.rollback()


def delete_old_flights(db: Session) -> None:
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
    db.query(FlightRawData).filter(FlightRawData.flight_date < cutoff.date()).delete()
    db.commit()
