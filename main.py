# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import datetime as dt
import pandas as pd
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# ---------------------------- Create a Dictionary for Birthdays CSV------------------------------- #
birthday = pd.read_csv("birthdays.csv")
birthday_dict = {
    key: group
    for key, group in birthday.groupby(["month", "day"])
}

# ---------------------------- Select Random Letter ------------------------------- #
def random_letter(bday_name):
    path = "./letter_templates/"
    letter = random.choice(os.listdir(path))
    rand_path = path + letter
    with open(rand_path) as file:
        contents = file.read()
        new_letter = contents.replace('[NAME]', bday_name)
    return new_letter


# ---------------------------- Check Date and Time ------------------------------- #
# This function returns an array of names, and emails
def date_verify():
    today = dt.datetime.now()
    today_tuple = (today.month, today.day)
    return today_tuple


# ---------------------------- Generate Email ------------------------------- #

def gen_email(bday_addr, bday_name, bday_letter):
    my_email = "b6800528@gmail.com"
    password = "wwqlhlkddidsjpki"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=bday_addr,
                            msg=f"Subject:Happy Birthday! {bday_name}\n\n{bday_letter}"
                            )


# ---------------------------- Main ------------------------------- #
try:
    bday_person = birthday_dict.get(date_verify())
    for (index, row) in bday_person.iterrows():
        gen_email(bday_addr=row.email, bday_name=row['name'], bday_letter=random_letter(row['name']))
except AttributeError:
    print(f"No birthdays today {dt.datetime.now()}. Exiting.")
    exit(0)
