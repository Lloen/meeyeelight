class YeelightMessage():
    def __init__(self):
        self._magic_number = None
        self._packet_length = None
        self._unknown = None
        self._device_id = None
        self._stamp = None
        self._md5_checksum = None
        self._data = None
        self._message = None

    @property
    def magic_number(self):
        return self._magic_number

    @property
    def packet_length(self):
        return self._packet_length

    @property
    def unknown(self):
        return self._unknown
    
    @property
    def device_id(self):
        return self._device_id

    @property
    def stamp(self):
        return self._stamp

    @property
    def md5_checksum(self):
        return self._md5_checksum

    @property
    def data(self):
        return self._data

    @property 
    def message(self):
        self._message = f"{self.magic_number}{self.packet_length}{self.unknown}{self.device_id}{self.stamp}{self.md5_checksum}{self.data}"
        return self._message

    @magic_number.setter
    def magic_number(self, value):
        self._magic_number = value

    @packet_length.setter
    def packet_length(self, value):
        self._packet_length = value

    @unknown.setter
    def unknown(self, value):
        self._unknown = value

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @stamp.setter
    def stamp(self, value):
        self._stamp = value

    @md5_checksum.setter
    def md5_checksum(self, value):
        self._md5_checksum = value

    @data.setter
    def data(self, value):
        self._data = value
