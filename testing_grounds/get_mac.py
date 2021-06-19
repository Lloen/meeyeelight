from scapy.all import *


ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.13.2"), retry=-2, timeout=5, verbose=1, iface="wlp3s0")
mac = ""

for sent, received in ans:
    mac = received.hwsrc

print(mac)
