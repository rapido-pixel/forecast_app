# -*- coding: utf-8 -*-
import time
import locale
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

URL = "https://pogoda.mail.ru/prognoz/moskva"

MONTHS_NUMBERS = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"
}

HEADERS = {

    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 "
                  "Safari/537.36 "
}


class WeatherMaker:

    def __init__(self, url, months_numbers, from_date=None, days_count=None):
        self.url = url
        self.user_date = from_date
        self.days_count = days_count
        self.dates = []
        self.url_dates = []
        self.days_forecasts = []
        self.months_numbers = months_numbers

    def date_generator(self):
        start_date = datetime.strptime(self.user_date, "%Y-%m-%d")
        end_date = datetime.strptime(self.days_count, "%Y-%m-%d")
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def url_dates_generator(self):
        for date in self.date_generator():
            self.url_dates.append(f"{date.day}-{self.months_numbers[date.month]}")

    def forecast_parser(self):
        for date in self.url_dates:
            url = requests.get(f"{self.url}/{date}", headers=HEADERS).text
            time.sleep(0.6)
            soup = BeautifulSoup(url, "html.parser")
            forecast_to_day = {}
            forecast = soup.find("div", {"class": "block block_selected"})
            data = forecast.find("div", {"class": "heading"})
            data = data.text.replace("\n", "").replace("\t", "")
            forecast_to_day["date"] = str(datetime.strptime(data, "%d %B %Y"))
            days = forecast.find_all("div", {"class": "day day_period"})
            for day in days:
                if day.find("div", text="Днем"):
                    temp = day.find("div", {"class": "day__temperature"}).text
                    forecast_to_day["temperature"] = temp.replace("°", "")
                    weather = day.find("span").text
                    forecast_to_day["weather"] = weather
                    self.days_forecasts.append(forecast_to_day)

    def run(self):
        self.date_generator()
        self.url_dates_generator()
        self.forecast_parser()
