import requests
from datetime import datetime
import os


API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
flight_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
POST_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
CITY_CODE_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"


class FlightSearch:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        response = requests.post(
            url=POST_ENDPOINT,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials",
                  "client_id": API_KEY,
                  "client_secret": API_KEY_SECRET}
        )
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return None
        return response.json().get("access_token", None)

    def get_city_code(self, city_name):
        city_search_params = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS",
        }
        response = requests.get(url=CITY_CODE_ENDPOINT, headers={"Authorization": "Bearer " + self.token},
                                params=city_search_params)

        # print(f"Status code {self.response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=flight_endpoint,
            headers=headers,
            params=query,
        )


        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()