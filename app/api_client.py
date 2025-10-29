import requests
from app.config import settings

def fetch_flights(offset: int = 0, limit: int = 100, dep_iata: str = None, arr_iata: str = None):
    params = {
        "access_key": settings.API_KEY,
        "limit": limit,
        "offset": offset,
    }

    if dep_iata:
        params["dep_iata"] = dep_iata
    if arr_iata:
        params["arr_iata"] = arr_iata

    response = requests.get(settings.API_URL, params=params)
    response.raise_for_status()
    return response.json()
