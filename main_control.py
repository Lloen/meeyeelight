import tkinter as tk
import os
import time
from threading import *
from tkinter.colorchooser import askcolor
from yeelight import Bulb
from yeelight.transitions import *
from yeelight import Flow
from hotspot.hotspot_controller import create_hotspot, create_malicious_yeelight, stop_hotspot
from mitm.yeelight_connect import connect_to_yeelight

class GUI_CONTROL():
    def __init__(self, var):
        self.bulb = Bulb("192.168.12.169")

        self._var = var
        self.root = tk.Tk(className="MeeYeelight")
        self.root.resizable(False, False)
        self.root.geometry('300x300')
        self.media_directory = os.getcwd() + "/media"

        self.brightness_Value = tk.IntVar()

        # thread_create_malicious_ap = Thread(target=create_hotspot, 
        #     args=("wlx908d7820402b", 
        #         self._var.hotspot['ssid'],
        #         self._var.hotspot['password']))
        # thread_create_malicious_ap.name = 'create_malicious_yeelight'
        # thread_create_malicious_ap.setDaemon(True)
        # thread_create_malicious_ap.start()  

        self.BTN_on = tk.Button(self.root, text="On", command=self.on_click)
        self.BTN_off = tk.Button(self.root, text="Off", command=self.off_click)
        self.BTN_red = tk.Button(self.root, text="Pick a color", command=self.change_color)
        self.BTN_strobe = tk.Button(self.root, text="Strobe", command=self.strobe)
        self.SCL_brightness = tk.Scale(self.root, from_=0, to=100, variable=self.brightness_Value, orient=tk.HORIZONTAL)
        self.BTN_brightness = tk.Button(self.root, text="Set Brightness", command=self.change_brightness)

        self.load_gui()

    def load_gui(self):
        self.BTN_on.pack(expand=True)
        self.BTN_off.pack(expand=True)
        self.BTN_red.pack(expand=True)
        self.BTN_strobe.pack(expand=True)
        self.SCL_brightness.pack(expand=True)
        self.BTN_brightness.pack(expand=True)

        self.root.mainloop()
    
    def change_color(self):
        colors = askcolor(title="Yeelight Color")
        self.root.configure(bg=colors[1])
        self.bulb.set_rgb(int(colors[0][0]), int(colors[0][1]), int(colors[0][2]))

    def change_brightness(self):
        self.bulb.set_brightness(self.brightness_Value.get())

    def strobe(self):
        flow = Flow(
            count=10,
            transitions=strobe_color(brightness=100),
        )
        self.bulb.start_flow(flow)
               
    def on_click(self):
        self.bulb.turn_on()

    def off_click(self):
        self.bulb.turn_off()
