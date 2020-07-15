# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Zeus Weather System

Date: 29 Mar 2020
Last update: 15 Jul 2020

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
from datetime import datetime
from dateutil import tz

class Zeus:

	def __init__(self):

		self.__name = "zeus object"
		self.__url_nws = "https://forecast.weather.gov/MapClick.php?lat=25.9931&lon=-97.5607&FcstType=digitalDWML"
		self.__url_sunset = "https://api.sunrise-sunset.org/json?lat=25.9931&lng=-97.5607&formatted=0"

	def __str__(self):

		return self.__name

	def get_name(self):

		return self.__name

	def set_name(self, name):

		self.__name = name

	def get_current_status(self):

		forecast = self.get_forecast()

		time = forecast["time"][0]
		time_jd = forecast["time_jd"][0]
		dew_point = forecast["dew_point"][0]
		heat_index = forecast["heat_index"][0]
		wind_speed = forecast["wind_speed"][0]
		cloud_amount = forecast["cloud_amount"][0]
		prob_of_precip = forecast["prob_of_precip"][0]
		humidity = forecast["humidity"][0]
		wind_direction = forecast["wind_direction"][0]
		temperature = forecast["temperature"][0]
		gust = forecast["gust"][0]
		hourly_qpf = forecast["hourly_qpf"][0]

		return {"time" : time,
				"time_jd" : time_jd,
				"dew_point" : dew_point,
				"heat_index" : heat_index,
				"wind_speed" : wind_speed,
				"cloud_amount" : cloud_amount,
				"prob_of_precip" : prob_of_precip,
				"humidity" : humidity,
				"wind_direction" : wind_direction,
				"temperature" : temperature,
				"gust" : gust,
				"hourly_qpf" : hourly_qpf}

	def get_forecast(self):

		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()

		print(" Querying URL:", self.__url_sunset)
		response_sunset = requests.get(url=self.__url_sunset)
		response_sunset_status_code = response_sunset.status_code
		response_nws_content_type = response_sunset.headers["content-type"]
		response_nws_encoding = response_sunset.encoding

		parse_response_sunset = json.loads(response_sunset.text)

		sunrise_str = parse_response_sunset["results"]["sunrise"]

		if sunrise_str.endswith("+00:00"):
			sunrise_str = sunrise_str[:-6]

		sunrise_obj = Time(sunrise_str, format="isot", scale="utc")
		sunrise_obj_jd = sunrise_obj.jd

		sunset_str = parse_response_sunset["results"]["sunset"]

		if sunset_str.endswith("+00:00"):
			sunset_str = sunset_str[:-6]

		sunset_obj = Time(sunset_str, format="isot", scale="utc")
		sunset_obj_jd = sunset_obj.jd

		print(" Querying URL:", self.__url_nws)
		response_nws = requests.get(url=self.__url_nws)
		response_nws_status_code = response_nws.status_code
		response_nws_content_type = response_nws.headers["content-type"]
		response_nws_encoding = response_nws.encoding

		xml_content = response_nws.content
		root = ET.fromstring(xml_content)

		element_creation_date = root[0][0][0]
		element_data = root[1]
		element_point = root[1][0][1]
		element_area = root[1][0][2]
		element_height = root[1][0][3]
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
		conditions_list = []

		for i in range(0, 168):

			dew_point = element_dew_point[i]
			dew_point_str = dew_point.text
			dew_point_int = int(dew_point_str)
			dew_point_list.append(dew_point_int)

			heat_index = element_heat_index[i]
			heat_index_str = heat_index.text
			if heat_index_str == None:
				heat_index_int = 0
			else:
				heat_index_int = int(heat_index_str)
			heat_index_list.append(heat_index_int)

			wind_speed = element_wind_speed[i]
			wind_speed_str = wind_speed.text
			wind_speed_int = int(wind_speed_str)
			wind_speed_list.append(wind_speed_int)

			cloud_amount = element_cloud_amount[i]
			cloud_amount_str = cloud_amount.text
			cloud_amount_int = int(cloud_amount_str)
			cloud_amount_list.append(cloud_amount_int)

			prob_of_precip = element_precipitation[i]
			prob_of_precip_str = prob_of_precip.text
			prob_of_precip_int = int(prob_of_precip_str)
			prob_of_precip_list.append(prob_of_precip_int)

			humidity = element_humidity[i]
			humidity_str = humidity.text
			humidity_int = int(humidity_str)
			humidity_list.append(humidity_int)

			wind_direction = element_wind_direction[i]
			wind_direction_str = wind_direction.text
			wind_direction_int = int(wind_direction_str)
			wind_direction_list.append(wind_direction_int)

			temperature = element_temperature[i]
			temperature_str = temperature.text
			temperature_int = int(temperature_str)
			temperature_list.append(temperature_int)

			gust = element_gust[i]
			gust_str = gust.text
			if gust_str == None:
				gust_int = 0
			else:
				gust_int = int(gust_str)
			gust_list.append(gust_int)

			hourly_qpf = element_hourly_qpf[i]
			hourly_qpf_str = hourly_qpf.text
			if hourly_qpf_str == None:
				hourly_qpf_float = 0.0
			else:
				hourly_qpf_float = float(hourly_qpf_str)
			hourly_qpf_list.append(hourly_qpf_float)

		return {"time" : time_start_list, 
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

	def get_imaging(self, location):

		return

if __name__ == "__main__":

	os.system("clear")
	start_time = time.time()

	zeus = Zeus()

	print(" CTMO ZEUS Weather System v2.0")

	something = zeus.get_current_status()

	end_time = time.time()
	total_time = end_time - start_time
	print(" ZEUS ended after", "%.1f" % total_time, "seconds")
