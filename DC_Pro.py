import threading
import tkinter as tk

class DeviceManager:
    def __init__(self):
        self.devices = {'printer': None, 'scanner': None}
        self.users = {}
        self.pending_requests = {}
        self.lock = threading.Lock()

    def allocate_device(self, user, device_name):
        with self.lock:
            if device_name in self.devices and self.devices[device_name] is None:
                self.devices[device_name] = user
                self.users[user] = device_name
                return f"Device {device_name} allocated to {user}"
            else:
                return f"Device {device_name} is not available. {user} added to the queue."

    def release_device(self, user):
        with self.lock:
            if user in self.users:
                device_name = self.users[user]
                self.devices[device_name] = None
                del self.users[user]
                if self.pending_requests.get(device_name):
                    if self.pending_requests[device_name]:
                        next_user = self.pending_requests[device_name].pop(0)
                        self.devices[device_name] = next_user
                        self.users[next_user] = device_name
                        return f"Device {device_name} allocated to {next_user} from the queue."
                return f"Device {device_name} is released."
            else:
                return f"No device allocated to {user}."

    def check_device_status(self):
        return '\n'.join([f"{device}: {user if user else 'Available'}" for device, user in self.devices.items()])

    def start_release_timer(self, device_name):
        def release():
            result = self.release_device(self.devices[device_name])
            device_status.config(text=result)
            update_status()
        
        root.after(15000, release)  # Release after 15 seconds

manager = DeviceManager()

def request_device():
    user = entry_user.get()
    device_name = entry_device.get()
    result = manager.allocate_device(user, device_name)
    device_status.config(text=result)
    if 'added to the queue' not in result:
        manager.start_release_timer(device_name)

def release_device():
    user = entry_user.get()
    result = manager.release_device(user)
    device_status.config(text=result)

def update_status():
    status = manager.check_device_status()
    label_status.config(text=status)
    root.after(1000, update_status)

root = tk.Tk()
root.title("Device Management System")

label_user = tk.Label(root, text="Enter User:")
label_user.pack()

entry_user = tk.Entry(root)
entry_user.pack()

label_device = tk.Label(root, text="Enter Device:")
label_device.pack()

entry_device = tk.Entry(root)
entry_device.pack()

btn_request = tk.Button(root, text="Request Device", command=request_device)
btn_request.pack()

btn_release = tk.Button(root, text="Release Device", command=release_device)
btn_release.pack()

device_status = tk.Label(root, text="")
device_status.pack()

label_status = tk.Label(root, text="")
label_status.pack()

root.after(1000, update_status)
root.mainloop()
