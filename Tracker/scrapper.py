from selenium import webdriver
import time
import os
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")



#browser = webdriver.Chrome("C:/Users/Lenovo/Desktop/chromedriver_win32/chromedriver.exe",options=options)
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)



def ads(lat,lang):
    Dict = {}
    url = "http://maps.google.com/maps?q="+ str(lat) +"," + str(lang)

    browser.get(url)
    time.sleep(5)
    review_text = browser.find_elements_by_class_name("widget-pane-link")
    #print(review_text)
    address = [a.text for a in review_text][2]
    #print(address)
    #pincode = address[-6:]

    index = address[::-1].find(',')
    pincode = address[-13:-index - 1]
    country = address[-index + 1:]
    if(pincode.isdigit()):
        #print("YES")
        #print(pincode)
        Dict["address"] = address[:-index-8]
        print(address[:index])
        Dict["pincode"] = pincode
        Dict["country"] = country
        Dict["url"] = url
    else:
        Dict["address"] = address

    return Dict
    browser.quit()


def dir_time(cur_lat,cur_lang,dest_lat,dest_lang):
    Dict = {}
    url = "https://www.google.co.in/maps/dir/"+str(cur_lat)+","+str(cur_lang)+"/"+str(dest_lat)+",+"+str(dest_lang)+"/"
    browser.get(url)
    time.sleep(2)
    dist = browser.find_elements_by_class_name("section-directions-trip-distance")
    tme = browser.find_elements_by_class_name("section-directions-trip-duration")
    distance = [a.text for a in dist][0]
    duration = [a.text for a in tme][0]
    print(distance)
    print(duration)
    Dict["distance"] = distance
    Dict["duration"] = duration
    browser.quit()


#dir_time(22.355,73.1640,24.355,75.1640)