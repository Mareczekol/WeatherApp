import requests
import json
from datetime import datetime, timedelta
import os


def get_weather_forecast(latitude, longitude, date):
    # Format the date
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

    # Build the API URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&" \
          f"longitude={longitude}&hourly=rain&daily=rain_sum&timezone=" \
          f"Europe%2FLondon&start_date={formatted_date}&end_date=" \
          f"{formatted_date}"

    # Send the HTTP GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract the rainfall value from the response
        rainfall = data["daily"]["rain_sum"][0]

        # Determine the weather condition based on the rainfall value
        if rainfall > 0.0:
            return "Będzie padać"
        elif rainfall == 0.0:
            return "Nie będzie padać"
        else:
            return "Nie wiem"
    else:
        return "Nie wiem"


def save_weather_data(date, weather_condition):
    # Open the file
    with open("weather_data.txt", "a") as file:
        # Write the date and weather condition to the file
        file.write(f"{date}: {weather_condition}\n")


def check_weather():
    # Ask the user for the date
    date_input = input("Podaj datę (YYYY-mm-dd): ")

    # Check if a date was provided
    if date_input:
        date = date_input
    else:
        # If no date was provided, use the next day's date
        today = datetime.now().date()
        date = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    # Check if the weather data for the date is already saved in the file
    with open("weather_data.txt", "r") as file:
        for line in file:
            if date in line:
                # If the data is already saved, retrieve the weather
                # condition from the file
                weather_condition = line.split(":")[1].strip()
                return weather_condition

    # If the weather data is not saved, retrieve it from the API
    latitude = input("Podaj szerokość geograficzną: ")
    longitude = input("Podaj długość geograficzną: ")

    weather_condition = get_weather_forecast(latitude, longitude, date)

    # Save the weather data to the file
    save_weather_data(date, weather_condition)

    return weather_condition


def create_weather_file():
    if not os.path.exists("weather_data.txt"):
        with open("weather_data.txt", "w") as file:
            file.write("")


# Create the weather file if it doesn't exist
create_weather_file()

# Run the program
weather_condition = check_weather()
print(weather_condition)
