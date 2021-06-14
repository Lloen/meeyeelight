from global_variables import GlobalData
from main_arp import GUI_MAIN_ARP
from main_discover import GUI_DISCOVER
from main_deauth import GUI_DEAUTH


def main():
    _var = GlobalData()
    GUI_MAIN_ARP(_var)
    GUI_DISCOVER(_var)
    GUI_DEAUTH(_var)


if __name__ == '__main__':
    main()
