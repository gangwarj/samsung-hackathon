from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS,cross_origin
from datetime import datetime
import time
import requests
import os
import sys

app = FlaskAPI(__name__)
CORS(app)

LANG = 'en'

# DarkSky.net API Parameters
DS_API_HOST = 'https://api.darksky.net/forecast'
DS_API_KEY = '9643c1ba3ee12e2607db72dd5c1c1529'
DS_UNITS = 'si'

# Google Maps Geocoding API Parameters
GM_ENDPOINT = 'https://maps.google.com/maps/api/geocode/json'
GM_API_KEY = 'AIzaSyDMgdvxj2OE8VT7vnXloy7ntnJw-p78LS0'

###################### FLASK APIs ###############################################


class InvalidUsage(Exception):
    def __init__(self, message):
        super(InvalidUsage, self).__init__()
        self.message = message




# @app.route("/sampleGetRequest", methods=['GET'])
# def get_request():

#     if request.method == 'GET':
#         sample_data = request.args.get('data')
        
#         modified_data = sample_data + " modify kar diya."

#         resp = {"modified_data": modified_data}

#         return resp, status.HTTP_200_OK

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
    #print('Getting Forecast for: ' + geo['formatted_address'])
    #print('Weekly Summary: ' + forecast['summary'])
    #print()

    add_summ=[]
    add_summ.append(geo['formatted_address'])
    add_summ.append(forecast['summary'])

    seven_days_dict = {}
    for day in forecast['data']:
        date = datetime.fromtimestamp(day['time'])

        if date.date() == datetime.now().date():
            day_name = 'Today'
        else:
            day_name = date.strftime("%A")

        summary = day['summary']
        temperature_min = str(round(day['temperatureMin'])) + 'ºC'
        temperature_max = str(round(day['temperatureMax'])) + 'ºC'

        per_day = []
        per_day.append(day_name)
        per_day.append(summary)
        per_day.append(temperature_min)
        per_day.append(temperature_max)
        ddate = date.strftime('%d/%m/%Y')
        seven_days_dict[ddate] = per_day

    #print(seven_days_dict)

    # print(
    #     date.strftime('%d/%m/%Y') + ' (' + day_name + '): ' +
    #     summary + ' ' + temperature_min + ' - ' + temperature_max
    # )
    # print()

    flag = 0
    count = 0
    two_day_dict = {}
    for day in forecast['data']:
        if (flag == 0):
            flag = 1
            continue
        date = datetime.fromtimestamp(day['time'])
        precipIntensity = day['precipIntensity']
        precipProbability = day['precipProbability']
        try:
            precipType = day['precipType']
        except:
            precipType = "null"
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
        date_with_day = date.strftime('%d/%m/%Y') + ' (' + day_name + ') '
        day_dict = {}
        day_dict["summary"] = summary
        day_dict["temperature_min"] = temperature_min
        day_dict["temperature_max"] = temperature_max
        # day_dict["date_with_day"]=date.strftime('%d/%m/%Y') + ' (' + day_name + '): '
        day_dict["precipIntensity"] = precipIntensity
        day_dict["precipProbability"] = precipProbability
        day_dict["precipType"] = precipType
        day_dict["dewPoint"] = dewPoint
        day_dict["windSpeed"] = windSpeed
        day_dict["windBearing"] = windBearing
        day_dict["cloudCover"] = cloudCover
        day_dict["humidity"] = humidity
        day_dict["pressure"] = pressure
        day_dict["ozone"] = ozone

        count += 1
        two_day_dict[date_with_day] = day_dict

        # print (day_dict)
        # print(
        #     date.strftime('%d/%m/%Y') + ' (' + day_name + '): ' +
        #     summary + ' ' + temperature_min + ' - ' + temperature_max +' ' + str(precipIntensity)+' ' +str(precipProbability)
        # )
        # print()
        if (count == 2):
            break
    #print(two_day_dict)
    both_dict=[]
    both_dict.append(add_summ)
    both_dict.append(seven_days_dict)
    both_dict.append(two_day_dict)
    return both_dict

@app.route("/loginUser", methods=['POST'])
def loginUser_request():
    if request.method == 'POST':

        usr = request.data.get("username")
        pwd = request.data.get("password")
    if(usr=="admin" and pwd=="12345"):
        some_data = "Success"
        resp = {"response": some_data}
        return resp, status.HTTP_200_OK
    else:
        some_data = "Failed"
        resp = {"response": some_data}
        return resp, status.HTTP_200_OK


@app.route("/processData", methods=['POST'])
def process_request():
    if request.method == 'POST':
        inp_user = request.data.get("url_field")

        geo_data = get_geo_data(inp_user)
        if not geo_data:
            exit('Error: Address not found or invalid response')

        forecast_data = get_forecast_data(geo_data['lat'], geo_data['lng'])

        if not forecast_data:
            resp['Error']=  'Forecast not found or invalid response'

        resp=print_daily_forecast(geo_data, forecast_data)
        print(resp)
        return resp, status.HTTP_200_OK



#Error handling
@app.errorhandler(404)
def page_not_found(e):
    return {"message": "Enter the correct url for endpoint."}, 404

@app.errorhandler(405)
def page_not_found(e):
    return {"message": "Type of http request is incorrect."}, 405

@app.errorhandler(500)
def page_not_found(e):
    return {"message": "Internal server error encountered. Pass the parameters in correct format."}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=False)