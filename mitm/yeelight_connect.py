import os

def connect_to_yeelight(ssid, iface):
    iface_channel = f"sudo iwconfig {iface} channel 6"
    os.system(iface_channel)
    connect_yeelight_cmd = f"nmcli d wifi connect {ssid} ifname {iface}"
    try:
        if os.system(connect_yeelight_cmd) != 0:
            raise Exception()
    except:
        connect_to_yeelight(ssid, iface)
    else:
        return True