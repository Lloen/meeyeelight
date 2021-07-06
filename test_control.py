from global_variables import GlobalData
from main_control import GUI_CONTROL

if __name__ == '__main__':
    _var = GlobalData()
    _var.malicious_yeelight['ssid'] = "yeelink-light-color1_miap5332"
    _var.malicious_yeelight['gateway'] = "192.168.13.1"
    _var.interfaces['attack'] = "wlx908d7820402b"
    _var.interfaces['malicious_yeelight'] = "wlx908d7820496c"
    _var.interfaces['hotspot'] = "wlp3s0"
    _var.yeelight['mac'] = "78:11:dc:aa:53:32"
    _var.ssid['mac'] = "0C:80:63:59:D1:CE"
    _var.ssid['channel'] = "2"
    _var.hotspot['ssid'] = "Malicious_WLAN"
    _var.hotspot['password'] = "maliciouswlan123"
    GUI_CONTROL(_var)
