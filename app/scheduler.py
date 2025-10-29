import math

from app.api_client import fetch_flights
from app.repository import save_flights
from app.database import SessionLocal

def run_collector():
    db = SessionLocal()

    try:
        for airport_type, iata in [("departure", "ICN"), ("arrival", "ICN")]:
            print(f"Fetching flights for {airport_type} airport: {iata}")
            offset = 0
            limit = 100

            # Fetch first page
            first_page = fetch_flights(offset=offset, limit=limit,
                                       dep_iata=iata if airport_type == "departure" else None,
                                       arr_iata=iata if airport_type == "arrival" else None)
            total = first_page["pagination"]["total"]
            save_flights(db, first_page["data"])
            print(f"Fetched and saved {len(first_page['data'])}/{total} for {airport_type} {iata}")

            # Fetch remaining pages
            total_pages = math.ceil(total / limit)
            for page in range(1, total_pages):
                offset = page * limit
                data = fetch_flights(offset=offset, limit=limit,
                                     dep_iata=iata if airport_type == "departure" else None,
                                     arr_iata=iata if airport_type == "arrival" else None)
                save_flights(db, data["data"])
                print(f"Fetched and saved {offset + len(data['data'])}/{total} for {airport_type} {iata}")

    finally:
        db.close()