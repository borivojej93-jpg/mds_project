from app.entities.Device import Device


class Rack:
    def __init__(self, name: str, description: str, serial_num: int, units_capacity: int, max_usage_w: int,
                 device_storage: list[Device]):
        self.__name = name
        self.__description = description
        self.__serial_num = serial_num
        self.__units_capacity = units_capacity
        self.__max_usage_w = max_usage_w
        self.__device_storage = device_storage
        # todo, think whether this is needed, probably good enough to sum it up from device_storage
        self.__free_units = units_capacity
        self.__free_usage_w = max_usage_w

    def get_name(self) -> str:
        return self.__name

    def get_description(self) -> str:
        return self.__description

    def get_serial_num(self) -> int:
        return self.__serial_num

    def get_units_capacity(self) -> int:
        return self.__units_capacity

    def get_max_usage_w(self) -> int:
        return self.__max_usage_w

    def get_device_storage(self) -> list[Device]:
        return self.__device_storage

    def get_free_units(self) -> int:
        return self.__free_units

    def get_free_usage_w(self) -> int:
        return self.__free_usage_w

    def set_name(self, name: str):
        self.__name = name

    def set_description(self, description: str):
        self.__description = description

    def set_serial_num(self, serial_num: int):
        self.__serial_num = serial_num

    def set_units_capacity(self, units_capacity: int):
        self.__units_capacity = units_capacity

    def set_max_usage_w(self, max_usage_w: int):
        self.__max_usage_w = max_usage_w

    def set_device_storage(self, device_storage: list[Device]):
        self.__device_storage = device_storage

    def add_device(self, device: Device):
        if self.__free_units - device.get_num_of_units() >= 0 and self.__free_usage_w - device.get_usage_w() >= 0:
            self.update_free_units(device.get_num_of_units())
            self.update_free_usage_w(device.get_usage_w())
            self.__device_storage.append(device)
            return True
        return False

    def update_free_units(self, free_units: int):
        self.__free_units = self.__free_units - free_units

    def update_free_usage_w(self, free_usage_w: int):
        self.__free_usage_w = self.__free_usage_w - free_usage_w

    def reset_free_units(self):
        self.__free_units = self.__units_capacity

    def reset_free_usage_w(self):
        self.__free_usage_w = self.__max_usage_w

# todo, check total weight and unit capacity and prioritize one above, or closer to the limit
