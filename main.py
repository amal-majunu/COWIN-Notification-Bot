import requests

from datetime import datetime, timedelta
from notify_run import Notify
import time

import json

notify = Notify()
age = 50
pinCodes = ["695614","695102","695582","695581","695003","695024","695006","695125","695022","695004"]
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]


while True:
    counter = 0   

    for pinCode in pinCodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pinCode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            
            result = requests.get( URL, headers=header )
            if result.ok:
                response_json = result.json()

                flag = False
                if response_json["centers"]:            
                    if(print_flag.lower() =='y'):

                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print('Pincode: ' + pinCode)
                                    print("Available on: {}".format(given_date))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")

                                    counter = counter + 1
                                else:
                                    pass                                    
                else:
                    pass        
                            
            else:
                print("No Response!")

                
    if(counter == 0):
        print("No Vaccination slot avaliable!")
    else:
        notification_data = f"HURRY! Vaccine is availabe for age 45+"
        notify.send(notification_data)
        print("Search Completed!")

    dt = datetime.now() + timedelta(minutes=2)

    while datetime.now() < dt:
        time.sleep(1)


