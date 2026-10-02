import tkinter as tk
import subprocess


window = tk.Tk()


def scan_network():

    ips = [
        "192.168.10.1",
        "192.168.10.24",
        "192.168.10.35",
        "192.168.10.55",
        "192.168.10.254"
    ]      


    for ip in ips:

        result = subprocess.run(


            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True

        )

        if result.returncode == 0:

            print(f"🟢 {ip} is Online")

        else:

            print(f"🔴 {ip} is Offline")



window.title("Network Monitor Tool")
window.geometry("800x600")


scan_button = tk.Button(

    window,
    text="START SCAN",
    command=scan_network

)


scan_button.pack()


window.mainloop()