import telebot
import subprocess
import time
import os
from config import BOT_TOKEN, CHAT_ID, INTERVAL, PING_TIMEOUT
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import threading


bot = telebot.TeleBot(BOT_TOKEN)


devices = [

    {"name": "AC Pro F-Floor", "ip": "192.168.10.254", "type": "Access point"},
    {"name": "AC Lr Stair", "ip": "192.168.10.55", "type": "Access Point"},
    {"name": "AC Pro GR-Floor", "ip": "192.168.10.35", "type": "Access Point"},

]


# Log monitoring

handler = RotatingFileHandler(

    filename="network_monitor.log",
    maxBytes= 1024 * 1024,
    backupCount= 3,
    encoding="utf-8",
)


logging.basicConfig(

    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"

)


logging.info("Network Monitor Started...")


# Function for ping command

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


# Bot reply message to telegram

@bot.message_handler(commands=["status"])
def get_status(message):

    status_message = "📊 Network Devices Status\n\n"

    for device in devices:

        if check_ping(device["ip"]):

            status = "🟢 Online"

        else:

            status = "🔴 Offline"

        status_message += f"{status} : {device["name"]}\n"

    bot.reply_to(message, status_message)


# Create previous status memory.

previous_status = {}

for device in devices:

    previous_status[device["ip"]] = None


# Function for monitoring and prepare message for bot.

def monitor_device(device, previous_status):

    current_status = check_ping(device["ip"])

    if previous_status[device["ip"]] is None:

        previous_status[device["ip"]] = current_status

    elif previous_status[device["ip"]] != current_status:

        if current_status:

            logging.info(f"{device['name']} is Online")

            message = (

                f"🟢 NETWORK RESTORED\n\n" 
                f"Device: {device['name']}\n"
                f"Type: {device['type']}\n" 
                f"IP: {device['ip']}\n" 
                f"Status: ONLINE"

            )

        else:

            logging.warning(f"{device['name']} is Offline")

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


# Function for print devices status to terminal.

def print_device_status(device, current_status):

    if current_status:
    
        print(f"{device['name']:<20} {device['type']:<15} {device['ip']:<16} ONLINE")
    
    else:
    
        print(f"{device['name']:<20} {device['type']:<15} {device['ip']:<16} OFFLINE")


# Notification message to telegram when scrip started 

startup_line = []

for device in devices:

    status = check_ping(device["ip"])
    previous_status[device["ip"]] = status

    if status:

        status_text = "🟢 Online"
        logging.info(f"{device['name']} is Online")

    else:

        status_text = "🔴 Offline"
        logging.warning(f"{device['name']} is Offline")

    startup_line.append(

        f"{status_text} : {device['name']}"
    )

    message = (

        "Network Minitor Started...\n\n" + "\n".join(startup_line) 
    )


# Send message to bot.

send_alert(message)


# Create thread for bot listener.

thread_bot = threading.Thread(

    target=bot.infinity_polling,
    daemon=True,

)

thread_bot.start()

# Startup process of the main program and.

try:

    while True:

        os.system("cls")

        current_time = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{current_time}] Checking device...\n")

        print(f"{'Devices':<20} {'Type':<15} {'IP Address':<16} Status")

        print('-' * 60)

        online_count = 0
        offline_count = 0
        error_count = 0

        for device in devices:

            try:

                status = monitor_device(device, previous_status)

            except Exception:

                logging.exception(

                    f"Error Monitor: {device['name']}"
                )

                error_count += 1

                continue

            if status:

                online_count += 1

            else:

                offline_count += 1

        logging.info(

            "Monitor Sammry: %s Online, %s Offline, %s Error",
            online_count,
            offline_count,
            error_count,
        )

        print(f"\n{'-' * 60}")
        print("SUMMARY")
        print(f"{'-' * 60}")
        print(f"Total Devices : {len(devices)}")
        print(f"Online        : {online_count}")
        print(f"Offline       : {offline_count}")
        print(f"Error         : {error_count}")
        print('-' * 60)

        time.sleep(INTERVAL)

except KeyboardInterrupt:

    logging.info("Netwrok Monitor Stopped")