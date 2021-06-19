import os

def create_hotspot(iface, ssid, gateway_ip, new_mac):
    iface_down_cmd = f"sudo ifconfig {iface} down"
    iface_change_mac_cmd = f"sudo ifconfig {iface} hw ether {new_mac}"
    iface_up_cmd = f"sudo ifconfig {iface} up"
    create_hotspot_cmd = f"create_ap -g {gateway_ip} -n {iface} {ssid} --no-virt"
    os.system(iface_down_cmd)
    os.system(iface_change_mac_cmd)
    os.system(iface_up_cmd)
    os.system(create_hotspot_cmd)

def stop_hotspot(iface):
    stop_hotspot_cmd = "sudo nmcli dev wifi hotspot ifname " + iface + " ssid " + ssid +" password '" + password +"'"
    os.system(stop_hotspot_cmd)