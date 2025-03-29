import requests
from requests.auth import HTTPBasicAuth
import os

sheet_url = "https://api.sheety.co/9b18607244ca748465ed031d81b4cd53/copyOfFlightDealsForPython/prices"
# sheety_credentials if needed (for Basic Auth)
username = os.getenv("username")
password = os.getenv("password")

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._authorization = HTTPBasicAuth()
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheet_url)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_sheety(self):
        for city in self.destination_data:
            body = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            # print(city["id"])
            response = requests.put(url=f"https://api.sheety.co/9b18607244ca748465ed031d81b4cd53"
                                        f"/copyOfFlightDealsForPython/prices/{city['id']}", json=body,
                                        headers={"Content-Type": "application/json"})
