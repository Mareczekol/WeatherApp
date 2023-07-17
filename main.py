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

        # Check if rainfall is not None
        if rainfall is not None:
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

    if date_input:
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").strftime(
                "%Y-%m-%d")
        except ValueError:
            print("Podaj właściwą datę!")
            return check_weather()
    else:
        # If no date was provided, use the next day's date
        today = datetime.now().date()
        date = (today + timedelta(days=1)).strftime("%Y-%m-%d")

    # Extract the latitude and longitude coordinates from the response
    latitude = 0
    longitude = 0

    while not latitude:
        latitude_input = input("Podaj szerokość geograficzną: ")
        if latitude_input.replace(".", "", 1).isdigit():
            latitude = latitude_input
        else:
            print("Podaj właściwą szerokość geograficzną!")
            continue
    while not longitude:
        longitude_input = input("Podaj długość geograficzną: ")
        if longitude_input.replace(".", "", 1).isdigit():
            longitude = longitude_input
        else:
            print("Podaj właściwą długość geograficzną!")
            continue

    # Check if the weather data for the date is already saved in the file
    with open("weather_data.txt", "r") as file:
        for line in file:
            if date in line:
                # If the data is already saved, retrieve the weather
                # condition from the file
                weather_condition = line.split(":")[1].strip()
                return weather_condition

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
