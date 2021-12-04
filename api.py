import requests
from PIL import Image 
from io import BytesIO
from io import FileIO
from flask import Flask ,render_template
import datetime
import RPi.GPIO as GPIO
import time
import urllib.request

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
    return render_template('index.html', **templateData,  birdName = birdCommonName,scienceName = birdSeintificName, order = birdOrder, family = birdFamily)
    
    # if birdCommonName == " ":
    #     birdCommonName = 'Error Bird'
        
    # return render_template('index.html', **templateData, )
                  
@webApp.route("/about", methods=['POST'])

def about():
    return render_template('index.html', birdName = birdCommonName,scienceName = birdSeintificName, order = birdOrder, family = birdFamily, bird_iamge = statci_img)
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17 , False)


# button 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down= GPIO.PUD_UP)

    while True :
        input_state = GPIO.input(18)
        if input_state == False and GPIO.output(17 , False) == GPIO.output(17 , False) and useAPI == False:
            useAPI = True
            GPIO.output(17 , True)
            button_press_cout += 1
            print(button_press_cout)
            print('Butto Presssed')
            time.sleep(0.2)
            if button_press_cout > 1 :
                # useAPI = False 
                input_state == True
                GPIO.output(17 , False)



            if not useAPI:
               
                birdCommonName = 'American Robin'
                birdSeintificName = "Turdus migratorius"
                birdOrder = 'Passeriformes'
                birdFamily = "Turdidae"
                img = Image.open("static/img/test.jpg",'r')
            
            else: 
                url = "https://ebird.org/species/surprise-me"
                ebirdApiUrl = 'https://api.ebird.org/v2/ref/taxonomy/ebird?species='
                googleApiKey= 'AIzaSyCBHsp3-5nTZmycxR_LD9d5PDY38dWrt94'
                searchEnginieId = "2899995ddd82e257d"
                ebird_headers = {
                    'x-eBirdApiToken':'cao69vorvouv'
                }


                ebird_payload = {}
                response = requests.get(url, allow_redirects = True )
                birdId= response.url.split('/')
                birdId = birdId[-1]
                ebirdApiUrl += birdId
                apiResponse = requests.request("GET", ebirdApiUrl, headers= ebird_headers, data= ebird_payload)
                birdInfo = apiResponse.text.split(',')
                birdScientificName = birdInfo[14]
                birdScientificName = birdInfo[12:]
                birdCommonName = birdInfo[15]
                birdOrder = birdInfo[22]
                birdFamily = birdInfo[23]


                # google api 
                googleUrl = "https://www.googleapis.com/customsearch/v1" 
                google_Payload = {
                        
                    'key':'AIzaSyCHHxnd59q1wuAk87VTPjZaVA5BQVE96ko',
                    'cx':'2899995ddd82e257d',
                    'q': birdCommonName,
                    'num':'1',
                    'searchType':'image'
                }

                response = requests.get(googleUrl, params = google_Payload)
                birdImgLink = extract_link(response.json())
                headers = {
                    'name': google_Payload['q'],
                    'know_as': birdInfo[14],
                    'birdorder': birdInfo[22],
                    'birdfamily':birdInfo[23],
                    'size': f'{width}x{height}',
                    'accept':'image'
                }
                response = requests.get(birdImgLink, headers)
            
                try :
                    img = Image.open(BytesIO(response.content))
                    img.save(f"static/img/bird_api_img.jpg")
                    
                    # webApp.run(host='0.0.0.0', port=80, debug=True)
                    webApp.run()    

                    # img = statci_img
                except Exception as e :
                    print('An excenption occoutre try to get an imag of the bird! not all bird ')
                    webApp.run()    
