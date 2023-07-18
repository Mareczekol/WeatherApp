import requests
import json
from datetime import datetime, timedelta
import os


class WeatherForecast:
    def __init__(self):
        self.weather_data = {}
        self.create_weather_file()

    def get_weather_forecast(self, latitude, longitude, date):
        # Format the date
        formatted_date = datetime.strptime(date, "%Y-%m-%d").\
            strftime("%Y-%m-%d")

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

    def __setitem__(self, date, weather_condition):
        self.weather_data[date] = weather_condition
        with open("weather_data.txt", "a") as file:
            file.write(f"{date}: {weather_condition}\n")

    def __getitem__(self, date):
        if date not in self.weather_data:
            with open("weather_data.txt", "r") as file:
                for line in file:
                    if date in line:
                        weather_condition = line.split(":")[1].strip()
                        self.weather_data[date] = weather_condition
                        return weather_condition
            # latitude = input("Podaj szerokość geograficzną: ")
            # longitude = input("Podaj długość geograficzną: ")
            weather_condition = self.get_weather_forecast(latitude,
                                                          longitude, date)
            self.weather_data[date] = weather_condition
            self.__setitem__(date, weather_condition)
        return self.weather_data[date]

    def __iter__(self):
        return iter(self.weather_data)

    def items(self):
        return self.weather_data.items()

    def create_weather_file(self):
        if not os.path.exists("weather_data.txt"):
            with open("weather_data.txt", "w") as file:
                file.write("")

# Create the weather forecast object
weather_forecast = WeatherForecast()

# Run the program
date = None
while not date:
    date_input = input("Podaj datę (YYYY-mm-dd): ")
    if date_input:
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").\
                strftime("%Y-%m-%d")
        except ValueError:
            print("Podaj właściwą datę!")
    else:
        # If no date was provided, use the next day's date
        today = datetime.now().date()
        date = (today + timedelta(days=1)).strftime("%Y-%m-%d")

latitude = None
while not latitude:
    latitude_input = input("Podaj szerokość geograficzną: ")
    if latitude_input.replace(".", "", 1).isdigit():
        latitude = latitude_input
    else:
        print("Podaj właściwą szerokość geograficzną!")

longitude = None
while not longitude:
    longitude_input = input("Podaj długość geograficzną: ")
    if longitude_input.replace(".", "", 1).isdigit():
        longitude = longitude_input
    else:
        print("Podaj właściwą długość geograficzną!")


weather_condition = weather_forecast[date]
# print(weather_condition)
#
# for date in weather_forecast:
#     print(date)

for date, weather in weather_forecast.items():
    print(f"{date}: {weather}")
