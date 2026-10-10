import requests
from datetime import datetime
import smtplib

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
MY_RECEIVE = os.environ.get("MY_RECEIVE")

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


#Your position is within +5 or -5 degrees of the ISS position.
if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (MY_LONG - 5 <= iss_longitude <= MY_LONG + 5):
    print("The satellite is close!")
    iss_close = True
else:
    print("The satellite if far")
    iss_close = False

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
my_hour = int(time_now.hour)

print(f"My hour: {my_hour} Sunrise {sunrise} Sunset {sunset}")
if ((my_hour >= sunrise or my_hour <= sunset) and iss_close):
    print("Look up")
    my_email = MY_EMAIL
    password = MY_PASSWORD

    connection = smtplib.SMTP("smtp.gmail.com",port=587)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=MY_RECEIVE,
                            msg=f"Subject:ISS is Overhead\n\n{"Look up for the Satellite!"}."
                            )
    connection.close()

#If the ISS is close to my current position (Get My position)
# and it is currently dark (Time is greater than or equal to that sunset)
# Then send me an email to tell me to look up. (Generate Email function)
# BONUS: run the code every 60 seconds. (Github Action)
