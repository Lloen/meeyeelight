from dataclasses import dataclass, field


@dataclass
class GlobalData:

    # Options chosen at the start
    options: dict = field(default_factory=dict) 

    # List of hosts in the network with their IP and MAC
    network_hosts: dict = field(default_factory=dict)

    # Data about the attacker 
    this: dict = field(default_factory=dict)

    # Data about the malicious Access Point
    hotspot: dict = field(default_factory=dict)

    # Data about the malicious Yeelight
    malicious_yeelight: dict = field(default_factory=dict)

    # Data about the Yeelight
    yeelight: dict = field(default_factory=dict)

    # List of interfaces and their selected use
    interfaces: dict = field(default_factory=dict)

    ssid: dict = field(default_factory=dict)

