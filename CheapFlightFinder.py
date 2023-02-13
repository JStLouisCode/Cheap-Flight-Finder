#Jared St.Louis

#Cheap Flight Finder

#Imports (selenium)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#Imports (others)
import time
import pandas as pd
import schedule

#Imports (Email)
import os
import smtplib #emails
from email.message import EmailMessage

#Main Script

departure_flight_inputs = {'Departure': " YYZ", 'Arrival': " BOS", 'Date': "May 10, 2023"}

return_flight_inputs = {'Departure': " BOS", 'Arrival': " YYZ", 'Date': "May 14, 2023"}

#Function Definitions
def find_cheapest_flights(flight_info):
    PATH = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=PATH)
    
    #get values from keys of the flight information and assign them to a variable
    flying_from = flight_info['Departure']
    flying_to = flight_info['Arrival']
    trip_date = flight_info['Date']
    
    #Go to Expedia
    driver.get('https://expedia.com')
    
    #Get xPATH
    flight_xpath = '//a[@aria-controls="wizard-flight-pwa"]'
    
    #Click on Flights
    flight_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flight_xpath))) #waits (5 secs) for element on page to load before retrieving it
    flight_element.click()
    time.sleep(0.2)
    
    #Click on One-Way
    oneway_xpath = '//a[@aria-controls="wizard-flight-tab-oneway"]'
    oneway_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, oneway_xpath))) 
    oneway_element.click()
    time.sleep(0.2)
    
    #Part 1: Flying From, Flying To, Departure Date, Return Date
    
    #**********************  Start Of Leaving From Portion  **********************
    flying_from_xpath = '//button[@aria-label="Leaving from"]'
    flying_from_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flying_from_xpath)))
    flying_from_element.clear
    flying_from_element.click() #Click on Leaving from box
    time.sleep(1)
    flying_from_element.send_keys(flying_from) #inputs the airport passenger is leaving from
    
    time.sleep(1)
    flying_from_element.send_keys(Keys.DOWN, Keys.RETURN) #goes down list for an item and clicks enter to input that value
    #**********************  Complete Leaving From Portion  **********************
    
    
    
    #**********************  Start Of Going To Portion  **********************
    flying_to_xpath = '//button[@aria-label="Going to"]'
    flying_to_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, flying_to_xpath)))
    flying_to_element.clear
    flying_to_element.click() #Click on Going to box
    time.sleep(2)
    flying_to_element.send_keys(flying_to) #inputs the airport passenger is going to
    
    time.sleep(2)
    flying_to_element.send_keys(Keys.DOWN, Keys.RETURN) 
    #**********************  Complete Going To Portion  ********************** 
    
    
    
    #**********************  Complete Departure Date Portion  **********************
    departing_box_xpath = '//button[contains(@aria-label,"Departing")]'
    depart_box_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, departing_box_xpath)))
    depart_box_element.click() #Click on departure box
    time.sleep(2)
    
    #Find the current date. (WILL arrow to it)
    trip_date_xpath = '//button[contains(@aria-label,"{}")]'.format(trip_date)
    departing_date_element = ""
    
    #loops until finds the date
    while departing_date_element == "":
        try:
            departing_date_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, trip_date_xpath))) #looks for date on page for up to 3 secs
            departing_date_element.click() #Click on departure date
            
        #when/if 3 secs passed and date is not found, will use xpath of arrow in calender to click to the next month, etc...
        except TimeoutException: 
            departing_date_element = ""
            next_month_xpath = '//button[@data-stid="date-picker-paging"][2]' #xpath of (next month) arrow in calendar 
            next_month_element = driver.find_element(By.XPATH, next_month_xpath)
            next_month_element.click()#Click on next month
            time.sleep(1)
    depart_date_done_xpath = '//button[@data-stid="apply-date-picker"]'
    depart_date_done_element = driver.find_element(By.XPATH, depart_date_done_xpath)
    depart_date_done_element.click() #Click on Done button on Expedia Calendar
    #**********************  Complete Departure Date Portion  **********************  
    
    
    
    #**********************  Click Search  **********************
    search_button_xpath = '//button[@data-testid="submit-button"]'
    search_button_element = driver.find_element(By.XPATH, search_button_xpath)
    search_button_element.click()
    time.sleep(21) #lets the page load properly
    #**********************  Click Search  **********************
    
    
    
    #Part 2: Setting Conditions for our flight
    
    
    #**********************  Check for Nonstop Flights Sorted by Lowest Price  **********************
    nonstop_flight_xpath = '//input[@id="stops-0"]'
    one_stop_flight_xpath = '//input[@id="stops-1"]'
    
    if len(driver.find_elements_by_xpath(By.XPATH, nonstop_flight_xpath)) > 0:
        driver.find_element_by_xpath(By.XPATH, nonstop_flight_xpath).click()
        time.sleep(5)
        
        #Check if there are available flights
        available_flights = driver.find_elements_by_xpath("//span[contains(text(),'Select and show fare information ')]")
        if len(available_flights) > 0:
            if len(available_flights) == 1: #dont have to sort by prices here
                flights = [(item.text.split(",")[0].split('for')[-1].title(),
                            item.text.split(",")[1].title().replace("At",":"),
                            item.text.split(",")[2].title().replace("At",":"),
                            item.text.split(",")[3].title().replace("At",":")) for item in available_flights[0:5]]
                
            else:
                #Sort by lowest prices
                driver.find_element_by_xpath('//option[@data-opt-id="PRICE_INCREASING"]').click()
                time.sleep(5)
                flights = [(item.text.split(",")[0].split('for')[-1].title(),
                            item.text.split(",")[1].title().replace("At",":"),
                            item.text.split(",")[2].title().replace("At",":"),
                            item.text.split(",")[3].title().replace("At",":")) for item in available_flights[0:5]]
                
            print("Conditions satisfied for: {}:{}, {}:{}, {}:{}".format("Departure",flying_from,"Arrival",flying_to,"Date",trip_date))
            driver.quit()
            return flights
        
    else:
        print('Not all conditions could be met for the following: "{}:{}, {}:{}, {}:{}'.format("Departure",flying_from,"Arrival",flying_to,"Date",trip_date))
        driver.quit()
        return []
    #**********************  Check for Nonstop Flights Sorted by Lowest Price  **********************
    
    
    
    #**********************  Send the Email With Relevant Flight Information  **********************
def send_email():
    #Get return values
    departing_flights = find_cheapest_flights(departure_flight_inputs)
    return_flights = find_cheapest_flights(return_flight_inputs)
    
    #Put it into a dataframe to visualize this more easily
    df = pd.DataFrame(departing_flights + return_flights)
    
    if not df.empty: #Only send an email if we have actual flight info
        email_sender = 'YOUR EMAIL'
        password= 'YOUR PASSWORD'
        email_receiver = 'SOMEONES EMAIL'
        
        msg = EmailMessage()
        
        msg['Subject'] = "Python Flight Info! {} --> {}, Departing: {}, Returning: {}".format(departure_flight_inputs['Departure'], departure_flight_inputs['Arrival'], departure_flight_inputs['Date'],return_flight_inputs['Date'])
        
        msg['From'] = email_sender
        msg['To'] = email_receiver
        
        msg.add_alternative('''\
            <!DOCTYPE html>
            <html>
                <body>
                    {}
                </body>
            </html>'''.format(df.to_html()), subtype="html")
    
            
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(email_sender,password)
            smtp.send_message(msg)
            
                    
schedule.clear()
schedule.every(30).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
    #**********************  Send the Email With Relevant Flight Information  **********************


                
    
    
    
    
    
    
    
