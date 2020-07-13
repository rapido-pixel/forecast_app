import csv
import os

import cv2
from PIL import Image

IMAGE = cv2.imread('python_snippets/external_data/probe.jpg')
CLOUD = "python_snippets/external_data/weather_img/cloud.jpg"
RAIN = "python_snippets/external_data/weather_img/rain.jpg"
SNOW = "python_snippets/external_data/weather_img/snow.jpg"
SUN = "python_snippets/external_data/weather_img/sun.jpg"
IMG_PATH = "./daily_forecast"


class ImageMaker:

    def __init__(self, image, cloud, rain, snow, sun, image_path):
        self.image = image
        self.resized_image = None
        self.cloud = cloud
        self.rain = rain
        self.snow = snow
        self.sun = sun
        self.image_path = image_path
        self.icon = None
        self.color_y_coord = 0
        self.forecasts_for_draw = []

    def resize_image(self):
        scale_percent = 150
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)
        self.resized_image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

    def make_forecast_image(self):
        for day in self.forecasts_for_draw:
            output = self.resized_image.copy()
            y_coord = 120
            px = 0
            self.weather_gradient(px, output, day)
            for key in day:
                cv2.putText(output, day[key], (100, y_coord), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 0, 0), 4)
                y_coord += 100
            cv2.imwrite(os.path.join(self.image_path, f"forecast_{day['дата']}.jpg"), output)
            self.add_weather_icon(day)

    def add_weather_icon(self, day):
        forecast_img = Image.open(os.path.join(self.image_path, f"forecast_{day['дата']}.jpg"))
        if "дождь" in day["погода"]:
            self.icon = Image.open(self.rain)
        elif "облачно" in day["погода"]:
            self.icon = Image.open(self.cloud)
        elif "ясно" in day["погода"]:
            self.icon = Image.open(self.sun)
        else:
            self.icon = Image.open(self.snow)
        forecast_img.paste(self.icon, (600, 250))
        forecast_img.save(os.path.join(self.image_path, f"forecast_{day['дата']}.jpg"), "JPEG")

    def weather_gradient(self, px, img, day):
        if "облачно" in day["погода"] or "дымка" in day["погода"]:
            px = 100
        for h in range(0, img.shape[1], 1):
            if "дождь" in day["погода"]:
                img[self.color_y_coord:h, 0:img.shape[1], 1] = px
                img[self.color_y_coord:h, 0:img.shape[1], 2] = px
            elif "облачно" in day["погода"] or "дымка" in day["погода"]:
                img[self.color_y_coord:h, 0:img.shape[1], None] = px
            elif "ясно" in day["погода"]:
                img[self.color_y_coord:h, 0:img.shape[1], 0] = px
            else:
                img[self.color_y_coord:h, 0:img.shape[1], 2] = px
            self.color_y_coord = h
            px += 1
            if px >= 255:
                break

    def read_csv(self):
        with open("./import_f.csv", 'r', newline='') as csv_file:
            csv_data = csv.DictReader(csv_file)
            self.forecasts_for_draw = list(csv_data)

    def run(self):
        self.read_csv()
        self.resize_image()
        self.make_forecast_image()
