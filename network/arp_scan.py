from scapy.all import *


# Code from https://gist.github.com/ritiek
def getDefaultInterface(returnNet=True):
    def to_CIDR_notation(bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = 32 - int(round(math.log(0xFFFFFFFF - bytes_netmask, 2)))
        net = "%s/%s" % (network, netmask)
        if netmask < 16:
            return None
        else:
            return net
    for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue
        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue
        net = to_CIDR_notation(network, netmask)
        if interface != scapy.config.conf.iface:
            continue
        if net:
            if returnNet:
                return net
            else:
                return interface


def get_network_devices():
    network_ip = getDefaultInterface()
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_ip), retry=-2, timeout=5, verbose=0)

    devices = []

    for sent, received in ans:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices


def get_mac(iface, ip):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), retry=-1, timeout=5, verbose=0, iface=iface)
    mac = ""

    for sent, received in ans:
        mac = received.hwsrc

    return mac
