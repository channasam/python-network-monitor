# --- Importing library ---
import tkinter as tk
import subprocess as subp
import threading



# --- Creating window ---
window = tk.Tk()
window.title("Network Monitor Tool")
window.geometry("800x600")


# --- Container for both device lists ---
list_frames = tk.Frame(window)
list_frames.pack(pady=10)


# --- Left side: Discovered Devices ---
tk.Label(list_frames, text="Discovered Devices.").grid(row=0, column=0)
devices_list = tk.Listbox(list_frames, width=35, height=15)
devices_list.grid(row=1, column=0, padx=10)


# --- Right side: Monitored Devices ---
tk.Label(list_frames, text="Monitored Devices.").grid(row=0, column=1)
monitored_list = tk.Listbox(list_frames, width=35, height=15)
monitored_list.grid(row=1, column=1, padx=10)


# --- Show status label ---
status_label = tk.Label(

    window,
    text="READY",
    fg="blue"
)

status_label.pack(pady=5)

# --- Devices storages ---
devices = []


# --- Function for scan all lan ip and return the result ---
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
            window.after(0, devices_list.insert, tk.END, ip)
            
    return online_devices


# --- Function for call scan_net function ---
def run_scan():

    devices = scan_net()

    print(devices)


# --- Function for separate run_scan within another thread ---
def start_scan():

    devices_list.delete(0, tk.END)

    thread = threading.Thread(

        target=run_scan
    )

    thread.start()


# --- Function for adding devices to devices storages (devices) ---
def add_device():

    selected = devices_list.curselection()

    if not selected:

        status_label.config(

            text="Please select discovered device.",
            fg="red"
        )

        print("Please select discovered device.")

        return

    ip = devices_list.get(selected[0])

    if ip not in devices:

        devices.append(ip)
        monitored_list.insert(tk.END, ip)

        status_label.config(
        
            text=f"{ip} is Added successfully.",
            fg="blue"
        )

        print(f"{ip} is Added successfully.")
        print(f"Devices list: {devices}")

    else: 

        status_label.config(
                
            text=f"{ip} is Already added",
            fg="red"
        )

        print(f"{ip} is Already added")
        print(f"Devices list: {devices}")


# --- Function for remove device from monitored list ---
def remove_device():

    selected = monitored_list.curselection()

    if not selected:

        status_label.config(
                        
            text="Please select monitored device",
            fg="red"
        )

        print("Please select monitored device")

        return

    ip = monitored_list.get(selected[0])
    monitored_list.delete(selected[0])

    devices.remove(ip)

    status_label.config(
                            
        text=f"{ip} is Removed",
        fg="blue"
    )

    print(f"{ip} is Removed")
    print(f"Devices list: {devices}")


# --- Create scan_button on window ---
scan_button = tk.Button(

    window,
    text="START SCAN",
    command=start_scan,

)

scan_button.pack()


# --- Create add_button on window ---
add_button = tk.Button(

    window,
    text="ADD DEVICE",
    command=add_device
)

add_button.pack()


# --- Create remove button on windows ---
remove_button = tk.Button(
    window,
    text="REMOVE DEVICE",
    command=remove_device
)

remove_button.pack()



# --- Main loop ---
window.mainloop()