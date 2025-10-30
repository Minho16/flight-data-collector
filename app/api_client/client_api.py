from abc import ABC

import requests
from app.core.config import settings


class FlightDataCollector(ABC):
    def __init__(self, departure_airport_code):
        self.offset = 0
        self.limit = 100
        self.departure_airport_code = departure_airport_code
        self.api_url = None
        self.api_key = None

    def fetch_flights(self):
        params = {
            "access_key": self.api_key,
            "limit": self.limit,
            "offset": self.offset,
            "dep_iata": self.departure_airport_code,
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        return response.json()


class AviationStackFlightDataCollector(FlightDataCollector):
    def __init__(self, departure_airport_code):
        super().__init__(departure_airport_code)
        self.offset = 0
        self.limit = 100
        self.api_url = settings.AVIATION_STACK_API_URL
        self.api_key = settings.AVIATION_STACK_API_KEY
