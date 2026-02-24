class Device:
    def __init__(self, d_type: str, name: str, description: str, serial_num: int, num_of_units: int, usage_w: int):
        self.__d_type = d_type
        self.__name = name
        self.__description = description
        self.__serial_num = serial_num
        self.__num_of_units = num_of_units
        self.__usage_w = usage_w

    def get_d_type(self):
        return self.__d_type

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_serial_num(self):
        return self.__serial_num

    def get_num_of_units(self):
        return self.__num_of_units

    def get_usage_w(self):
        return self.__usage_w

    def set_d_type(self, d_type):
        self.__name = d_type

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_serial_num(self, serial_num):
        self.__serial_num = serial_num

    def set_num_of_units(self, num_of_units):
        self.__num_of_units = num_of_units

    def set_usage_w(self, usage_w):
        self.__usage_w = usage_w
