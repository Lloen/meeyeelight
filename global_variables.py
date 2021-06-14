from dataclasses import dataclass, field


@dataclass
class GlobalData:

    options: dict = field(default_factory=dict)

    network_hosts: dict = field(default_factory=dict)

    this: dict = field(default_factory=dict)

    hotspot: dict = field(default_factory=dict)

    yeelight: dict = field(default_factory=dict)

    phone: dict = field(default_factory=dict)

    interfaces: dict = field(default_factory=dict)
