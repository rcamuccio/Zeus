# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Zeus Weather System

Date: 29 Mar 2020
Last update: 11 Jul 2021

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

	def get_color_palette(self):

		return

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

	"""
	def get_imaging(self, location):

		return
	"""

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

	gust = forecast["gust"][0]

	humidity = forecast["humidity"][0]

	cloud_amount = forecast["cloud_amount"][0]

	prob_of_precip = forecast["prob_of_precip"][0]

	hourly_qpf = forecast["hourly_qpf"][0]

	print()
	print(" [Location]")
	print()

	print("   Point:", (latitude, longitude))
	print("   Location:", location)
	print("   Mean sea level:", height, "ft")

	print()
	print(" [Times]")
	print()

	print("   Begin astronomical twilight ", astronomical_twilight_begin)
	print("   Begin nautical twilight     ", nautical_twilight_begin)
	print("   Begin civil twilight        ", civil_twilight_begin)
	print("   Sunrise                     ", sunrise)
	print("   Solar noon                  ", solar_noon)
	print("   Sunset                      ", sunset)
	print("   End civil twilight          ", civil_twilight_end)
	print("   End nautical twilight       ", nautical_twilight_end)
	print("   End astronomical twilight   ", astronomical_twilight_end)

	print()
	print(" [Current Weather]")
	print()

	print("   Temperature                 ", temperature, "F")
	print("   Dew point                   ", dew_point, "F")
	print("   Heat index                  ", heat_index, "F")

	print()

	print("   Wind speed                  ", wind_speed, "mph")
	print("   Wind direction              ", wind_direction, "deg", "("+cardinal_direction+")")
	print("   Gust                        ", gust, "mph")

	print()

	print("   Humidity                    ", str(humidity) + "%")
	print("   Cloud amount                ", str(cloud_amount) + "%")
	print("   Precipitation               ", str(prob_of_precip) + "%")
	print("   Hourly QPF                  ", hourly_qpf, "in")

	"""
	print()
	print(" [Forecast]")
	print()

	block_hour = "  Hour (CDT)       "
	i = 0

	while i < 168:

		hour_str = "↓" + str(datetime.fromisoformat(forecast["time"][i]).hour)
		padding = " " * (6 - len(hour_str))
		block_hour += hour_str + padding
		i += 6

	print (block_hour)

	color_cloud_amount = "#FFFFFF"
	block_cloud_amount = "  Cloud amount (%) "

	for cloud_amount in forecast["cloud_amount"]:

		if cloud_amount < 1:
			color_cloud_amount = "#000020"
		elif 1 <= cloud_amount <= 9:
			color_cloud_amount = "#000040"
		elif 10 <= cloud_amount <= 19:
			color_cloud_amount = "#000060"
		elif 20 <= cloud_amount <= 29:
			color_cloud_amount = "#000080"
		elif 30 <= cloud_amount <= 39:
			color_cloud_amount = "#00009F"
		elif 40 <= cloud_amount <= 49:
			color_cloud_amount = "#0000BF"
		elif 50 <= cloud_amount <= 59:
			color_cloud_amount = "#0000DF"
		elif 60 <= cloud_amount <= 69:
			color_cloud_amount = "#6060FF"
		elif 70 <= cloud_amount <= 79:
			color_cloud_amount = "#8080FF"
		elif 80 <= cloud_amount <= 89:
			color_cloud_amount = "#9F9FFF"
		elif 90 <= cloud_amount <= 99:
			color_cloud_amount = "#BFBFFF"
		elif cloud_amount > 99:
			color_cloud_amount = "#DFDFFF"
		else:
			cloud_amount = "#FFFFFF"

		# Build cloud amount block
		block_cloud_amount += fg(color_cloud_amount) + u"\u25A0" + res

	print(block_cloud_amount)

	color_humidity = "#FFFFFF"
	block_humidity = "  Humidity (%)     "

	for humidity in forecast["humidity"]:

		if humidity < 1:
			color_humidity = "#003400"
		elif 1 <= humidity <= 9:
			color_humidity = "#005000"
		elif 10 <= humidity <= 19:
			color_humidity = "#006000"
		elif 20 <= humidity <= 29:
			color_humidity = "#007000"
		elif 30 <= humidity <= 39:
			color_humidity = "#008000"
		elif 40 <= humidity <= 49:
			color_humidity = "#009000"
		elif 50 <= humidity <= 59:
			color_humidity = "#209020"
		elif 60 <= humidity <= 69:
			color_humidity = "#60B060"
		elif 70 <= humidity <= 79:
			color_humidity = "#80C080"
		elif 80 <= humidity <= 89:
			color_humidity = "#9FCF9F"
		elif 90 <= humidity <= 99:
			color_humidity = "#BFDFBF"
		elif humidity > 99:
			color_humidity = "DFEFDF"
		else:
			humidity = "#FFFFFF"

		# Build humidity block
		block_humidity += fg(color_humidity) + u"\u25A0" + res

	print(block_humidity)

	color_temperature = "#FFFFFF"
	block_temperature = "  Temp (F)         "

	for temperature in forecast["temperature"]:

		if temperature < -40:
			color_temperature = "#FF00FF"
		elif -40 <= temperature <= -31:
			color_temperature = "#800080"
		elif -30 <= temperature <= -21:
			color_temperature = "#4B0082"
		elif -20 <= temperature <= -11:
			color_temperature = "#9400D3"
		elif -10 <= temperature <= -1:
			color_temperature = "#00008B"
		elif 0 <= temperature <= 9:
			color_temperature = "#0000CD"
		elif 10 <= temperature <= 19:
			color_temperature = "#0000FF"
		elif 20 <= temperature <= 29:
			color_temperature = "#00BFFF"
		elif 30 <= temperature <= 39:
			color_temperature = "#40E0D0"
		elif 40 <= temperature <= 49:
			color_temperature = "#008000"
		elif 50 <= temperature <= 59:
			color_temperature = "#32CD32"
		elif 60 <= temperature <= 69:
			color_temperature = "#ADFF2F"
		elif 70 <= temperature <= 79:
			color_temperature = "#FFFF00"
		elif 80 <= temperature <= 89:
			color_temperature = "#FFD700"
		elif 90 <= temperature <= 99:
			color_temperature = "#FFA500"
		elif 100 <= temperature <= 109:
			color_temperature = "#FF8C00"
		elif 110 <= temperature <= 119:
			color_temperature = "#FF4500"
		elif 120 <= temperature <= 129:
			color_temperature = "#FF0000"
		elif 130 <= temperature <= 139:
			color_temperature = "#800000"
		elif temperature > 140:
			color_temperature = "A52A2A"
		else:
			color_temperature = "#FFFFFF"

		block_temperature += fg(color_temperature) + u"\u25A0" + res

	print(block_temperature)

	"""

	print()

	end_time = time.time()
	total_time = end_time - start_time
	print(" ZEUS ended after", "%.1f" % total_time, "seconds")
