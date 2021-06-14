import tkinter as tk
import os
import threading


from deauth.deauth import run_deauth


class GUI_DEAUTH():
    def __init__(self, var):
        self._var = var
        self.root = tk.Tk(className="MeeYeelight - Deauth")
        self.root.resizable(False, False)
        self.media_directory = os.getcwd() + "/media"

        # Frames
        self.FRAME_deauth = tk.Frame(self.root, borderwidth=10)
        # Deauth SUB_FRAME_deauth
        self.LB_arp_yeelight_hosts = tk.Label(self.FRAME_deauth, text="Deauth Yeelight devices", font="bold")
        self.SUB_FRAME_deauth = tk.Frame(self.FRAME_deauth, pady=5)
        self.IMG_attacker = tk.PhotoImage(file=self.media_directory + "/attacker.png")
        self.IMG_attacker_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_attacker)
        self.IMG_lamp = tk.PhotoImage(file=self.media_directory + "/lamp.png")
        self.IMG_lamp_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_lamp)
        self.IMG_hub = tk.PhotoImage(file=self.media_directory + "/hub.png")
        self.IMG_hub_Pack = tk.Label(self.SUB_FRAME_deauth, image=self.IMG_hub)

        self.load_gui()

    def load_gui(self):
        self.FRAME_deauth.grid()
        self.LB_arp_yeelight_hosts.grid(row=0)
        self.IMG_attacker_Pack.grid()
        self.IMG_lamp_Pack.grid()
        self.IMG_hub_Pack.grid()

        thread_lamp_deauth = threading.Thread(target=run_deauth(self._var.yeelight['mac'], self._var.this['mac_gateway']))
        thread_lamp_deauth.start()
        self.root.mainloop()
