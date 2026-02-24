from app.entities import Rack, Device

rack_dict = {}
device_dict = {}
rack_list = []


def add_rack(a_rack: Rack.Rack):
    rack_dict[a_rack.get_serial_num()] = a_rack


def add_device(a_device: Device.Device):
    device_dict[a_device.get_serial_num()] = a_device


def add_racks(a_racks: list):
    for a_rack in a_racks:
        add_rack(a_rack)


def add_devices(a_devices: list):
    for a_device in a_devices:
        add_device(a_device)
