from global_variables import GlobalData
from main_mitm import GUI_MITM
from network.arp_scan import get_mac
from scapy.all import *



def main():
    _var = GlobalData()
    _var.malicious_yeelight['ssid'] = "yeelink-light-color1_miap5332"
    _var.malicious_yeelight['gateway'] = "192.168.13.1"
    _var.interfaces['attack'] = "wlp3s0"
    _var.interfaces['malicious_yeelight'] = "wlx908d7820496c"
    _var.interfaces['hotspot'] = "wlx908d7820402b"
    _var.yeelight['mac'] = "78:11:dc:aa:53:32"
    _var.this['mac_gateway'] = get_mac(_var.interfaces['attack'], conf.route.route()[2])
    GUI_MITM(_var)


if __name__ == '__main__':
    main()
