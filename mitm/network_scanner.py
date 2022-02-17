from scapy.all import *
from threading import Thread
import time

class NetworkScanner():
    def __init__(self, iface, ssid):
        self.stop_sniffing = False
        self.iface = iface
        self.iface_monitor = iface + "mon"
        self.ssid = ssid

        self.bssid = None
        self.channel = None

    def start_scan(self):
        self.set_iface_monitor()
        while self.bssid is None:
            self.start_sniff()
        self.stop_scan()
        self.set_iface_managed()
        return self.bssid, self.channel

    def stop_scan(self):
        self.stop_sniffing = True

    def get_stop_sniffing(self):
        if self.stop_sniffing:
            return True
        else:
            return False

    def channel_hopper(self):
        while not self.stop_sniffing:
            try:
                channel = random.randrange(1,14)
                cmd = f"sudo iwconfig {self.iface_monitor} channel {channel}"
                os.system(cmd)
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop_scan()
                break

        return True
  
    def start_sniff(self):
        thread_channel_hopper = Thread(target=self.channel_hopper)
        thread_channel_hopper.setDaemon(True)
        thread_channel_hopper.start()
        try:
            sniff(iface=self.iface_monitor,
                lfilter=lambda x:(x.haslayer(Dot11Beacon) or x.haslayer(Dot11ProbeResp)),
                stop_filter=self.get_stop_sniffing(),
                prn=lambda x: self.add_network(x))
        except Exception as e:
            pass
    
    def add_network(self, pkt):
        ssid = pkt[Dot11Beacon].network_stats()['ssid']
        if ssid == self.ssid:
            self.stop_scan()
            self.bssid = pkt[Dot11].addr3
            self.channel = int(ord(pkt[Dot11Elt:3].info))
            raise KeyboardInterrupt

    def set_iface_monitor(self):
        cmd_1 = f"sudo airmon-ng start {self.iface}"
        os.system(cmd_1)

    def set_iface_managed(self):
        cmd_1 = f"sudo airmon-ng stop {self.iface_monitor}"
        os.system(cmd_1)

