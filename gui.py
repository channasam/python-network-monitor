import tkinter as tk
import subprocess as subp
import threading


window = tk.Tk()

window.title("Network Monitor Tool")
window.geometry("800x600")

def scan_net():

    online_devices = []

    for number in range(1, 255):

        ip = f"192.168.10.{number}"

        result = subp.run(

            ["ping", "-n", "1", "-w", "100", ip],
            capture_output=True

        )

        if result.returncode == 0:

            online_devices.append(ip)
            print(f"🟢 {ip} is Online")
            
    return online_devices


def start_scan():

    thread = threading.Thread(

        target=scan_net
    )

    thread.start()



scan_button = tk.Button(

    window,
    text="START SCAN",
    command=start_scan,

)


scan_button.pack()



window.mainloop()