#!/usr/bin/env python

import os
import sys
import requests
from datetime import datetime

# Global Parameters
LANG = 'en'

# DarkSky.net API Parameters
DS_API_HOST = 'https://api.darksky.net/forecast'
DS_API_KEY = '9643c1ba3ee12e2607db72dd5c1c1529'
DS_UNITS = 'si'

# Google Maps Geocoding API Parameters
GM_ENDPOINT = 'https://maps.google.com/maps/api/geocode/json'
GM_API_KEY = 'AIzaSyDMgdvxj2OE8VT7vnXloy7ntnJw-p78LS0'


def make_get_request(uri: str, payload):
    """
    Function to make a GET request to API Endpoint
    :param uri:
    :param payload:
    :return:
    """
    response = requests.get(uri, payload)
    if response.status_code != 200:
        return None
    else:
        return response.json()


def get_geo_data(address: str):
    """ Function to get coordinates from Google Maps Geocoding API
    :param address:
    :return:
    """
    payload = {'address': address, 'language': LANG, 'key': GM_API_KEY}
    response = make_get_request(GM_ENDPOINT, payload)

    if not response:
        return None

    data = response['results'][0]
    formatted_address = data['formatted_address']
    lat = data['geometry']['location']['lat']
    lng = data['geometry']['location']['lng']

    return {'lat': lat, 'lng': lng, 'formatted_address': formatted_address}


def get_forecast_data(lat: str, lng: str):
    """ Function to get Forecast data from DarkSky.net API
    :param lat:
    :param lng:
    :return:
    """
    uri = DS_API_HOST + '/' + DS_API_KEY + '/' + str(lat) + ',' + str(lng)
    payload = {'lang': LANG, 'units': DS_UNITS}
    response = make_get_request(uri, payload)

    if not response:
        return None

    return response['daily']


def print_daily_forecast(geo, forecast):
    """
    Function to print daily weather forecast information
    :param geo:
    :param forecast:
    """
    print('Getting Forecast for: ' + geo['formatted_address'])
    print('Weekly Summary: ' + forecast['summary'])
    print()

    seven_days_dict={}
    for day in forecast['data']:
        date = datetime.fromtimestamp(day['time'])

        if date.date() == datetime.now().date():
            day_name = 'Today'
        else:
            day_name = date.strftime("%A")

        summary = day['summary']
        temperature_min = str(round(day['temperatureMin'])) + 'ºC'
        temperature_max = str(round(day['temperatureMax'])) + 'ºC'

        per_day=[]
        per_day.append(day_name)
        per_day.append(summary)
        per_day.append(temperature_min)
        per_day.append(temperature_max)
        ddate=date.strftime('%d/%m/%Y')
        seven_days_dict[ddate]=per_day

    print(seven_days_dict)


        # print(
        #     date.strftime('%d/%m/%Y') + ' (' + day_name + '): ' +
        #     summary + ' ' + temperature_min + ' - ' + temperature_max
        # )
        # print()

    flag=0
    count=0
    two_day_dict={}
    for day in forecast['data']:
        if(flag==0):
            flag=1
            continue
        date = datetime.fromtimestamp(day['time'])
        precipIntensity = day['precipIntensity']
        precipProbability = day['precipProbability']
        try:
            precipType = day['precipType']
        except:
            precipType="null"
        dewPoint = day['dewPoint']
        windSpeed = day['windSpeed']
        windBearing = day['windBearing']
        cloudCover = day['cloudCover']
        humidity = day['humidity']
        pressure = day['pressure']
        ozone = day['ozone']
		
        if date.date() == datetime.now().date():
            day_name = 'Today'
        else:
            day_name = date.strftime("%A")

        summary = day['summary']
        temperature_min = str(round(day['temperatureMin'])) + 'ºC'
        temperature_max = str(round(day['temperatureMax'])) + 'ºC'
        date_with_day= date.strftime('%d/%m/%Y') + ' (' + day_name + ') '
        day_dict={}
        day_dict["summary"]=summary
        day_dict["temperature_min"]=temperature_min
        day_dict["temperature_max"]=temperature_max
        #day_dict["date_with_day"]=date.strftime('%d/%m/%Y') + ' (' + day_name + '): '
        day_dict["precipIntensity"]=precipIntensity
        day_dict["precipProbability"]=precipProbability
        day_dict["precipType"]=precipType
        day_dict["dewPoint"]=dewPoint
        day_dict["windSpeed"]=windSpeed
        day_dict["windBearing"]=windBearing
        day_dict["cloudCover"]=cloudCover
        day_dict["humidity"]=humidity
        day_dict["pressure"]=pressure
        day_dict["ozone"]=ozone

        count+=1
        two_day_dict[date_with_day]=day_dict

        # print (day_dict)
        # print(
        #     date.strftime('%d/%m/%Y') + ' (' + day_name + '): ' +
        #     summary + ' ' + temperature_min + ' - ' + temperature_max +' ' + str(precipIntensity)+' ' +str(precipProbability)
        # )
        # print()
        if(count==2):
            break
    print(two_day_dict)

# def print_header():
#     print('---------------------------------')
#     print('     WEATHER FORECAST 1.O       ')
#     print('---------------------------------')
#     print()


def main():
    """
    Main Function
    """
    if len(sys.argv) < 2 or DS_API_KEY is None:
        exit('Error: no location or env vars found')

    geo_data = get_geo_data(sys.argv[1])

    if not geo_data:
        exit('Error: Address not found or invalid response')

    forecast_data = get_forecast_data(geo_data['lat'], geo_data['lng'])

    if not forecast_data:
        exit('Error: Forecast not found or invalid response')

    # Print Output Forecast information
    print_header()
    print_daily_forecast(geo_data, forecast_data)


if __name__ == '__main__':
    main()