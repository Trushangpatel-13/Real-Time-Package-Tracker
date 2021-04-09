from django.shortcuts import render
import pyrebase
from django.contrib import auth
from datetime import datetime
from .scrapper import ads
import time

config = {
  "apiKey": "AIzaSyDxQyfFPYsD27uHpOPGp9FC2VxlxVSEmsA",
  "authDomain": "news-471f1.firebaseapp.com",
  "databaseURL": "https://news-471f1.firebaseio.com",
  "projectId": "news-471f1",
  "storageBucket": "news-471f1.appspot.com",
  "messagingSenderId": "579352149196",
  "appId": "1:579352149196:web:75c2b568d65623cdbed669",
  "measurementId": "G-YT4FLNBL4N"
};

firebase = pyrebase.initialize_app(config)

authO = firebase.auth()
db = firebase.database()

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def map(request):
    #data = {}
    location_data = {}
    address_data = {}
    tracking_id = request.GET.get('tracking_id')
    time.sleep(2)
    try:
        package = db.child('Packages').child(str(tracking_id)).get()

    except:
        Invalid = "Invalid Tracking Id"
        return render(request,"map.html",{"msg":Invalid})
    package_data = package.val()
    if(package_data != None):
        package = db.child('Drivers').child(str(package_data['Transporter']).lower()).child('Category').get()
        if(package.val() == "Warehouse Owner"):
            package_data['Trans_Cat'] = "In Sorting Facility"
        elif(package.val() == "Transporter"):
            package_data['Trans_Cat'] = "In Truck"
        current = package_data['TWID']
        package = db.child('Location').child(str(package_data['Transporter']).lower()).get()
        location_data = package.val()
        location_data['Timestamp'] = datetime.utcfromtimestamp(location_data['Timestamp']/1000)
        location_data['Pms_Date'] = datetime.utcfromtimestamp(package_data['Pms_Date'])
        package = db.child('Drivers').child(str(package_data['Transporter']).lower()).child('Name').get()
        package_data["Transporter_Name"] = package.val()
        for item in range(0,len(package_data['Inter_Loc'])):
            if(package_data['Inter_Loc'][item] == current):
                item += 1
                break
        if(item <= len(package_data['Inter_Loc'])):
            package_data['upcoming'] =  package_data['Inter_Loc'][item]
        else:
            package_data['upcoming'] = "Out For Delivery"

        #for item in package.each:
        #    print(item.val)
        driver_obj = db.child('Drivers').get()
        driver = driver_obj.val()
        #for user in driver_obj.each():
        #    print(user.key())
        #    print(user.val())
        address_data = ads(location_data['Lat'],location_data['Long'])
        #distance_data =
        #print(address_data)
        package_data.update(location_data)
        package_data.update(address_data)
        #print(location_data)
        #print(package_data)
    return render(request,"map.html",{"data":package_data})

def service(request):
    return render(request,"service.html")

def signIn(request):
    return render(request,"login.html")

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authO.sign_in_with_email_and_password(email,password)

    except:
        msg = "Invalid Credentials"
        return render(request,"login.html",{"msg":msg})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request,"map.html",{"msg":email})

def logout(request):
    auth.logout(request)
    return render(request,"index.html")
