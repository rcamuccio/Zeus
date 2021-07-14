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
	if temperature < -40:
		color_temperature = "#FC00FC"
	elif temperature > -41 and temperature < -30:
		color_temperature = "#000085"
	elif temperature > -31 and temperature < -20:
		color_temperature = "#0000B2"
	elif temperature > -21 and temperature < -11:
		color_temperature = "#0000EC"
	elif temperature > -12 and temperature < -2:
		color_temperature = "#0034FE"
	elif temperature > -3 and temperature < 6:
		color_temperature = "#0089FE"
	elif temperature > 5 and temperature < 15:
		color_temperature = "#00D4FE"
	elif temperature > 14 and temperature < 24:
		color_temperature = "#1EFEDE"
	elif temperature > 23 and temperature < 33:
		color_temperature = "#FBFBFB"
	elif temperature > 32 and temperature < 42:
		color_temperature = "#5EFE9E"
	elif temperature > 41 and temperature < 51:
		color_temperature = "#A2FE5A"
	elif temperature > 50 and temperature < 60:
		color_temperature = "#FEDE00"
	elif temperature > 59 and temperature < 69:
		color_temperature = "#FE9E00"
	elif temperature > 68 and temperature < 78:
		color_temperature = "#FE5A00"
	elif temperature > 77 and temperature < 87:
		color_temperature = "#FE1E00"
	elif temperature > 86 and temperature < 96:
		color_temperature = "#E20000"
	elif temperature > 95 and temperature < 105:
		color_temperature = "#A90000"
	elif temperature > 104 and temperature < 114:
		color_temperature = "#7E0000"
	elif temperature > 113:
		color_temperature = "#C6C6C6"
	else:
		color_temperature = "#FFFFFF"
	block_temperature = fg(color_temperature) + u"\u25A0" + res

	dew_point = forecast["dew_point"][0]
	heat_index = forecast["heat_index"][0]

	wind_speed = forecast["wind_speed"][0]
	if wind_speed < 6:
		color_wind_speed = "#003F7F"
	elif wind_speed > 5 and wind_speed < 12:
		color_wind_speed = "#2C6CAC"
	elif wind_speed > 11 and wind_speed < 17:
		color_wind_speed = "#63A3E3"
	elif wind_speed > 16 and wind_speed < 29:
		color_wind_speed = "#95D5D5"
	elif wind_speed > 28 and wind_speed < 46:
		color_wind_speed = "#C7C7C7"
	elif wind_speed > 45:
		color_wind_speed = "#F9F9F9"

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
	if humidity < 25:
		color_humidity = "#08035D"
	elif humidity > 24 and humidity < 31:
		color_humidity = "#0D4D8D"
	elif humidity > 30 and humidity < 36:
		color_humidity = "#3070B0"
	elif humidity > 35 and humidity < 41:
		color_humidity = "#4E8ECE"
	elif humidity > 40 and humidity < 46:
		color_humidity = "#71B1F1"
	elif humidity > 45 and humidity < 51:
		color_humidity = "#80C0C0"
	elif humidity > 50 and humidity < 56:
		color_humidity = "#09FEED"
	elif humidity > 55 and humidity < 61:
		color_humidity = "#55FAAD"
	elif humidity > 60 and humidity < 66:
		color_humidity = "#94FE6A"
	elif humidity > 65 and humidity < 71:
		color_humidity = "#EAFB16"
	elif humidity > 70 and humidity < 76:
		color_humidity = "#FEC600"
	elif humidity > 75 and humidity < 81:
		color_humidity = "#FC8602"
	elif humidity > 80 and humidity < 86:
		color_humidity = "#FE3401"
	elif humidity > 85 and humidity < 91:
		color_humidity = "#EA0000"
	elif humidity > 90 and humidity < 96:
		color_humidity = "#B70000"
	elif humidity > 95 and humidity < 101:
		color_humidity = "#E10000"

	cloud_amount = forecast["cloud_amount"][0]
	if cloud_amount < 10:
		color_cloud_amount = "#003F7F"
	elif cloud_amount > 9 and cloud_amount < 20:
		color_cloud_amount = "#135393"
	elif cloud_amount > 19 and cloud_amount < 30:
		color_cloud_amount = "#2767A7"
	elif cloud_amount > 29 and cloud_amount < 40:
		color_cloud_amount = "#4F8FCF"
	elif cloud_amount > 39 and cloud_amount < 50:
		color_cloud_amount = "#63A3E3"
	elif cloud_amount > 49 and cloud_amount < 60:
		color_cloud_amount = "#77B7F7"
	elif cloud_amount > 59 and cloud_amount < 70:
		color_cloud_amount = "#9ADADA"
	elif cloud_amount > 69 and cloud_amount < 80:
		color_cloud_amount = "#AEEEEE"
	elif cloud_amount > 79 and cloud_amount < 90:
		color_cloud_amount = "#C2C2C2"
	elif cloud_amount > 89 and cloud_amount < 100:
		color_cloud_amount = "#EAEAEA"
	elif cloud_amount > 99:
		color_cloud_amount = "#FBFBFB"

	prob_of_precip = forecast["prob_of_precip"][0]
	hourly_qpf = forecast["hourly_qpf"][0]

	print()
	print("\033[1m" + " [Location]" + "\033[0m", location, (latitude, longitude))
	print("           ", height, "ft")
	print()
	print("\033[1m" + " [Time]" + "\033[0m", time_now.date(), time_now.strftime("%H:%M:%S"))
	print()
	print("   [BMAT] ", astronomical_twilight_begin.strftime("%H:%M:%S"))
	print("   [BMNT] ", nautical_twilight_begin.strftime("%H:%M:%S"))
	print("   [BMCT] ", civil_twilight_begin.strftime("%H:%M:%S"))
	print()
	print("   [Rise] ", sunrise.strftime("%H:%M:%S"))
	print("   [Noon] ", solar_noon.strftime("%H:%M:%S"))
	print("   [Set]  ", sunset.strftime("%H:%M:%S"))
	print()
	print("   [EECT] ", civil_twilight_end.strftime("%H:%M:%S"))
	print("   [EENT] ", nautical_twilight_end.strftime("%H:%M:%S"))
	print("   [EEAT] ", astronomical_twilight_end.strftime("%H:%M:%S"))
	print()
	print("\033[1m" + " [Weather]" + "\033[0m")
	print()
	print("   [Temperature]   ", fg(color_temperature) + str(temperature) + " F" + res)
	print("   [Dew Point]     ", dew_point, "F")
	print("   [Heat Index]    ", heat_index, "F")
	print()
	print("   [Humidity]      ", fg(color_humidity) + str(humidity) + " %" + res)
	print("   [Clouds]        ", fg(color_cloud_amount) + str(cloud_amount) + " %" + res)
	print("   [Wind]          ", fg(color_wind_speed) + cardinal_direction + " " + str(wind_speed) + " mph" + res)
	print("   [Gusts]         ", gust, "mph")
	print()
	print("   [Precipitation] ", str(prob_of_precip) + "%")
	print("   [QPF]           ", hourly_qpf, "in/hr")

	##############################################################################################

	print()
	print(" [Forecast]")
	print()

	block_hour = "  Hour (CDT)       "

	color_temperature = "#FFFFFF"
	block_temperature = "  Temperature (F)  "

	color_humidity = "#FFFFFF"
	block_humidity = "  Humidity (%)     "

	color_cloud_amount = "#FFFFFF"
	block_cloud_amount = "  Clouds (%)       "

	color_wind_speed = "#FFFFFF"
	block_wind_speed = "  Wind (mph)       "

	i = 0

	while i < 120:

		hour_str = "↓" + str(datetime.fromisoformat(forecast["time"][i]).hour)
		padding = " " * (6 - len(hour_str))
		block_hour += hour_str + padding
		i += 6

	print(block_hour)

	i = 0

	while i < 120:

		temperature = forecast["temperature"][i]
		if temperature < -40:
			color_temperature = "#FC00FC"
		elif temperature > -41 and temperature < -30:
			color_temperature = "#000085"
		elif temperature > -31 and temperature < -20:
			color_temperature = "#0000B2"
		elif temperature > -21 and temperature < -11:
			color_temperature = "#0000EC"
		elif temperature > -12 and temperature < -2:
			color_temperature = "#0034FE"
		elif temperature > -3 and temperature < 6:
			color_temperature = "#0089FE"
		elif temperature > 5 and temperature < 15:
			color_temperature = "#00D4FE"
		elif temperature > 14 and temperature < 24:
			color_temperature = "#1EFEDE"
		elif temperature > 23 and temperature < 33:
			color_temperature = "#FBFBFB"
		elif temperature > 32 and temperature < 42:
			color_temperature = "#5EFE9E"
		elif temperature > 41 and temperature < 51:
			color_temperature = "#A2FE5A"
		elif temperature > 50 and temperature < 60:
			color_temperature = "#FEDE00"
		elif temperature > 59 and temperature < 69:
			color_temperature = "#FE9E00"
		elif temperature > 68 and temperature < 78:
			color_temperature = "#FE5A00"
		elif temperature > 77 and temperature < 87:
			color_temperature = "#FE1E00"
		elif temperature > 86 and temperature < 96:
			color_temperature = "#E20000"
		elif temperature > 95 and temperature < 105:
			color_temperature = "#A90000"
		elif temperature > 104 and temperature < 114:
			color_temperature = "#7E0000"
		elif temperature > 113:
			color_temperature = "#C6C6C6"
		else:
			color_temperature = "#FFFFFF"
		block_temperature += fg(color_temperature) + u"\u25A0" + res

		humidity = forecast["humidity"][i]
		if humidity < 25:
			color_humidity = "#08035D"
		elif humidity > 24 and humidity < 31:
			color_humidity = "#0D4D8D"
		elif humidity > 30 and humidity < 36:
			color_humidity = "#3070B0"
		elif humidity > 35 and humidity < 41:
			color_humidity = "#4E8ECE"
		elif humidity > 40 and humidity < 46:
			color_humidity = "#71B1F1"
		elif humidity > 45 and humidity < 51:
			color_humidity = "#80C0C0"
		elif humidity > 50 and humidity < 56:
			color_humidity = "#09FEED"
		elif humidity > 55 and humidity < 61:
			color_humidity = "#55FAAD"
		elif humidity > 60 and humidity < 66:
			color_humidity = "#94FE6A"
		elif humidity > 65 and humidity < 71:
			color_humidity = "#EAFB16"
		elif humidity > 70 and humidity < 76:
			color_humidity = "#FEC600"
		elif humidity > 75 and humidity < 81:
			color_humidity = "#FC8602"
		elif humidity > 80 and humidity < 86:
			color_humidity = "#FE3401"
		elif humidity > 85 and humidity < 91:
			color_humidity = "#EA0000"
		elif humidity > 90 and humidity < 96:
			color_humidity = "#B70000"
		elif humidity > 95 and humidity < 101:
			color_humidity = "#E10000"
		block_humidity += fg(color_humidity) + u"\u25A0" + res


		cloud_amount = forecast["cloud_amount"][i]
		if cloud_amount < 10:
			color_cloud_amount = "#003F7F"
		elif cloud_amount > 9 and cloud_amount < 20:
			color_cloud_amount = "#135393"
		elif cloud_amount > 19 and cloud_amount < 30:
			color_cloud_amount = "#2767A7"
		elif cloud_amount > 29 and cloud_amount < 40:
			color_cloud_amount = "#4F8FCF"
		elif cloud_amount > 39 and cloud_amount < 50:
			color_cloud_amount = "#63A3E3"
		elif cloud_amount > 49 and cloud_amount < 60:
			color_cloud_amount = "#77B7F7"
		elif cloud_amount > 59 and cloud_amount < 70:
			color_cloud_amount = "#9ADADA"
		elif cloud_amount > 69 and cloud_amount < 80:
			color_cloud_amount = "#AEEEEE"
		elif cloud_amount > 79 and cloud_amount < 90:
			color_cloud_amount = "#C2C2C2"
		elif cloud_amount > 89 and cloud_amount < 100:
			color_cloud_amount = "#EAEAEA"
		elif cloud_amount > 99:
			color_cloud_amount = "#FBFBFB"
		block_cloud_amount += fg(color_cloud_amount) + u"\u25A0" + res

		wind_speed = forecast["wind_speed"][i]
		if wind_speed < 6:
			color_wind_speed = "#003F7F"
		elif wind_speed > 5 and wind_speed < 12:
			color_wind_speed = "#2C6CAC"
		elif wind_speed > 11 and wind_speed < 17:
			color_wind_speed = "#63A3E3"
		elif wind_speed > 16 and wind_speed < 29:
			color_wind_speed = "#95D5D5"
		elif wind_speed > 28 and wind_speed < 46:
			color_wind_speed = "#C7C7C7"
		elif wind_speed > 45:
			color_wind_speed = "#F9F9F9"
		block_wind_speed += fg(color_wind_speed) + u"\u25A0" + res

		i += 1

	print(block_temperature)
	print(block_humidity)
	print(block_cloud_amount)
	print(block_wind_speed)
	print()

	end_time = time.time()
	total_time = end_time - start_time
	print(" ZEUS ended after", "%.1f" % total_time, "seconds")