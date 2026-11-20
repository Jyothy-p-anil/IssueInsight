
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.core.cache import cache


HOLIDAY_API_URL = (
    "https://calendar-api-d7a8.onrender.com/v1/holidays"
    "?country=IN&year={year}&region=KL&scope=state"
)

CACHE_TIMEOUT = 60 * 60 * 24


def get_kerala_public_holidays(year):
    cache_key = f"kerala_public_holidays_{year}"

    cached_holidays = cache.get(cache_key)
    if cached_holidays is not None:
        return cached_holidays

    url = HOLIDAY_API_URL.format(year=year)

    try:
        with urlopen(url, timeout=5) as response:
            data = json.load(response)

        holidays = data.get("data")

        if not isinstance(holidays, list):
            return []

        holidays = [
            {
                "date": holiday["date"],
                "name": holiday["name"],
            }
            for holiday in holidays
            if (
                isinstance(holiday, dict)
                and isinstance(holiday.get("date"), str)
                and isinstance(holiday.get("name"), str)
                and holiday.get("level") == "state"
            )
        ]

        holidays.sort(key=lambda holiday: holiday["date"])

        cache.set(cache_key, holidays, CACHE_TIMEOUT)

        return holidays

    except (HTTPError, URLError, TimeoutError, ValueError, OSError):
        return []
