from global_variables import GlobalData
from main_iface import GUI_MAIN_IFACE
from main_discover import GUI_DISCOVER
from main_mitm import GUI_MITM
from main_control import GUI_CONTROL


def main():
    _var = GlobalData()
    GUI_MAIN_IFACE(_var)
    GUI_DISCOVER(_var)
    GUI_MITM(_var)
    GUI_CONTROL(_var)


if __name__ == '__main__':
    main()
