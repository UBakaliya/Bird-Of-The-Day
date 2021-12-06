import requests
from PIL import Image 
from io import BytesIO
from io import FileIO
from flask import Flask, render_template, request, jsonify, redirect
import datetime
from random import randint
import RPi.GPIO as GPIO
import time
import urllib.request



# app = Flask(__name__)
useAPI = False 
apiResponse = ''
birdCommonName = ''
birdSeintificName  = ''
birdOrder = ''
birdFamily = ''

height = 10
width = 10
button_press_cout = 0 
webApp = Flask(__name__)

#since we are just returning a jsonified dictionary and not a usable html page, we don't need to make an imgandtitle html file
@app.route('/imgandtitle', methods=['GET', 'POST'])
def apiCall():
    def extract_link(json):
    return json["items"][0]["link"]

@webApp.route('/')
def home():

    global birdCommonName
    global birdSeintificName
    global birdOrder
    global birdFamily
    curr_date = datetime.datetime.now()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'Bird of the day!',
        'time': timeString,
                
                        
    }
    # return render_template('index.html', **templateData,  birdName = birdCommonName,scienceName = birdSeintificName, order = birdOrder, family = birdFamily)
  

    value = randint(0, 100)
    #random photo url could 
    base_url = f'https://picsum.photos/{value}'
       
    #Since we are replacing an attribute all we need to do is get the new url as a string.
    url = base_url
    #use full h2 tag since you're replacing the html object with a new one
    title = f'<h2 id=title >{value}</h2>'

    Data = {
        'url': url,
        'title': title

    }

    #return your json file

    return jsonify(**Data)   
    


@app.route('/', methods = ['GET', 'POST'])

#define app function

def index():
    Hello = "Hello World!"
    value = randint(0, 100)
        
    url = f'https://picsum.photos/{value}'
       
    print(url)
    Data = {
        'title' : Hello,
        'img' : url
    }

    return render_template('index.html', **Data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)