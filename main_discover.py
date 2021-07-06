import os
import tkinter as tk
import threading
import queue

import global_variables as _var

from mitm.network_scanner import NetworkScanner
from mitm.client_scanner import ClientScanner


class GUI_DISCOVER():
    def __init__(self, var):
        self._var = var
        self.queue = queue.Queue()
        self.root = tk.Tk(className="MeeYeelight - Discovery")
        self.root.resizable(False, False)

        self.media_directory = os.getcwd() + "/media"
        self.ssid_name = tk.StringVar()
        self.ssid_mac = tk.StringVar()
        self.ssid_channel = tk.StringVar()
        self.yeelight_mac = tk.StringVar()

        # Discover GUI variables
        self.FRAME_discover = tk.Frame(self.root, borderwidth=10)
        self.BTN_next = tk.Button(self.FRAME_discover, text="Next", command=self.next_click, bg='#C5DDB6', width=25)
        self.LB_discover_yeelight_hosts = tk.Label(self.FRAME_discover, text="Discovering Network devices", font="bold")
        # Discover SUB_FRAME_discovery
        self.SUB_FRAME_discovery = tk.Frame(self.FRAME_discover)
        self.LB_yeelight_MAC = tk.Label(self.SUB_FRAME_discovery, text="Yeelight MAC:")
        self.EN_yeelight_MAC = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.yeelight_mac, justify='center')
        self.LB_ssid_name = tk.Label(self.SUB_FRAME_discovery, text="SSID:")
        self.EN_ssid_name = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.ssid_name, justify='center')
        self.BTN_scan = tk.Button(self.SUB_FRAME_discovery, text="Scan", command=self.scan_click)
        self.LB_ssid_MAC = tk.Label(self.SUB_FRAME_discovery, text="BSSID:")
        self.EN_ssid_MAC = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.ssid_mac, justify='center')
        self.LB_ssid_channel = tk.Label(self.SUB_FRAME_discovery, text="Channel:")
        self.EN_ssid_channel = tk.Entry(self.SUB_FRAME_discovery, textvariable=self.ssid_channel, justify='center')
        self.LB_loading_discover = tk.Label(self.FRAME_discover)

        self.load_gui()

    def load_gui(self):
        self.FRAME_discover.grid()
        self.BTN_next.grid(row=0, column=0)
        self.LB_discover_yeelight_hosts.grid(row=1, column=0)
        self.SUB_FRAME_discovery.grid()
        self.LB_ssid_name.grid(row=1, column=0)
        self.EN_ssid_name.grid(row=2, column=0)
        self.BTN_scan.grid(row=3, column=0)
        self.LB_ssid_MAC.grid(row=4, column=0)
        self.EN_ssid_MAC.grid(row=5, column=0)
        self.LB_ssid_channel.grid(row=6, column=0)
        self.EN_ssid_channel.grid(row=7, column=0)
        self.LB_yeelight_MAC.grid(row=8, column=0)
        self.EN_yeelight_MAC.grid(row=9, column=0)

        self.root.mainloop()

    def scan_click(self):
        self.BTN_scan.config(text="⌛")
        self.root.update()
        network_scanner = NetworkScanner(self._var.interfaces['hotspot'], self.ssid_name.get())
        bssid, channel = network_scanner.start_scan()
      
        self.EN_ssid_MAC.delete(0, tk.END)
        self.EN_ssid_MAC.insert(0, str(bssid))
        self.EN_ssid_channel.delete(0, tk.END)
        self.EN_ssid_channel.insert(0, str(channel))
        self.root.update()
        
        if bssid is not None:
            client_scanner = ClientScanner(self._var.interfaces['hotspot'], bssid, channel)
            yeelight_mac = client_scanner.start_scan()

            self.EN_yeelight_MAC.delete(0, tk.END)
            self.EN_yeelight_MAC.insert(0, str(yeelight_mac))

        self.BTN_scan.config(text="Re-Scan")
        self.root.update()

        
    def next_click(self):
        # Change Global Variables
        self._var.ssid['mac'] = self.ssid_mac.get()
        self._var.ssid['channel'] = self.ssid_channel.get()
        self._var.yeelight['mac'] = self.yeelight_mac.get()

        self.root.destroy()
