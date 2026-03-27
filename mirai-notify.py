import os
import time
import requests
from smtplib import SMTP

nameStatus = {
    "261": "unavailable",
    "1": "offhours",
    "2": "online",
    "3": "limited",
    "4": "refresh",
    "5": "offline",
    "6": "unknown"
}

def main(args):
    if len(args) < 7:
        print("Usage: python3 mirai-notify.py <stationID> <35|70> <smtp_host> <smtp_user> <smtp_password> <email1> [email2] ...")
        return

    oldStationStatus = "6"
    stationID = args[1]
    H35 = args[2] == "35"
    host = args[3]
    user = args[4]
    pwd = args[5]
    mailList = args[6:]

    while True:
        r = requests.get("https://m.h2fcp.org/sites/default/files/nocache/soss2-status-mini.json")

        if r.status_code != 200:
            print("Error fetching data")
            continue

        json = r.json()

        for station in json:
            if station["s"] == stationID:
                print(station)
                stationStatus = "261" if station["ds"] == "261" else (station["s3"] if H35 else station["s7"])
                stationCapacity = station["c3"] if H35 else station["c7"]
                break
        
        if stationStatus != oldStationStatus:
            oldStationStatus = stationStatus
            
            print(f"Station {stationID} is now {nameStatus.get(stationStatus, 'unknown')}")
            sendEmail(host, user, pwd, mailList, f"Hydrogen station is now {nameStatus.get(stationStatus, 'unknown')}", f"Status of {'35' if H35 else '70'}MPa pump with station ID {stationID} is now {nameStatus.get(stationStatus, 'unknown')} with {stationCapacity}kg stored.")
        
        time.sleep(300)

def sendEmail(host, user, pwd, mailList, subject, body):
    try:
        with SMTP(host, 587) as smtp:
            smtp.starttls()
            smtp.login(user, pwd)

            for mail in mailList:
                print(f"    Sending email to {mail}")
                msg = f"Subject: {subject}\n\n{body}"
                smtp.sendmail(user, mail, msg)
    except:
        print("Error sending email")

if __name__ == "__main__":
    main(os.sys.argv)