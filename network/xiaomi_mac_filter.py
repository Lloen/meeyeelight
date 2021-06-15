from scapy.all import *
import global_variables as _var


def filter(network_devices):

    filtered_devices = []

    for device in network_devices:
        device_vendor_MAC = device['mac'][0:8]
        if device_vendor_MAC == "78:11:DC" or device_vendor_MAC == "78:11:dc":
            filtered_devices.append(device)
    return filtered_devices


def order(filtered_devices):
    src_port = RandShort()
    dst_port = 54321
    yeelight = {
        'ip': "No Yeelight found.",
        'mac': ""
    }

    for device in filtered_devices:
        dst_ip = device['ip']
        pkt = sr1(IP(dst=dst_ip)/UDP(sport=src_port, dport=dst_port), timeout=2, verbose=0)
        if pkt is None:
            yeelight['ip'] = device['ip']
            yeelight['mac'] = device['mac']
    return yeelight
