import os

def connect_to_yeelight(ssid, iface):
    try:
        os.system(f"nmcli d wifi connect {ssid} ifname {iface}")
    except:
        raise
    else:
        return True