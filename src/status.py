# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Richard Camuccio
# 16 Jun 2019
#
# Last update: 18 Jun 2019
#
# Zeus - Current status monitor
#

from colored import  fg, bg, attr
import datetime
import os
import pyowm
import time

api_key = "user-api-key"

daylight_savings = True

if daylight_savings == True:
	delta_time = datetime.timedelta(hours=5)
else:
	delta_time = datetime.timedelta(hours=6)

latitude = 25.995784
longitude = -97.568957

run = True
while run == True:

	os.system("clear")

	print("+--------------------------+")
	print(" CTMO ZEUS Weather System")
	print(" Current Status")
	print("+--------------------------+")

	owm = pyowm.OWM(api_key)

	print("Sending weather query ...")
	obs = owm.weather_at_coords(latitude, longitude)
	print("Weather query received!")
	print()

	reception_time = obs.get_reception_time(timeformat="date")
	print("Reception time:", reception_time, "UTC")
	local_reception_time = reception_time - delta_time
	print("               ", local_reception_time, "local")
	print()

	weather = obs.get_weather()

	reference_time = weather.get_reference_time(timeformat="date")
	print("Reference time:", reference_time, "UTC")
	local_reference_time = reference_time - delta_time
	print("               ", local_reference_time, "local")
	print()

	sunrise_time = weather.get_sunrise_time("date")
	print("Sunrise:", sunrise_time, "UTC")
	local_sunrise_time = sunrise_time - delta_time
	print("        ", local_sunrise_time, "local")
	print()

	sunset_time = weather.get_sunset_time("date")
	print("Sunset:", sunset_time, "UTC")
	local_sunset_time = sunset_time - delta_time
	print("       ", local_sunset_time, "local")
	print()

	location = obs.get_location()
	name = location.get_name()
	longitude = location.get_lon()
	latitude = location.get_lat()

	print("City:", name)
	print("Longitude:", longitude)
	print("Latitude:", latitude)
	print()

	status = weather.get_status()
	detailed_status = weather.get_detailed_status()
	print("Status:", status)
	print("Detailed status:", detailed_status)

	clouds = weather.get_clouds()
	print("Clouds:", clouds, "%")

	rain = weather.get_rain()
	print("Rain:", rain)

	snow = weather.get_snow()
	print("Snow:", snow)
	print()

	temperature_c = weather.get_temperature(unit="celsius")
	temperature_f = weather.get_temperature(unit="fahrenheit")

	temp_c = temperature_c["temp"]
	temp_f = temperature_f["temp"]

	temp_max_c = temperature_c["temp_max"]
	temp_max_f = temperature_f["temp_max"]

	temp_min_c = temperature_c["temp_min"]
	temp_min_f = temperature_f["temp_min"]

	delta_plus_c = temp_max_c - temp_c
	delta_plus_f = temp_max_f - temp_f

	delta_minus_c = temp_c - temp_min_c
	delta_minus_f = temp_f - temp_min_f

	print("Temperature:", temp_c, "( +", "%.2f" % delta_plus_c, "-", "%.2f" % delta_minus_c, ") °C")
	print("            ", temp_f, "( +", "%.2f" % delta_plus_f, "-", "%.2f" % delta_minus_f, ") °C")


	heat_index = weather.get_heat_index()
	print("Heat index:", heat_index)

	dew_point = weather.get_dewpoint()
	print("Dew point:", dew_point)
	print()

	wind = weather.get_wind(unit="meters_sec")
	print("Wind speed:", "%.2f" % wind["speed"], "m/s")
	print("Direction:", wind["deg"], "deg")
	print()

	humidity = weather.get_humidity()
	print("Humidity:", humidity, "%")
	print()

	pressure = weather.get_pressure()
	print("Pressure:", pressure["press"], "hPa")
	print()

	visibility = weather.get_visibility_distance()
	print("Visibility:", visibility)

	print()
	print("+--------------------------------------------------+")
	print()

	print("Sending UVI query ...")
	uvi = owm.uvindex_around_coords(latitude, longitude)
	print("UVI query received!")
	print()

	uvi_reception_time = uvi.get_reception_time(timeformat="date")
	print("UVI reception time:", uvi_reception_time, "UTC")
	print()

	uvi_reference_time = uvi.get_reference_time(timeformat="date")
	print("UVI reference time:", uvi_reference_time, "UTC")
	print()

	uvi_value = uvi.get_value()
	print("UV index:", uvi_value)

	uvi_exposure_risk = uvi.get_exposure_risk()

	reset = attr("reset")

	if uvi_exposure_risk == "green":
		print("UV exposure risk:", fg("green") + uvi_exposure_risk + reset)
		print()

	elif uvi_exposure_risk == "yellow":
		print("UV exposure risk:", fg("yellow") + uvi_exposure_risk + reset)
		print()

	elif uvi_exposure_risk == "orange":
		print("UV exposure risk:", fg("orange") + uvi_exposure_risk + reset)
		print()

	elif uvi_exposure_risk == "red":
		print("UV exposure risk:", fg("red") + uvi_exposure_risk + reset)
		print()

	elif uvi_exposure_risk == "extreme":
		print("UV exposure risk:", fg("violet") + uvi_exposure_risk + reset)
		print()

	else:
		print("UV exposure risk:", uvi_exposure_risk)
		print()

	print("Pausing for one minute ...")
	time.sleep(60)