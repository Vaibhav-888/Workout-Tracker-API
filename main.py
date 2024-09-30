import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os


# Authenticating and POST requests method through Nutritionix API
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = "bb254af6"
API_KEY = "f3355b595d48d56881dd3c7b40954940"

# APP_ID = os.environ["NT_APP_ID"]
# API_KEY = os.environ["NT_API_KEY"]

exercise_text = input("Tell me which exercise you did?: ")

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

nutritionix_payload = {
    "query": exercise_text,
    "weight_kg": 65,
    "gender": "male",
    "age": 25
}

nutritionix_response = requests.post(url=nutritionix_endpoint, headers=nutritionix_headers, json=nutritionix_payload)
nutritionix_data = nutritionix_response.json()
print(nutritionix_data)

# Save data and add a rows to the Google spreadsheet via "Sheety API"

sheety_endpoint = "https://api.sheety.co/c8cfb98808f497d90d5026ddb4cb54fa/copyOfMyWorkouts/sheet1"
# sheety_endpoint = os.environ["SHEETY_ENDPOINT"]

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in nutritionix_data["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"],
            }
        }
    }

# Authenticating Sheety API
USERNAME = "vaibhavi1"
PASSWORD = "Sheety@123"

AUTH_TOKEN = "Bearer dmFpYmhhdmkxOlNoZWV0eUAxMjMi="

sheety_auth_headers = {
    "Authorization": AUTH_TOKEN
}

sheety_response = requests.post(
    url=sheety_endpoint,
    json=sheet_inputs,
    headers=sheety_auth_headers,
)
print(sheety_response.text)
