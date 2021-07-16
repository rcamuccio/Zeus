# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Zeus Weather System

Date: 29 Mar 2020
Last update: 16 Jul 2021

"""

__author__ = "Richard Camuccio"
__version__ = "2.0.0"

import json
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os
import requests
import time
import xml.etree.ElementTree as ET

from astropy.time import Time
from colored import fg, bg, attr
from datetime import datetime
from dateutil import tz
from twython import Twython

class Zeus:

	def __init__(self):

		self.__access_token = ""
		self.__access_token_secret = ""
		self.__consumer_key = ""
		self.__consumer_secret = ""
		self.__url_nws = "https://forecast.weather.gov/MapClick.php?lat=33.5706&lon=-101.8553&FcstType=digitalDWML"
		self.__url_time = "https://api.sunrise-sunset.org/json?lat=33.5706&lng=-101.8553&formatted=0"

	def get_cardinal_direction(self, wind_direction):

		if wind_direction > 10 and wind_direction < 31:
			cardinal_direction = "NNE"
		elif wind_direction > 30 and wind_direction < 51:
			cardinal_direction = "NE"
		elif wind_direction > 50 and wind_direction < 71:
			cardinal_direction = "ENE"
		elif wind_direction > 70 and wind_direction < 101:
			cardinal_direction = "E"
		elif wind_direction > 100 and wind_direction < 121:
			cardinal_direction = "ESE"
		elif wind_direction > 120 and wind_direction < 141:
			cardinal_direction = "SE"
		elif wind_direction > 140 and wind_direction < 161:
			cardinal_direction = "SSE"
		elif wind_direction > 160 and wind_direction < 191:
			cardinal_direction = "S"
		elif wind_direction > 190 and wind_direction < 211:
			cardinal_direction = "SSW"
		elif wind_direction > 210 and wind_direction < 231:
			cardinal_direction = "SW"
		elif wind_direction > 230 and wind_direction < 251:
			cardinal_direction = "WSW"
		elif wind_direction > 250 and wind_direction < 281:
			cardinal_direction = "W"
		elif wind_direction > 280 and wind_direction < 301:
			cardinal_direction = "WNW"
		elif wind_direction > 300 and wind_direction < 321:
			cardinal_direcion = "NW"
		elif wind_direction > 320 and wind_direction < 341:
			cardinal_direction = "NNW"
		elif wind_direction > 340 and wind_direction < 11:
			cardinal_direction = "N"

		return cardinal_direction

	def get_color(self, parameter, value):

		if parameter == "cloud_amount":
			if value < 10:
				color = "#003F7F"
			elif value > 9 and value < 20:
				color = "#135393"
			elif value > 19 and value < 30:
				color = "#2767A7"
			elif value > 29 and value < 40:
				color = "#4F8FCF"
			elif value > 39 and value < 50:
				color = "#63A3E3"
			elif value > 49 and value < 60:
				color = "#77B7F7"
			elif value > 59 and value < 70:
				color = "#9ADADA"
			elif value > 69 and value < 80:
				color = "#AEEEEE"
			elif value > 79 and value < 90:
				color = "#C2C2C2"
			elif value > 89 and value < 100:
				color = "#EAEAEA"
			elif value > 99:
				color = "#FBFBFB"

		if parameter == "humidity":
			if value < 25:
				color = "#08035D"
			elif value > 24 and value < 31:
				color = "#0D4D8D"
			elif value > 30 and value < 36:
				color = "#3070B0"
			elif value > 35 and value < 41:
				color = "#4E8ECE"
			elif value > 40 and value < 46:
				color = "#71B1F1"
			elif value > 45 and value < 51:
				color = "#80C0C0"
			elif value > 50 and value < 56:
				color = "#09FEED"
			elif value > 55 and value < 61:
				color = "#55FAAD"
			elif value > 60 and value < 66:
				color = "#94FE6A"
			elif value > 65 and value < 71:
				color = "#EAFB16"
			elif value > 70 and value < 76:
				color = "#FEC600"
			elif value > 75 and value < 81:
				color = "#FC8602"
			elif value > 80 and value < 86:
				color = "#FE3401"
			elif value > 85 and value < 91:
				color = "#EA0000"
			elif value > 90 and value < 96:
				color = "#B70000"
			elif value > 95 and value < 101:
				color = "#E10000"

		if parameter == "temperature":
			if value < -40:
				color = "#FC00FC"
			elif value > -41 and value < -30:
				color = "#000085"
			elif value > -31 and value < -20:
				color = "#0000B2"
			elif value > -21 and value < -11:
				color = "#0000EC"
			elif value > -12 and value < -2:
				color = "#0034FE"
			elif value > -3 and value < 6:
				color = "#0089FE"
			elif value > 5 and value < 15:
				color = "#00D4FE"
			elif value > 14 and value < 24:
				color = "#1EFEDE"
			elif value > 23 and value < 33:
				color = "#FBFBFB"
			elif value > 32 and value < 42:
				color = "#5EFE9E"
			elif value > 41 and value < 51:
				color = "#A2FE5A"
			elif value > 50 and value < 60:
				color = "#FEDE00"
			elif value > 59 and value < 69:
				color = "#FE9E00"
			elif value > 68 and value < 78:
				color = "#FE5A00"
			elif value > 77 and value < 87:
				color = "#FE1E00"
			elif value > 86 and value < 96:
				color = "#E20000"
			elif value > 95 and value < 105:
				color = "#A90000"
			elif value > 104 and value < 114:
				color = "#7E0000"
			elif value > 113:
				color = "#C6C6C6"

		if parameter == "wind_speed":
			if value < 6:
				color = "#003F7F"
			elif value > 5 and value < 12:
				color = "#2C6CAC"
			elif value > 11 and value < 17:
				color = "#63A3E3"
			elif value > 16 and value < 29:
				color = "#95D5D5"
			elif value > 28 and value < 46:
				color = "#C7C7C7"
			elif value > 45:
				color = "#F9F9F9"

		return color

	def get_dst_index(self):

		response = requests.get(url="https://services.swpc.noaa.gov/products/kyoto-dst.json")

		response_text = json.loads(response.text)

		time_tag = response_text[len(response_text) - 1][0]
		dst = response_text[len(response_text) - 1][1]

		return time_tag, dst

	def get_forecast(self):

		response_nws = requests.get(url=self.__url_nws)
		response_nws_status_code = response_nws.status_code
		response_nws_content_type = response_nws.headers["content-type"]
		response_nws_encoding = response_nws.encoding

		xml_content = response_nws.content
		root = ET.fromstring(xml_content)

		element_creation_date = root[0][0][0]

		element_time_layout = root[1][2]

		element_dew_point = root[1][3][0]
		element_heat_index = root[1][3][1]
		element_wind_speed = root[1][3][2]
		element_cloud_amount = root[1][3][3]
		element_precipitation = root[1][3][4]
		element_humidity = root[1][3][5]
		element_wind_direction = root[1][3][6]
		element_temperature = root[1][3][7]
		element_gust = root[1][3][8]
		element_hourly_qpf = root[1][3][9]
		element_conditions = root[1][3][10]

		# Location
		for element in root.iter("point"):
			latitude = element.attrib["latitude"]
			longitude = element.attrib["longitude"]

		latitude_float = float(latitude)
		longitude_float = float(longitude)

		for element in root.iter("city"):
			location_str = element.text

		for element in root.iter("height"):
			element_height_str = element.text

		# Time
		time_start_list = []
		time_start_jd_list = []

		for i in range(1, 337, 2):

			time_start = element_time_layout[i]
			time_start_str = time_start.text

			if time_start_str.endswith("-05:00"):
				time_start_str = time_start_str[:-6]

			time_start_list.append(time_start_str)

			time_start_obj = Time(time_start_str, format="isot", scale="utc")
			time_start_jd = time_start_obj.jd
			time_start_jd_list.append(time_start_jd)

		# Weather conditions
		dew_point_list = []
		heat_index_list = []
		wind_speed_list = []
		cloud_amount_list = []
		prob_of_precip_list = []
		humidity_list = []
		wind_direction_list = []
		temperature_list = []
		gust_list = []
		hourly_qpf_list = []

		for i in range(0, 168):

			# Dew point list
			dew_point = element_dew_point[i]
			dew_point_str = dew_point.text
			dew_point_int = int(dew_point_str)
			dew_point_list.append(dew_point_int)

			# Heat index list
			heat_index = element_heat_index[i]
			heat_index_str = heat_index.text
			if heat_index_str == None:
				heat_index_int = 0
			else:
				heat_index_int = int(heat_index_str)
			heat_index_list.append(heat_index_int)

			# Wind speed list
			wind_speed = element_wind_speed[i]
			wind_speed_str = wind_speed.text
			wind_speed_int = int(wind_speed_str)
			wind_speed_list.append(wind_speed_int)

			# Cloud amount list
			cloud_amount = element_cloud_amount[i]
			cloud_amount_str = cloud_amount.text
			cloud_amount_int = int(cloud_amount_str)
			cloud_amount_list.append(cloud_amount_int)

			# Probability of precipitation list
			prob_of_precip = element_precipitation[i]
			prob_of_precip_str = prob_of_precip.text
			prob_of_precip_int = int(prob_of_precip_str)
			prob_of_precip_list.append(prob_of_precip_int)

			# Humidity list
			humidity = element_humidity[i]
			humidity_str = humidity.text
			humidity_int = int(humidity_str)
			humidity_list.append(humidity_int)

			# Wind direction list
			wind_direction = element_wind_direction[i]
			wind_direction_str = wind_direction.text
			wind_direction_int = int(wind_direction_str)
			wind_direction_list.append(wind_direction_int)

			# Temperature list
			temperature = element_temperature[i]
			temperature_str = temperature.text
			temperature_int = int(temperature_str)
			temperature_list.append(temperature_int)

			# Gust list
			gust = element_gust[i]
			gust_str = gust.text
			if gust_str == None:
				gust_int = 0
			else:
				gust_int = int(gust_str)
			gust_list.append(gust_int)

			# Hourly QPF list
			hourly_qpf = element_hourly_qpf[i]
			hourly_qpf_str = hourly_qpf.text
			if hourly_qpf_str == None:
				hourly_qpf_float = 0.0
			else:
				hourly_qpf_float = float(hourly_qpf_str)
			hourly_qpf_list.append(hourly_qpf_float)

		return {"latitude" : latitude_float,
				"longitude" : longitude_float,
				"location" : location_str,
				"height" : element_height_str,
				"time" : time_start_list, 
				"time_jd" : time_start_jd_list, 
				"dew_point" : dew_point_list, 
				"heat_index" : heat_index_list, 
				"wind_speed" : wind_speed_list, 
				"cloud_amount" : cloud_amount_list, 
				"prob_of_precip" : prob_of_precip_list, 
				"humidity" : humidity_list, 
				"wind_direction" : wind_direction_list, 
				"temperature" : temperature_list, 
				"gust" : gust_list, 
				"hourly_qpf" : hourly_qpf_list}

	def get_k_index(self):

		response = requests.get(url="https://services.swpc.noaa.gov/products/noaa-estimated-planetary-k-index-1-minute.json")

		response_text = json.loads(response.text)

		time_tag = response_text[len(response_text) - 1][0]
		k_index = response_text[len(response_text) - 1][1]

		return time_tag, k_index

	def get_radio_flux(self):

		response = requests.get(url="https://services.swpc.noaa.gov/products/10cm-flux-30-day.json")

		response_text = json.loads(response.text)

		time_tag = response_text[len(response_text) - 1][0]
		flux = response_text[len(response_text) - 1][1]

		return time_tag, flux

	def get_solar_magnetic_field(self):

		response = requests.get(url="https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json")

		response_text = json.loads(response.text)

		time_tag = response_text[len(response_text) - 1][0]
		b_total = response_text[len(response_text) - 1][6]

		return time_tag, b_total

	def get_solar_wind(self):

		response = requests.get(url="https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json")

		response_text = json.loads(response.text)

		time_tag = response_text[len(response_text) - 1][0]
		density = response_text[len(response_text) - 1][1]
		speed = response_text[len(response_text) - 1][2]
		temperature = response_text[len(response_text) - 1][3]

		return time_tag, density, speed, temperature

	def get_xray_flux(self):

		response = requests.get(url="https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json")

		response_text = json.loads(response.text)

		current_time = response_text[0]["time_tag"]
		current_class = response_text[0]["current_class"]
		max_time = response_text[0]["max_time"]
		max_class = response_text[0]["max_class"]
		max_flux = response_text[0]["max_xrlong"]

		return current_time, current_class, max_time, max_class, max_flux

	def get_times(self):

		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()

		response_sunset = requests.get(url=self.__url_time)
		response_sunset_status_code = response_sunset.status_code
		response_sunset_content_type = response_sunset.headers["content-type"]
		response_sunset_encoding = response_sunset.encoding

		parse_response_sunset = json.loads(response_sunset.text)

		# Begin astronomical twilight
		astronomical_twilight_begin_str = parse_response_sunset["results"]["astronomical_twilight_begin"]
		astronomical_twilight_begin_datetime = datetime.strptime(astronomical_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
		astronomical_twilight_begin_datetime_utc = astronomical_twilight_begin_datetime.replace(tzinfo=from_zone)
		astronomical_twilight_begin_datetime_local = astronomical_twilight_begin_datetime_utc.astimezone(to_zone)

		# Begin nautical twilight
		nautical_twilight_begin_str = parse_response_sunset["results"]["nautical_twilight_begin"]
		nautical_twilight_begin_datetime = datetime.strptime(nautical_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
		nautical_twilight_begin_datetime_utc = nautical_twilight_begin_datetime.replace(tzinfo=from_zone)
		nautical_twilight_begin_datetime_local = nautical_twilight_begin_datetime_utc.astimezone(to_zone)

		# Begin civil twilight
		civil_twilight_begin_str = parse_response_sunset["results"]["civil_twilight_begin"]
		civil_twilight_begin_datetime = datetime.strptime(civil_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
		civil_twilight_begin_datetime_utc = civil_twilight_begin_datetime.replace(tzinfo=from_zone)
		civil_twilight_begin_datetime_local = civil_twilight_begin_datetime_utc.astimezone(to_zone)

		# Sunrise
		sunrise_str = parse_response_sunset["results"]["sunrise"]
		sunrise_datetime = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M:%S+00:00")
		sunrise_datetime_utc = sunrise_datetime.replace(tzinfo=from_zone)
		sunrise_datetime_local = sunrise_datetime_utc.astimezone(to_zone)

		# Solar noon
		solar_noon_str = parse_response_sunset["results"]["solar_noon"]
		solar_noon_datetime = datetime.strptime(solar_noon_str, "%Y-%m-%dT%H:%M:%S+00:00")
		solar_noon_datetime_utc = solar_noon_datetime.replace(tzinfo=from_zone)
		solar_noon_datetime_local = solar_noon_datetime_utc.astimezone(to_zone)

		# Sunset
		sunset_str = parse_response_sunset["results"]["sunset"]
		sunset_datetime = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M:%S+00:00")
		sunset_datetime_utc = sunset_datetime.replace(tzinfo=from_zone)
		sunset_datetime_local = sunset_datetime_utc.astimezone(to_zone)

		# End civil twilight
		civil_twilight_end_str = parse_response_sunset["results"]["civil_twilight_end"]
		civil_twilight_end_datetime = datetime.strptime(civil_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
		civil_twilight_end_datetime_utc = civil_twilight_end_datetime.replace(tzinfo=from_zone)
		civil_twilight_end_datetime_local = civil_twilight_end_datetime_utc.astimezone(to_zone)

		# End nautical twilight
		nautical_twilight_end_str = parse_response_sunset["results"]["nautical_twilight_end"]
		nautical_twilight_end_datetime = datetime.strptime(nautical_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
		nautical_twilight_end_datetime_utc = nautical_twilight_end_datetime.replace(tzinfo=from_zone)
		nautical_twilight_end_datetime_local = nautical_twilight_end_datetime_utc.astimezone(to_zone)

		# End astronomical twilight
		astronomical_twilight_end_str = parse_response_sunset["results"]["astronomical_twilight_end"]
		astronomical_twilight_end_datetime = datetime.strptime(astronomical_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
		astronomical_twilight_end_datetime_utc = astronomical_twilight_end_datetime.replace(tzinfo=from_zone)
		astronomical_twilight_end_datetime_local = astronomical_twilight_end_datetime_utc.astimezone(to_zone)

		return {"astronomical_twilight_begin" : astronomical_twilight_begin_datetime_local,
				"nautical_twilight_begin" : nautical_twilight_begin_datetime_local,
				"civil_twilight_begin" : civil_twilight_begin_datetime_local,
				"sunrise" : sunrise_datetime_local,
				"solar_noon" : solar_noon_datetime_local,
				"sunset" : sunset_datetime_local,
				"civil_twilight_end" : civil_twilight_end_datetime_local,
				"nautical_twilight_end" : nautical_twilight_end_datetime_local,
				"astronomical_twilight_end" : astronomical_twilight_end_datetime_local}

	"""
	def send_tweet(self, message="#ctmosays Hello world!"):

		twitter = Twython(self.__consumer_key, self.__consumer_secret, self.__access_token, self.__access_token_secret)

		#twitter.update_status(status = message)
		print(" Tweeted: %s" % message)

		return
	"""

if __name__ == "__main__":

	os.system("clear")
	start_time = time.time()

	zeus = Zeus()
	print(" ZEUS Weather System v2.0")
	res = attr("reset")

	time_now = datetime.now()

	times = zeus.get_times()

	astronomical_twilight_begin = times["astronomical_twilight_begin"]
	nautical_twilight_begin = times["nautical_twilight_begin"]
	civil_twilight_begin = times["civil_twilight_begin"]
	sunrise = times["sunrise"]
	solar_noon = times["solar_noon"]
	sunset = times["sunset"]
	civil_twilight_end = times["civil_twilight_end"]
	nautical_twilight_end = times["nautical_twilight_end"]
	astronomical_twilight_end = times["astronomical_twilight_end"]

	forecast = zeus.get_forecast()

	latitude = forecast["latitude"]
	longitude = forecast["longitude"]
	location = forecast["location"]
	height = forecast["height"]

	temperature = forecast["temperature"][0]
	dew_point = forecast["dew_point"][0]
	heat_index = forecast["heat_index"][0]

	wind_speed = forecast["wind_speed"][0]
	wind_direction = forecast["wind_direction"][0]
	cardinal_direction = zeus.get_cardinal_direction(wind_direction)
	gust = forecast["gust"][0]

	humidity = forecast["humidity"][0]

	cloud_amount = forecast["cloud_amount"][0]

	prob_of_precip = forecast["prob_of_precip"][0]

	hourly_qpf = forecast["hourly_qpf"][0]

	radio_flux = zeus.get_radio_flux()
	flux_time = radio_flux[0]
	flux = radio_flux[1]

	b_field = zeus.get_solar_magnetic_field()
	b_time = b_field[0]
	b_total = b_field[1]

	solar_wind = zeus.get_solar_wind()
	solar_wind_time = solar_wind[0]
	solar_wind_density = solar_wind[1]
	solar_wind_speed = solar_wind[2]
	solar_wind_temperature = solar_wind[3]

	kyoto_dst = zeus.get_dst_index()
	dst_time = kyoto_dst[0]
	dst = kyoto_dst[1]

	planetary_k = zeus.get_k_index()
	k_index_time = planetary_k[0]
	k_index = planetary_k[1]

	xray_flares = zeus.get_xray_flux()
	xray_current_time = xray_flares[0]
	xray_current_class = xray_flares[1]
	xray_max_time = xray_flares[2]
	xray_max_class = xray_flares[3]
	xray_max_flux = xray_flares[4]

	print()
	print("\033[1m" + " [Location]" + "\033[0m", location, (latitude, longitude))
	print("           ", height, "ft")
	print()
	print("\033[1m" + " [Time]" + "\033[0m", time_now.date(), time_now.strftime("%H:%M:%S"))
	print()
	print("   [BMAT]", astronomical_twilight_begin.strftime("%H:%M:%S"), "| [Rise]", sunrise.strftime("%H:%M:%S"), "| [EECT]", civil_twilight_end.strftime("%H:%M:%S"))
	print("   [BMNT]", nautical_twilight_begin.strftime("%H:%M:%S"), "| [Noon]", solar_noon.strftime("%H:%M:%S"), "| [EENT]", nautical_twilight_end.strftime("%H:%M:%S"))
	print("   [BMCT]", civil_twilight_begin.strftime("%H:%M:%S"), "| [Set] ", sunset.strftime("%H:%M:%S"), "| [EEAT]", astronomical_twilight_end.strftime("%H:%M:%S"))
	print()
	print("\033[1m" + " [Weather]" + "\033[0m" + "                      " + "\033[1m" + "[Solar]" + "\033[0m")
	print()
	print("   [Temperature]   ", temperature, "F", "        ", "[Speed]         ", solar_wind_speed, "km/s")
	print("   [Dew Point]     ", dew_point, "F", "        ", "[Density]       ", solar_wind_density, "protons/cm^3")
	print("   [Heat Index]    ", heat_index, "F", "        ", "[Temperature]   ", solar_wind_temperature, "K")
	print()
	print("   [Humidity]      ", humidity, "%", "        ", "[F10.7 Flux]    ", flux, "sfu")
	print("   [Clouds]        ", cloud_amount, "%", "         ", "[B Field]       ", b_total, "nT")
	print("   [Wind]          ", cardinal_direction, wind_speed, "mph", "   ", "[X-Ray Current] ", xray_current_class)
	print("   [Gusts]         ", gust, "mph", "       ", "[X-Ray Max]     ", xray_max_class, "("+"{:0.2e}".format(xray_max_flux)+" W/m^2)")
	print("                                 ", )
	print("   [Precipitation] ", str(prob_of_precip) + "%", "          ", "[K_p Index]     ", k_index)
	print("   [QPF]           ", hourly_qpf, "in/hr", "   ", "[DST Index]     ", dst)

	##############################################################################################

	print()
	print("\033[1m" + " [Forecast]" + "\033[0m")
	print()

	block_day = 		"   Date (0000 CDT)  "
	block_hour = 		"                    "
	block_temperature = "   Temperature (F)  "
	block_humidity = 	"   Humidity (%)     "
	block_cloud_amount ="   Clouds (%)       "
	block_wind_speed = 	"   Wind (mph)       "

	days = 5
	blocks = days * 24
	i = 0
	j = 0

	while i < blocks:

		month = datetime.fromisoformat(forecast["time"][i]).month
		day = datetime.fromisoformat(forecast["time"][i]).day
		hour = datetime.fromisoformat(forecast["time"][i]).hour

		if hour == 0:
			hour_str = "↓"
			block_hour += hour_str
			block_day += str(month) + "/" + str(day)
			j = 3
		else:
			if j > 0:
				hour_str = " "
				block_hour += hour_str
				block_day += ""
				j -= 1
			else:
				hour_str = " "
				block_hour += hour_str
				block_day += " "

		# Build temperature blocks
		temperature = forecast["temperature"][i]
		color_temperature = zeus.get_color("temperature", temperature)
		block_temperature += fg(color_temperature) + u"\u25A0" + res

		# Build humidity blocks
		humidity = forecast["humidity"][i]
		color_humidity = zeus.get_color("humidity", humidity)
		block_humidity += fg(color_humidity) + u"\u25A0" + res

		# Build cloud amount blocks
		cloud_amount = forecast["cloud_amount"][i]
		color_cloud_amount = zeus.get_color("cloud_amount", cloud_amount)
		block_cloud_amount += fg(color_cloud_amount) + u"\u25A0" + res

		# Build wind speed blocks
		wind_speed = forecast["wind_speed"][i]
		color_wind_speed = zeus.get_color("wind_speed", wind_speed)
		block_wind_speed += fg(color_wind_speed) + u"\u25A0" + res

		i += 1

	print(block_day)
	print(block_hour)
	print(block_temperature)
	print(block_humidity)
	print()
	print(block_cloud_amount)
	print(block_wind_speed)
	print()

	##############################################################################################

	end_time = time.time()
	total_time = end_time - start_time
	print(" ZEUS ended after", "%.1f" % total_time, "seconds")
	print()