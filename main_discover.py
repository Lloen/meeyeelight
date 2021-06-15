import os
import tkinter as tk
import threading
import queue

import global_variables as _var
from network.arp_scan import get_network_devices, get_mac
from network.xiaomi_mac_filter import filter, order


class GUI_DISCOVER():
    def __init__(self, var):
        self._var = var
        self.queue = queue.Queue()
        self.root = tk.Tk(className="MeeYeelight - Discovery")
        self.root.resizable(False, False)

        self.media_directory = os.getcwd() + "/media"
        self.phone_ip = tk.StringVar()
        self.phone_mac = tk.StringVar()
        self.yeelight_ip = tk.StringVar()
        self.yeelight_mac = tk.StringVar()

        # Discover GUI variables
        self.FRAME_discover = tk.Frame(self.root, borderwidth=10)
        self.BTN_next = tk.Button(self.FRAME_discover, text="Next", command=self.next_click, bg='#C5DDB6', width=25)
        self.LB_discover_yeelight_hosts = tk.Label(self.FRAME_discover, text="Discovering Network devices", font="bold")
        # Discover SUB_FRAME_discovery
        self.SUB_FRAME_discovery = tk.Frame(self.FRAME_discover)
        self.LB_yeelight_IP = tk.Label(self.SUB_FRAME_discovery, text="Yeelight IP:")
        self.EN_yeelight_IP = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.yeelight_ip)
        self.LB_yeelight_MAC = tk.Label(self.SUB_FRAME_discovery, text="Yeelight MAC:")
        self.EN_yeelight_MAC = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.yeelight_mac)
        self.BTN_yeelight_MAC = tk.Button(self.SUB_FRAME_discovery, text="Get MAC", command=lambda: self.set_MAC_yeelight())
        self.LB_phone_IP = tk.Label(self.SUB_FRAME_discovery, text="Phone IP:")
        self.EN_phone_IP = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.phone_ip)
        self.LB_phone_MAC = tk.Label(self.SUB_FRAME_discovery, text="Phone MAC:")
        self.EN_phone_MAC = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.phone_mac)
        self.BTN_phone_MAC = tk.Button(self.SUB_FRAME_discovery, text="Get MAC", command=lambda: self.set_MAC_phone())
        self.frames = [tk.PhotoImage(file=self.media_directory + "/loading_network.gif", format="gif -index %i" %(i)) for i in range(13)]
        self.LB_loading_discover = tk.Label(self.FRAME_discover)

        self.load_gui()

    def load_gui(self):
        self.FRAME_discover.grid()
        self.LB_discover_yeelight_hosts.grid(row=1, column=0)
        self.LB_yeelight_IP.grid(row=1, column=0)
        self.EN_yeelight_IP.grid(row=2, column=0)
        self.LB_yeelight_MAC.grid(row=3, column=0)
        self.EN_yeelight_MAC.grid(row=4, column=0)
        self.BTN_yeelight_MAC.grid(row=5, column=0)
        self.LB_phone_IP.grid(row=1, column=1)
        self.EN_phone_IP.grid(row=2, column=1)
        self.LB_phone_MAC.grid(row=3, column=1)
        self.EN_phone_MAC.grid(row=4, column=1)
        self.BTN_phone_MAC.grid(row=5, column=1)

        self.EN_yeelight_IP.config(highlightbackground="#ff0000")
        self.EN_yeelight_MAC.config(highlightbackground="#ff0000")
        self.EN_phone_IP.config(highlightbackground="#ff0000")
        self.EN_phone_MAC.config(highlightbackground="#ff0000")

        if self._var.options['autodiscovery']:
            self.LB_loading_discover.grid()
            self.FRAME_discover.after(0, self.update, 0)

            thread_network_scan = threading.Thread(target=self.discover_devices)
            thread_network_scan.start()
            while not self._var.network_hosts:
                self.root.update()

            thread_yeelight_discover = threading.Thread(target=self.discover_xiaomi)
            thread_yeelight_discover.start()
            self.LB_discover_yeelight_hosts.config(text="Discovering Yeelight devices")
            while not self._var.yeelight:
                self.root.update()

            self.LB_loading_discover.grid_forget()
            if self._var.yeelight is not None:
                self.EN_yeelight_IP.insert(0, self._var.yeelight['ip'])
                self.EN_yeelight_IP.config(highlightbackground="#006600")
                self.EN_yeelight_MAC.insert(0, self._var.yeelight['mac'])
                self.EN_yeelight_MAC.config(highlightbackground="#006600")

        self.BTN_next.grid(row=0, column=0)
        self.SUB_FRAME_discovery.grid()
        self.root.mainloop()

    def next_click(self):
        # Change Global Variables
        self._var.yeelight['ip'] = self.yeelight_ip.get()
        self._var.yeelight['mac'] = self.yeelight_mac.get()
        self._var.phone['ip'] = self.phone_ip.get()
        self._var.phone['mac'] = self.phone_mac.get()
        # Get Gateway's MAC
        if self._var.options['autodiscovery']:
            for device in self._var.network_hosts:
                if device['ip'] == self._var.this['ip_gateway']:
                    self._var.this['mac_gateway'] = device['mac']
        else:
            self._var.this['mac_gateway'] = get_mac(self._var.interfaces['attack'], self._var.this['ip_gateway'])

        self.root.destroy()

    def discover_devices(self):
        network_devices = get_network_devices()
        self._var.network_hosts = network_devices

    def discover_xiaomi(self):
        xiaomi_devices = filter(self._var.network_hosts)
        yeelight_device = order(xiaomi_devices)
        self._var.yeelight['ip'] = yeelight_device['ip']
        self._var.yeelight['mac'] = yeelight_device['mac']

    def set_MAC_phone(self):
        phone_ip = self.phone_ip.get()
        if self._var.options['autodiscovery']:
            for device in self._var.network_hosts:
                if device['ip'] == phone_ip:
                    mac = device['mac']
        else:
            mac = get_mac(self._var.interfaces['attack'], phone_ip)

        if not mac == "":
            self.EN_phone_MAC.delete(0, tk.END)
            self.EN_phone_MAC.insert(0, str(mac))
            self.EN_phone_IP.config(highlightbackground="#006600")
            self.EN_phone_MAC.config(highlightbackground="#006600")

    def set_MAC_yeelight(self):
        yeelight_ip = self.phone_ip.get()
        if self._var.options['autodiscovery']:
            for device in self._var.network_hosts:
                if device['ip'] == yeelight_ip:
                    mac = device['mac']
        else:
            mac = get_mac(self._var.interfaces['attack'], yeelight_ip)

        if not mac == "":
            self.EN_yeelight_ip_MAC.delete(0, tk.END)
            self.EN_yeelight_ip_MAC.insert(0, str(mac))
            self.EN_yeelight_ip_IP.config(highlightbackground="#006600")
            self.EN_yeelight_ip_MAC.config(highlightbackground="#006600")

    # Function to play GIF
    def update(self, ind):
        frame = self.frames[ind]
        ind += 1
        if ind == 13:
            ind = 0
        self.LB_loading_discover.configure(image=frame)
        self.root.after(65, self.update, ind)
