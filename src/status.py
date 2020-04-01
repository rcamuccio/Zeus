# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Richard Camuccio
# 28 Mar 2020
#
# Last update: 29 Mar 2020
#
# Zeus - Current status monitor
#

from datetime import datetime
from dateutil import tz
import json
import os
import requests
import time
import xml.etree.ElementTree as ET

url_nws = "https://forecast.weather.gov/MapClick.php?lat=25.9931&lon=-97.5607&FcstType=digitalDWML"
url_sunset = "https://api.sunrise-sunset.org/json?lat=25.9931&lng=-97.5607&formatted=0"

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

run = True
while run == True:

	os.system("clear")
	print(" CTMO ZEUS Weather System")
	print(" Current Status Monitor")
	print("------------------------------------------------------------")
	print(" Querying URL:", url_nws)
	response_nws = requests.get(url=url_nws)
	print(" Response status code:", response_nws.status_code)
	print(" Response content type:", response_nws.headers["content-type"])
	print(" Response encoding:", response_nws.encoding)
	print("------------------------------------------------------------")
	print(" Querying URL:", url_sunset)
	response_sunset = requests.get(url=url_sunset)
	print(" Response status code:", response_sunset.status_code)
	print(" Response content type:", response_sunset.headers["content-type"])
	print(" Response encoding:", response_sunset.encoding)
	print("------------------------------------------------------------")

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

	latitude = element_point.attrib["latitude"]
	longitude = element_point.attrib["longitude"]
	print(" Point:", (float(latitude), float(longitude)), "at", element_area.text)
	print(" Mean sea level:", element_height.text, "ft")

	print("------------------------------------------------------------")

	time_start_str = element_time_layout[1].text
	time_start_datetime = datetime.strptime(time_start_str, "%Y-%m-%dT%H:%M:%S-05:00")
	print(" Reference date:", str(time_start_datetime) + "-05:00")

	parse_response_sunset = json.loads(response_sunset.text)

	astronomical_twilight_begin_str = parse_response_sunset["results"]["astronomical_twilight_begin"]
	astronomical_twilight_begin_datetime = datetime.strptime(astronomical_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
	astronomical_twilight_begin_datetime_utc = astronomical_twilight_begin_datetime.replace(tzinfo=from_zone)
	astronomical_twilight_begin_datetime_local = astronomical_twilight_begin_datetime_utc.astimezone(to_zone)
	print("   Begin astronomical twilight:", astronomical_twilight_begin_datetime_local)

	nautical_twilight_begin_str = parse_response_sunset["results"]["nautical_twilight_begin"]
	nautical_twilight_begin_datetime = datetime.strptime(nautical_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
	nautical_twilight_begin_datetime_utc = nautical_twilight_begin_datetime.replace(tzinfo=from_zone)
	nautical_twilight_begin_datetime_local = nautical_twilight_begin_datetime_utc.astimezone(to_zone)
	print("   Begin nautical twilight:", nautical_twilight_begin_datetime_local)

	civil_twilight_begin_str = parse_response_sunset["results"]["civil_twilight_begin"]
	civil_twilight_begin_datetime = datetime.strptime(civil_twilight_begin_str, "%Y-%m-%dT%H:%M:%S+00:00")
	civil_twilight_begin_datetime_utc = civil_twilight_begin_datetime.replace(tzinfo=from_zone)
	civil_twilight_begin_datetime_local = civil_twilight_begin_datetime_utc.astimezone(to_zone)
	print("   Begin civil twilight:", civil_twilight_begin_datetime_local)

	sunrise_str = parse_response_sunset["results"]["sunrise"]
	sunrise_datetime = datetime.strptime(sunrise_str, "%Y-%m-%dT%H:%M:%S+00:00")
	sunrise_datetime_utc = sunrise_datetime.replace(tzinfo=from_zone)
	sunrise_datetime_local = sunrise_datetime_utc.astimezone(to_zone)
	print(" Sunrise:", sunrise_datetime_local)

	solar_noon_str = parse_response_sunset["results"]["solar_noon"]
	solar_noon_datetime = datetime.strptime(solar_noon_str, "%Y-%m-%dT%H:%M:%S+00:00")
	solar_noon_datetime_utc = solar_noon_datetime.replace(tzinfo=from_zone)
	solar_noon_datetime_local = solar_noon_datetime_utc.astimezone(to_zone)
	print(" Solar noon:", solar_noon_datetime_local)

	sunset_str = parse_response_sunset["results"]["sunset"]
	sunset_datetime = datetime.strptime(sunset_str, "%Y-%m-%dT%H:%M:%S+00:00")
	sunset_datetime_utc = sunset_datetime.replace(tzinfo=from_zone)
	sunset_datetime_local = sunset_datetime_utc.astimezone(to_zone)
	print(" Sunset:", sunset_datetime_local)

	civil_twilight_end_str = parse_response_sunset["results"]["civil_twilight_end"]
	civil_twilight_end_datetime = datetime.strptime(civil_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
	civil_twilight_end_datetime_utc = civil_twilight_end_datetime.replace(tzinfo=from_zone)
	civil_twilight_end_datetime_local = civil_twilight_end_datetime_utc.astimezone(to_zone)
	print("   End civil twilight:", civil_twilight_end_datetime_local)

	nautical_twilight_end_str = parse_response_sunset["results"]["nautical_twilight_end"]
	nautical_twilight_end_datetime = datetime.strptime(nautical_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
	nautical_twilight_end_datetime_utc = nautical_twilight_end_datetime.replace(tzinfo=from_zone)
	nautical_twilight_end_datetime_local = nautical_twilight_end_datetime_utc.astimezone(to_zone)
	print("   End nautical twilight:", nautical_twilight_end_datetime_local)

	astronomical_twilight_end_str = parse_response_sunset["results"]["astronomical_twilight_end"]
	astronomical_twilight_end_datetime = datetime.strptime(astronomical_twilight_end_str, "%Y-%m-%dT%H:%M:%S+00:00")
	astronomical_twilight_end_datetime_utc = astronomical_twilight_end_datetime.replace(tzinfo=from_zone)
	astronomical_twilight_end_datetime_local = astronomical_twilight_end_datetime_utc.astimezone(to_zone)
	print("   End astronomical twilight:", astronomical_twilight_end_datetime_local)

	print("------------------------------------------------------------")

	temperature = element_temperature[0].text
	temperature = int(temperature)
	print(" Temperature:", temperature, "F")

	dew_point = element_dew_point[0].text
	print(" Dew point:", dew_point, "F")

	heat_index = element_heat_index[0].text
	if heat_index == "None":
		heat_index = 0
	print(" Heat index:", heat_index, "F")

	print("------------------------------------------------------------")

	wind_speed = element_wind_speed[0].text
	print(" Wind speed:", wind_speed, "mph")

	wind_direction = element_wind_direction[0].text
	print(" Wind direction:", wind_direction, "deg")

	gust = element_gust[0].text
	if gust == None:
		gust = 0
	print(" Gust:", gust, "mph")

	print("------------------------------------------------------------")

	humidity = element_humidity[0].text
	print(" Humidity:", str(humidity) + "%")

	cloud_amount = element_cloud_amount[0].text
	print(" Cloud amount:", str(cloud_amount) + "%")

	precipitation = element_precipitation[0].text
	print(" Precipitation:", str(precipitation) + "%")

	hourly_qpf = element_hourly_qpf[0].text
	print(" Hourly QPF:", hourly_qpf, "in")

	print("------------------------------------------------------------")

	try:
		conditions_weather_type_1 = element_conditions[0][0].attrib["weather-type"]
		conditions_coverage_1 = element_conditions[0][0].attrib["coverage"]
		print(" Conditions:", conditions_weather_type_1, "(" + str(conditions_coverage_1) + ")")

	except IndexError:
		print(" Conditions: none")

	try:
		conditions_weather_type_2 = element_conditions[0][1].attrib["weather-type"]
		conditions_coverage_2 = element_conditions[0][1].attrib["coverage"]
		print(" Conditions:", conditions_weather_type_2, "(" + str(conditions_coverage_2) + ")")

	except IndexError:
		print(" Conditions: none")

	print()
	print(" Pausing for one minute ...")
	time.sleep(60)