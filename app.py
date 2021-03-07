from flask import Flask, jsonify, render_template, request

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'sample.html')


#import search
app=Flask(__name__)


import requests
import json
url ='https://vaccination-6fa56-default-rtdb.firebaseio.com/'

name=requests.get(url+'user/0/User Info/Name.json').text.replace('"','')
address=requests.get(url+'user/0/User Info/Address.json').text.replace('"','')
state=requests.get(url+'user/0/User Info/State.json').text.replace('"','')

status=requests.get(url+'user/0/Status/Eligibility.json').text.replace('"','')

gps=requests.get(url+'user/0/Profile Setting/GPS Tracker.json').text.replace('"','')
notify=requests.get(url+'user/0/Profile Setting/Notification.json').text.replace('"','')
method=requests.get(url+'user/0/Profile Setting/Preference/Method.json').text.replace('"','')
contact=requests.get(url+'user/0/Profile Setting/Preference/Email.json').text.replace('"','')

eligibility=requests.get(url+'user/0/Eligibility/Frontline Worker.json').text.replace('"','')

class SampleData:
    name = name
    address = address 

#Geopy Section
from geopy import geocoders
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.extra.rate_limiter import RateLimiter

provider_addresss=requests.get(url+'provider.json?orderBy="Address"')
address_list=json.loads(provider_addresss.text)
g_api_key = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCemq2z2xhvTpVhzbtCyz4DokkOyRgJ6TI'
gn = geocoders.GoogleV3(g_api_key)
geolocator = Nominatim(user_agent="Joyce")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def ret_2nd_ele(tuple_1):
    return tuple_1[2]

def nearby_center(user_location):
    location = geolocator.geocode(user_location)
    user_coordinate=(location.latitude, location.longitude)
    pairs=[]
    for x in range(len(address_list)):
        name=address_list[x]['Provider Info']['Name']
        address=address_list[x]['Provider Info']['Address']
        location = geolocator.geocode(address)
        x_coordinate=(location.latitude, location.longitude)
        distance=geodesic(x_coordinate, user_coordinate).miles
        pairs.append((name, address,round(distance, 2)))
    closest_name=min(pairs, key=ret_2nd_ele)[0]
    closest_address=min(pairs, key=ret_2nd_ele)[1]
    closest_distance=min(pairs, key=ret_2nd_ele)[2]
    return (closest_name,closest_address, closest_distance)

@app.route("/")
def index():
    return render_template('sample.html', data=SampleData)



@app.route("/signup", methods=['POST','GET'])
def getvalue():
    if request.method=='POST':
        name_update = request.form['name']
        email_update = request.form['email']
        password_update = request.form['password']
        state_update = request.form['state']
        update_name=requests.put(url+'user/3/User Info/Name.json', json=name_update)
        update_email=requests.put(url+'user/3/Profile Setting/Preference/Email.json', json=email_update)
        update_state=requests.put(url+'user/3/User Info/State.json', json=state_update)
        return render_template('sample.html',data=SampleData)
    else:
        return render_template('signup.html')

@app.route("/calendar", methods=['POST','GET'])
def getvalue2():
    if request.method=='POST':
        address_update = request.form['address']
        update_address=requests.put(url+'user/3/User Info/Address.json', json=address_update)
        ((closest_name,closest_address, closest_distance))=nearby_center(address_update)
        return render_template('calendar_distance.html',closest_name=closest_name,closest_address=closest_address,closest_distance=closest_distance)
    else:
        return render_template('calendar.html')

if __name__=="__main__":
    app.run(debug=True)