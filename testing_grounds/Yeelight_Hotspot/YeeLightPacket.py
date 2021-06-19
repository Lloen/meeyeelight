import binascii
from scapy.all import *

data = binascii.unhexlify('21310020ffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
print(data)
packet = Ether(dst='78:11:dc:aa:53:32', src= get_if_hwaddr("wlp3s0"), type=2048)/IP(version=4, ihl=5, tos=0, len=60, id=54230, flags=2, frag=0, ttl=64, proto=17, src='192.168.13.3', dst='192.168.13.1')/UDP(sport=40934, dport=54321, len=40)/Raw(load=data)
# class UDP(Packet):
#     name = "UDP"
#     fields_desc = [ ShortEnumField("sport", 53, UDP_SERVICES),
#                     ShortEnumField("dport", 53, UDP_SERVICES),
#                     ShortField("len", None),
#                     XShortField("chksum", None), ]

sendp(packet, iface="wlp3s0")