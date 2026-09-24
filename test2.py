import telebot
import subprocess
import time
import os
from config import BOT_TOKEN, CHAT_ID, INTERVAL, PING_TIMEOUT
from datetime import datetime


bot = telebot.TeleBot(BOT_TOKEN)


def check_ping(ip_address):

    try:

        subprocess.check_output(

            ["ping", "-n", "1", "-w", str(PING_TIMEOUT), ip_address], stderr=subprocess.STDOUT

        )

        return True
    
    except subprocess.CalledProcessError:

        return False


def send_alert(message):

    bot.send_message(CHAT_ID, message)


devices = [

    {"name": "AC Pro F-Floor", "ip": "192.168.10.254", "type": "Access point"},
    {"name": "AC Lr Stair", "ip": "192.168.10.55", "type": "Access Point"},
    {"name": "AC Pro GR-Floor", "ip": "192.168.10.35", "type": "Access Point"},

]

previous_status = {}

for device in devices:

    previous_status[device["ip"]] = None


def monitor_device(device, previous_status):

    current_status = check_ping(device["ip"])

    if previous_status[device["ip"]] is None:

        previous_status[device["ip"]] = current_status

    elif previous_status[device["ip"]] != current_status:

        if current_status:

            message = (

                f"🟢 NETWORK RESTORED\n\n" 
                f"Device: {device['name']}\n"
                f"Type: {device['type']}\n" 
                f"IP: {device['ip']}\n" 
                f"Status: ONLINE"

            )

        else:

            message = (

                f"🚨 NETWORK ALERT\n\n" 
                f"Device: {device['name']}\n"
                f"Type: {device['type']}\n"
                f"IP: {device['ip']}\n" 
                f"Status: OFFLINE"

            )

        send_alert(message)

    print_device_status(device, current_status)

    previous_status[device["ip"]] = current_status

    return current_status


def print_device_status(device, current_status):

    if current_status:
    
        print(f"{device["name"]:<20} {device["type"]:<15} {device["ip"]:<16} ONLINE")
    
    else:
    
        print(f"{device["name"]:<20} {device["type"]:<15} {device["ip"]:<16} OFFLINE")


while True:

    os.system("cls")

    current_time = datetime.now().strftime("%H:%M:%S")

    print(f"\n[{current_time}] Checking device...\n")

    print(f"{'Devices':<20} {'Type':<15} {'IP Address':<16} Status")

    print('-' * 60)

    online_count = 0
    offline_count = 0

    for device in devices:

        status = monitor_device(device, previous_status)

        if status:

           online_count += 1

        else:

           offline_count += 1

    print(f"\n{'-' * 60}")
    print("SUMMARY")
    print('-' * 60)
    print(f"Total Devices : {len(devices)}")
    print(f"Online        : {online_count}")
    print(f"Offline       : {offline_count}")
    print('-' * 60)

    time.sleep(INTERVAL)