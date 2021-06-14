import tkinter as tk
import os

from scapy.all import get_if_list, get_if_hwaddr, get_if_addr, conf


class GUI_MAIN_ARP():
    def __init__(self, var):
            self._var = var
            self.root = tk.Tk(className="MeeYeelight - Start")
            self.root.resizable(False, False)

            self.media_directory = os.getcwd() + "/media"
            self.auto_discovery = tk.BooleanVar(value=True)
            self.hotspot_interface = tk.StringVar(value="Select")
            self.attack_interface = tk.StringVar(value="Select")
            self.network_interfaces = get_if_list()

            # Start GUI variables
            self.FRAME_start = tk.Frame(self.root, borderwidth=10)
            self.BTN_start = tk.Button(self.FRAME_start, text="Start", command=self.start_click, bg='#C5DDB6', width=25)
            self.LB_autodiscover = tk.Label(self.FRAME_start, text="Autodiscovery")
            self.CB_autodiscover = tk.Checkbutton(self.FRAME_start, variable=self.auto_discovery, onvalue=True, offvalue=False)
            self.LB_hotspot_interface = tk.Label(self.FRAME_start, text="Hotspot Interface")
            self.OM_hotspot_interface = tk.OptionMenu(self.FRAME_start, self.hotspot_interface, *self.network_interfaces)
            self.LB_attack_interface = tk.Label(self.FRAME_start, text="Attack Interface")
            self.OM_attack_interface = tk.OptionMenu(self.FRAME_start, self.attack_interface, *self.network_interfaces)

            self.load_gui()

    def load_gui(self):
        # Start
        self.FRAME_start.grid()
        self.BTN_start.grid(row=0, column=1)
        self.LB_autodiscover.grid(row=1, column=0)
        self.LB_hotspot_interface.grid(row=1, column=1)
        self.LB_attack_interface.grid(row=1, column=2)
        self.CB_autodiscover.grid(row=2, column=0)
        self.OM_hotspot_interface.grid(row=2, column=1)
        self.OM_attack_interface.grid(row=2, column=2)
        self.root.mainloop()

    def start_click(self):
        # Global variable changes
        self._var.options['autodiscovery'] = self.auto_discovery.get()
        self._var.interfaces['attack'] = self.attack_interface.get()
        self._var.interfaces['hotspot'] = self.hotspot_interface.get()
        self._var.interfaces['attack_mon'] = self.attack_interface.get() + "mon"
        self._var.this['mac'] = get_if_hwaddr(self._var.interfaces['attack'])
        self._var.this['ip'] = get_if_addr(self._var.interfaces['attack'])
        self._var.this['ip_gateway'] = conf.route.route()[2]

        self.root.destroy()

    def arp_gui(self):
        self.root.focus()
        self.FRAME_arp.grid()
        self.SUB_FRAME_show_arp.grid()
