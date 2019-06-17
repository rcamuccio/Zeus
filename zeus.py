# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Richard Camuccio
# 16 Jun 2019
#
# Last update: 17 Jun 2019
#
# Zeus
#

import os
import pyowm
import time

api_key = "api-key"
latitude = 25.995784
longitude = -97.568957

def do_query(api_key, latitude, longitude):

	owm = pyowm.OWM(api_key)

	obs = owm.weather_at_coords(latitude, longitude)

	reception_time = obs.get_reception_time(timeformat="iso")
	print("Reception time:", reception_time)

	return obs

if __name__ == "__main__":

	run = True
	while run == True:

		os.system("clear")

		print("+--------------------------+")
		print(" ZEUS Weather System")
		print(" C. T. Memorial Observatory")
		print("+--------------------------+")

		print("Sending pyowm query ...")
		obs = do_query(api_key, latitude, longitude)
		print("Query received:", obs)
		print()

		weather = obs.get_weather()

		reference_time = weather.get_reference_time(timeformat="iso")
		print("Reference time:", reference_time)
		print()
		
		location = obs.get_location()
		name = location.get_name()
		longitude = location.get_lon()
		latitude = location.get_lat()

		clouds = weather.get_clouds()
		rain = weather.get_rain()
		snow = weather.get_snow()
		humidity = weather.get_humidity()
		pressure = weather.get_pressure()
		temperature = weather.get_temperature(unit="celsius")
		status = weather.get_status()
		detailed_status = weather.get_detailed_status()
		weather_code = weather.get_weather_code()
		sunrise_time = weather.get_sunrise_time("iso")
		sunset_time = weather.get_sunset_time("iso")

		print("Clouds:", clouds)
		print("Rain:", rain)
		print("Snow:", snow)
		print()

		print("Humidity:", humidity)
		print()

		print("Pressure:", pressure["press"], "mbar")
		print()

		print("Temperature:", temperature["temp"], "°C")
		print("Max:", temperature["temp_max"], "°C")
		print("Min:", temperature["temp_min"], "°C")
		print()

		print("Status:", status)
		print("Detailed status:", detailed_status)
		print()

		print("Sunrise:", sunrise_time, "UTC")
		print("Sunset:", sunset_time, "UTC")
		print()

		print("City:", name)
		print("Longitude:", longitude)
		print("Latitude:", latitude)
		print()

		print("Pausing for one minute ...")
		time.sleep(60)