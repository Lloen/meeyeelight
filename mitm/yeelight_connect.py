import os
import sys
import time

def connect_to_yeelight(ssid, iface):
    iface_channel = f"sudo iwconfig {iface} channel 6"
    os.system(iface_channel)
    connect_yeelight_cmd = f"sudo nmcli d wifi connect {ssid} ifname {iface}"
    connected = False

    while not connected:
        try:
            if os.system(connect_yeelight_cmd) != 0:
                time.sleep(0.5)
            else:
                connected = True
        except KeyboardInterrupt:
            break    
    return True