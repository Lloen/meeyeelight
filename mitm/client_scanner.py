from scapy.all import *
from threading import Thread
import time

class ClientScanner():
    def __init__(self, iface, bssid, channel):
        self.stop_sniffing = False
        self.iface = iface
        self.iface_monitor = self.iface + "mon"
        self.bssid = bssid
        self.channel = channel

        self.client_mac = None

    def start_scan(self):
        self.set_iface_monitor()
        self.start_sniff()
        
        self.set_iface_managed()
        return self.client_mac
  
    def start_sniff(self):
        try:
            sniff(iface=self.iface_monitor,
                stop_filter=self.stop_sniffing,
                prn=lambda x: self.add_client(x))
        except:
            pass
    
    def add_client(self, pkt):
        if pkt.haslayer(Dot11) or pkt.haslayer(Dot11FCS):
            bssid = pkt[Dot11].addr3
            if bssid == self.bssid:
                device_vendor_MAC = pkt[Dot11].addr1[0:8]
                if device_vendor_MAC == "78:11:DC" or device_vendor_MAC == "78:11:dc":
                    self.stop_sniffing = True
                    self.client_mac = pkt[Dot11].addr1
                    raise KeyboardInterrupt


    def set_iface_monitor(self):
        cmd_1 = f"sudo airmon-ng start {self.iface} {self.channel}"
        os.system(cmd_1)

    def set_iface_managed(self):
        cmd_1 = f"sudo airmon-ng stop {self.iface_monitor}"
        os.system(cmd_1)

