from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS,cross_origin
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
#from bs4 import BeautifulSoup
#import PyPDF2
#from summarize import summarize
#import requests
#import pdfx
import codecs
import time 
import requests
import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


app = FlaskAPI(__name__,static_folder="fig")
CORS(app)

_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'
_key =  '0202f67e349948c0896d4034d84dd1be' #Here you have to paste your primary key
uri_base = 'westcentralus.api.cognitive.microsoft.com'
_maxNumRetries = 10
###################### FLASK APIs ###############################################


class InvalidUsage(Exception):
    def __init__(self, message):
        super(InvalidUsage, self).__init__()
        self.message = message


def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
        
    return result

def getOCRTextResult( operationLocation, headers ):
    """
    Helper function to get text result from operation location

    Parameters:
    operationLocation: operationLocation to get text result, See API Documentation
    headers: Used to pass the key information
    """

    retries = 0
    result = None

    while True:
        response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

    return result

def showResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""
    img = img[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(img, aspect='equal')

    lines = result['recognitionResult']['lines']

    for i in range(len(lines)):
        words = lines[i]['words']
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text']
            x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
            y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
            line = Line2D(x, y, linewidth=3.5, color='red')
            ax.add_line(line)
            ax.text(tl[0], tl[1] - 2, '{:s}'.format(text),
            bbox=dict(facecolor='blue', alpha=0.5),
            fontsize=14, color='white')

    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    #plt.show()
    plt.savefig('fig/img1.png')


# @app.route("/sampleGetRequest", methods=['GET'])
# def get_request():

#     if request.method == 'GET':
#         sample_data = request.args.get('data')
        
#         modified_data = sample_data + " modify kar diya."

#         resp = {"modified_data": modified_data}

#         return resp, status.HTTP_200_OK


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
        urlImage = request.data.get("url_field")
        #print(urlImage)
        # Computer Vision parameters
        params = { 'handwriting' : 'true'}
        
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/json'
        json = { 'url': urlImage }
        data = None

        result = None
        operationLocation = processRequest(json, data, headers, params)
        if (operationLocation != None):
            headers = {}
            headers['Ocp-Apim-Subscription-Key'] = _key
            while True:
                time.sleep(1)
                result = getOCRTextResult(operationLocation, headers)
                if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                    break
            
        if result is not None and result['status'] == 'Succeeded':
            # Load the original image, fetched from the URL
            arr = np.asarray( bytearray( requests.get( urlImage ).content ), dtype=np.uint8 )
            img = cv2.cvtColor( cv2.imdecode( arr, -1 ), cv2.COLOR_BGR2RGB )
            showResultOnImage( result, img )
        
        #print(result)
        openthis = "/fig/img1.png"
        resp = {'result': result, 'figure':openthis}
        return resp, status.HTTP_200_OK



@app.route("/processImg", methods=['POST'])
def process_img():

    if request.method == 'POST':
        urlImage = request.data.get("url_field")
        
        headers = {
        # Request headers.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': _key,
        }

        params = urllib.parse.urlencode({
            # Request parameters. All of them are optional.
            'visualFeatures': 'Categories,Description,Color',
            'language': 'en',
            })
        

        body = "{'url': '"+urlImage+"'}"
    
        reader = codecs.getreader("utf-8")

        try:
            # Execute the REST API call and get the response.
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            
            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(data)
            #print ("Response:")
            #print (json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()
        
        except Exception as e:
            print('Error:')
            print(e)

    return data, status.HTTP_200_OK



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
    app.run(host='0.0.0.0', port=5050, debug=False)