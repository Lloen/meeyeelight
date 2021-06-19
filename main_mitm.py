import tkinter as tk
import os
import threading
import time

from mitm.yeelight_connect import connect_to_yeelight
from mitm.deauth import run_deauth
from mitm.ping_of_death import run_ping_of_death
from hotspot.hotspot_controller import create_hotspot
from hotspot.yeelight_socket import start_connection_proccess


class GUI_MITM():
    def __init__(self, var):
        self._var = var
        self.root = tk.Tk(className="MeeYeelight - Deauth")
        self.root.resizable(False, False)
        self.media_directory = os.getcwd() + "/media"

        # Frames
        self.FRAME_deauth = tk.Frame(self.root, borderwidth=10)
        # Deauth SUB_FRAME_deauth
        self.LB_deauth_title = tk.Label(self.FRAME_deauth, text="Deauth Yeelight devices", font="bold")
        self.SUB_FRAME_deauth = tk.Frame(self.FRAME_deauth, pady=5)
        self.LB_deauth_yeelight = tk.Label(self.FRAME_deauth, text="Yeelight deauthenticated")
        self.LB_start_ap = tk.Label(self.FRAME_deauth, text="Access Point started")
        self.LB_start_malicious_yeelight = tk.Label(self.FRAME_deauth, text="Malicious Yeelight started")
        self.IMG_attacker = tk.PhotoImage(file=self.media_directory + "/attacker.png")
        self.IMG_attacker_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_attacker)
        self.IMG_lamp = tk.PhotoImage(file=self.media_directory + "/lamp.png")
        self.IMG_lamp_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_lamp)
        self.IMG_hub = tk.PhotoImage(file=self.media_directory + "/hub.png")
        self.IMG_hub_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_hub)

        self.load_gui()

    def load_gui(self):
        self.FRAME_deauth.grid()
        self.LB_deauth_title.grid(row=0)
        self.SUB_FRAME_deauth.grid()
        self.FRAME_deauth.grid()
        self.IMG_attacker_Pack.grid()
        self.IMG_lamp_Pack.grid()
        self.IMG_hub_Pack.grid()

        # Deauth Yeelight
        # thread_lamp_deauth = threading.Thread(target=run_deauth(self._var.yeelight['mac'], self._var.this['mac_gateway']))
        thread_lamp_deauth = threading.Thread(target=run_ping_of_death, 
            args=(self._var.yeelight['ip'], self._var.interfaces['attack'],))
        thread_lamp_deauth.name = 'lamp_deauth'
        thread_lamp_deauth.start()
        self.LB_deauth_yeelight.grid()
        self.root.update()


        # Connect to Yeelight
        thread_yeelight_connection = threading.Thread(target=connect_to_yeelight,
            args=(self._var.hotspot['ssid'], self._var.interfaces['attack'],))
        thread_yeelight_connection.name = 'yeelight_connection'
        thread_yeelight_connection.start()
        thread_yeelight_connection.join()


        # Create Access Point
        thread_create_hotspot = threading.Thread(target=create_hotspot, 
            args=(self._var.interfaces['hotspot'], 
                self._var.hotspot['ssid'], 
                self._var.hotspot['gateway'], 
                self._var.yeelight['mac'], ))
        thread_create_hotspot.name = 'create_hotspot'
        thread_create_hotspot.start()
        thread_create_hotspot.join()
        self.LB_start_ap.grid()
        self.root.update()


        time.sleep(5)

        # Start Yeelight Connection Process
        thread_start_connection_process = threading.Thread(target=start_connection_proccess,
            args=(self._var.interfaces['hotspot'], ))
        thread_start_connection_process.name = "connection_process"
        thread_start_connection_process.start()
        self.LB_start_malicious_yeelight.grid
        self.root.update()

        self.root.mainloop()