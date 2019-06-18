# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Richard Camuccio
# 17 Jun 2019
#
# Last update: 18 Jun 2019
#
# Zeus - Forecast monitor
#

import os
import pyowm
import time

api_key = "fc0f2f7ea440369459875fd191908468"
latitude = 25.995784
longitude = -97.568957

run = True
while run == True:

	os.system("clear")

	print("+--------------------------+")
	print(" ZEUS Weather System - Forecast Monitor")
	print(" C. T. Memorial Observatory")
	print("+--------------------------+")

	owm = pyowm.OWM(api_key)

	fc = owm.three_hours_forecast_at_coords(latitude, longitude)

	forecast = fc.get_forecast()
	print(forecast)

	for weather in forecast:

		clouds = weather.get_clouds()
		detailed_status = weather.get_detailed_status()
		dew_point = weather.get_dewpoint()
		heat_index = weather.get_heat_index()
		humidity = weather.get_humidity()
		pressure = weather.get_pressure()
		rain = weather.get_rain()


		reference_time = weather.get_reference_time(timeformat="date")


		snow = weather.get_snow()
		temperature = weather.get_temperature(unit="celsius")
		visibility = weather.get_visibility_distance()
		wind = weather.get_wind(unit="meters_sec")

		print(reference_time, clouds, rain, snow, humidity, pressure["press"], temperature["temp"], heat_index, dew_point, visibility, detailed_status)

	print("Pausing for one hour ...")
	time.sleep(3600)