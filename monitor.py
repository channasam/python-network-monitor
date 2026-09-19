import telebot
import subprocess
import time
from config import BOT_TOKEN, CHAT_ID
import os
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)


def check_ping(ip_address):

    try:

        subprocess.check_output(

            ["ping", "-n", "1", "-w", "1000", ip_address], stderr=subprocess.STDOUT

        )

        return True

    except subprocess.CalledProcessError:

        return False


def send_alert(message):

    bot.send_message(CHAT_ID, message)


devices = [

    {"name":"AC Pro F-Floor", "ip": "192.168.10.254"},
    {"name": "AC Lr Stair", "ip": "192.168.10.55"},
    {"name": "AC Pro GR-Floor", "ip": "192.168.10.35"},

]

previous_status = {}

for device in devices:

    previous_status[device["ip"]] = None


def monitor_device(device, previous_status):

    current_status = check_ping(device["ip"])

    if previous_status[device["ip"]] is None:

        previous_status[device["ip"]] = current_status

    elif current_status != previous_status[device["ip"]]:

        if current_status:

            message = (

                f"🟢 NETWORK RESTORED\n\n" 
                f"Device: {device['name']}\n" 
                f"IP: {device['ip']}\n" 
                f"Status: ONLINE"

            )

        else:

            message = (

                f"🚨 NETWORK ALERT\n\n" 
                f"Device: {device['name']}\n" 
                f"IP: {device['ip']}\n" 
                f"Status: OFFLINE"

            )

        send_alert(message)

    previous_status[device["ip"]] = current_status


    if current_status:

        print(f"{device['name']:<20} {device['ip']:<16} ONLINE")

    else:

        print(f"{device['name']:<20} {device['ip']:<16} OFFLINE")


while True:

    os.system("cls")
    
    current_time = datetime.now().strftime("%H:%M:%S")

    print(f"\n{[current_time]} Checking device...\n")

    print(f"{'Device':<20} {'IP Address':<16} Status")

    print('-' * 50)

    for device in devices:

        monitor_device(device, previous_status)

    time.sleep(10)





