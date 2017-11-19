
# coding: utf-8

# In[18]:



########### Python 3.6 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json



# In[19]:


###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '0202f67e349948c0896d4034d84dd1be'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'



# In[20]:



headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})



# In[23]:


# Replace the three dots below with the URL of a JPEG image of a celebrity.
body = "{'url':'https://www.burgerfuel.com/uploads/cache/home_page_burger/uploads/media/57d1edb82fda3/bfd-chicken-bacon-backfire-500px-09-16-crop.png'}"

import codecs
reader = codecs.getreader("utf-8")


# In[24]:


try:
    # Execute the REST API call and get the response.
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf8')

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)

####################################

