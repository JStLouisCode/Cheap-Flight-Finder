# Cheap-Flight-Finder

# Description
The "Cheap Flight Finder" program is a Python script that uses the Selenium module to automate the process of finding the cheapest flights available on Expedia. The program inputs the departure airport, destination airport, and date of travel and returns the cheapest flights on Expedia for a one-way trip. The program also sends an email with the flight details.

# Requirements
The following modules must be installed for this program to run:

selenium
pandas
schedule
os
smtplib
email.message
The program requires Google Chrome to be installed and the Chrome driver to be downloaded and installed in /usr/local/bin/. You can download the Chrome driver from the following link: https://chromedriver.chromium.org/downloads.

# Usage
Open the file cheap_flight_finder.py in a Python IDE.
Input the departure_flight_inputs and return_flight_inputs dictionaries at the beginning of the script with the necessary details for your trip.
Run the script.
The program will launch Google Chrome, navigate to Expedia, input your flight information, and return the cheapest flights available. The program will also send an email with the flight details.

Note: You must have a Google account to use the email feature.
