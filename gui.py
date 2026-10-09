import tkinter as tk
import subprocess as subp
import threading


window = tk.Tk()

window.title("Network Monitor Tool")
window.geometry("800x600")

devices_list = tk.Listbox(window, width=40, height=10)

devices_list.pack()

devices = []


def scan_net():

    online_devices = []

    for number in range(34, 56):

        ip = f"192.168.10.{number}"

        result = subp.run(

            ["ping", "-n", "1", "-w", "100", ip],
            capture_output=True

        )

        if result.returncode == 0:

            online_devices.append(ip)
            print(f"🟢 {ip} is Online")
            devices_list.insert(tk.END, ip)
            
    return online_devices


def run_scan():

    devices = scan_net()

    print(devices)


def start_scan():

    devices_list.delete(0, tk.END)

    thread = threading.Thread(

        target=run_scan
    )

    thread.start()


def add_device():

    selected = devices_list.curselection()
    ip = devices_list.get(selected[0])

    if ip not in devices:

        devices.append(ip)
        print(f"{ip} is Added")
        print(f"Devices: {devices}")

    else: 

        print(f"{ip} is Already added")
        print(f"Devices: {devices}")


scan_button = tk.Button(

    window,
    text="START SCAN",
    command=start_scan,

)


add_button = tk.Button(

    window,
    text="ADD DEVICE",
    command=add_device
)

scan_button.pack()
add_button.pack()


window.mainloop()