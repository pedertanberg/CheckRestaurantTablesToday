from pandas.tseries.offsets import Hour
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, make_response
from requests.api import post
from flask_cors import CORS



day = datetime.now().date()
print(day)
test = str(day)
norwegianDayFormat = test[5:7]+"-"+test[8:10]+"-"+test[0:4]


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
CORS(app, resources={r'/*': {'origins': '*'}})

gastroplannerArray=['Majorstua','villafrogner','Grynerlokka','delicatessen', 'delicatessen2','delicatessen3','aymara', 'asia']
dinnerbookingArray =['2522','2036','355','698','1816']

numberOfSeats = 4
houseitems = []

def gastroplanner(num):
    for rest in gastroplannerArray:
        print("Gastroplanner restaurant",rest)
        name = rest
        nameurl = 'https://booking.gastroplanner.no/api/widget/bookings/sessions?date='+str(day)+'&guests='+str(num)
        jsonData =requests.get(nameurl,headers={"Referer":"https://booking.gastroplanner.no/"+str(name)+"/t", "Restaurant":str(name)})
        storage = jsonData.json()
        #for loop for determining lunch or dinner
        for typeLunchOrDinner in storage['result']:
            #print(typeLunchOrDinner)
            test = typeLunchOrDinner['hours']
            for i in test:
                #print(i)
                if i['available']==True:
                    print("available")
                    houseitems.append({str(name):i['hour']})
                else:
                    print("not available")
        print(houseitems)


def dinnerbooking(num):

    for k in dinnerbookingArray:
        nameurl = 'https://book.dinnerbooking.com/dk/en-US/book/table/day/'+str(k)+'/1'
        r_name =requests.get(nameurl)
        soup = BeautifulSoup(r_name.text)
        mydivs = soup.find_all("strong")
        #print(mydivs)
        #temparray=[]
        
        #print(mydivs[0])
        count=0
        for i in mydivs:
            #print("heere",i)
            #print("lenght", len(i))
            if count==0:
                j = str(i)
                lenght = len(j)
                rest_name = j[8:lenght-9]
                #temparray=[j[8:lenght-9]]
            count=count+1
           
            

        dinnerbookingurl = 'https://book.dinnerbooking.com/no/nb-NO/times/index/'+str(k)+'/2021-09-09/1/'+str(num)+'/0.json'

        r =requests.get(dinnerbookingurl)
        storage = r.json()
        print(storage)

        #print(storage)
        #print("1", storage['openTimes'])
        try:
            length = len(storage['openTimes'])
            #print(length)


            for i in range(0,length):
                #print(i)
                time = storage['openTimes'][i]['Time']['time']
                #print(time)
                #temparray.append(time)
                dict1 = {'Name':rest_name,'Hour':time, 'id':k}
                print(dict1)
                houseitems.append(dict1)
                
                
            
        except:
            print("no time")
        print(k)
    print(houseitems)
    #df1 = pd.DataFrame(houseitems)
    #print(df1)
    return houseitems

        
   
def sevenrooms(num):
    print(norwegianDayFormat)
    name="fyrbistronomibar"
    url="https://www.sevenrooms.com/api-yoa/availability/widget/range?venue="+str(name)+"&time_slot=18:45&party_size="+str(num)+"&halo_size_interval=16&start_date=09-08-2021&num_days=1&channel=SEVENROOMS_WIDGET"
    jsonData =requests.get(url)
    storage = jsonData.json()
    #print(storage)
    innerJSON = storage['data']['availability'][str(day)]
    for i in innerJSON :
        print(i['times'])
        availabletimes = i['times']
        for j in availabletimes:
            print(j)
            print(len(j))
            if len(j)>6:
                houseitems.append({name:j['time']})

            print("-----------------------------------------------BREAK----------------------------------------------------------")
    print(houseitems)

    
#URL = 127.0.0.1:5000/allrest?guests=4
@app.route('/allrest', methods=['GET'])
def unprotected():
    if request.method == 'GET':
        #data = []
        try:
            #print("YES")
            #post_data = request.get_json()
            #print(post_data)
            #numGuests = post_data['numberofSeats']
            base = str(request.args['guests'])
            data = gastroplanner(base)
            data1 = dinnerbooking(base)
            data2 = sevenrooms(base)
            return_data = [data,data1,data2]
            return jsonify(return_data)


        except Exception as e:
            print("NO")
            print(e)
            

    return jsonify(houseitems)


	


if __name__ == '__main__':
    #gastroplanner()
    #sevenrooms()
    app.run()



