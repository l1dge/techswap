import requests
from configobj import ConfigObj
import sys
from django.conf import settings
import os


config = ConfigObj(r".env")
city = str(sys.argv[1])

API_KEY = config.get("LOCATION_API_KEY")


def retrieve_location(city):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
        + city
        + "&inputtype=textquery&fields=geometry&key="
        + API_KEY
    )

    resp_json_payload = response.json()

    lat = resp_json_payload["candidates"][0]["geometry"]["location"]["lat"]
    long = resp_json_payload["candidates"][0]["geometry"]["location"]["lng"]
    return lat, long


if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = retrieve_location(arg)
