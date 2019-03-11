import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def distance(data, zipA, zipB):
    infoA = data.loc[data["Zipcode"] == int(zipA)]
    infoB = data.loc[data["Zipcode"] == int(zipB)]
    x1, y1 = float(infoA["Lat"]), float(infoA["Long"])
    x2, y2 = float(infoB["Lat"]), float(infoB["Long"])
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def closestMcD(data, shakeZips, home):
    closest = ''
    dist = 1E10
    for zipcode in shakeZips:
        if zipcode == home:
            return "your own zipcode, dummy!"
        zToHome = distance(data, zipcode, home)
        if zToHome < dist:
            dist = zToHome
            closest = zipcode
    return closest

def hasShamrockShake(zipcode):
    elem = driver.find_element_by_name("zip")
    elem.clear()
    elem.send_keys(str(zipcode), Keys.RETURN)
    time.sleep(1.5)                                               # loading time
    overlay = driver.find_element_by_id("resultserroroverlay")
    if "ng-hide" in str(overlay.get_attribute("class")):
        return True
    else:
        driver.find_element_by_id("resultserrorbutton").click()   # clears error message
        return False

def main():
    data = pd.read_csv("zipcode-database.csv")
    stateData = data.loc[data["State"] == STATE]

    with open('shamZips.txt', 'w') as file:
        file.write('Has Shamrock Shake\n')

    shakeZips = []
    print(f"{STATE} has {len(stateData['Zipcode'])} zipcodes...")
    with open('shamZips.txt', 'a') as file:
        for zipcode in stateData["Zipcode"]:
            print(f"Checking zip: {zipcode}", end=' ')
            if hasShamrockShake(zipcode):
                print("- Found!")
                file.write(f'{zipcode},\n')
                shakeZips.append(zipcode)
            else:
                print("\n", end='')

    if shakeZips:
        closest = closestMcD(data, shakeZips, HOME)
        print(f"The closest Shamrock Shake McDonalds to {HOME} is in {closest}")

    driver.close()

if(__name__=="__main__"):
    MCDFINDER = 'https://mcdfinder.com/#/'
    STATE = 'CA'
    HOME  = '90210'
    headless = False # running headless causes ugly error messages from McDonalds' website

    if headless:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Chrome()

    driver.get(MCDFINDER)

    t0 = time.clock()
    main()
    t1 = time.clock()
    print(f"Done. Finished in {t1 - t0}.")