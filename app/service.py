from app.entities import Rack, Device
from app import schemas
from app.exceptions import RackLimitError


def to_rack(s_rack: schemas.Rack) -> Rack.Rack:
    return Rack.Rack(s_rack.name, s_rack.description, s_rack.serial_num, s_rack.units_capacity, s_rack.max_usage_w, s_rack.device_storage)


def to_device(s_device: schemas.Device) -> Device.Device:
    return Device.Device(s_device.d_type, s_device.name, s_device.description, s_device.serial_num, s_device.num_of_units, s_device.usage_w)


def to_schemas_rack(rack: Rack.Rack) -> schemas.Rack:
    devices = []
    for device in rack.get_device_storage():
        s_device = to_schemas_device(device)
        devices.append(s_device)

    return schemas.Rack(name=rack.get_name(), description=rack.get_description(), serial_num=rack.get_serial_num(),
                        units_capacity=rack.get_units_capacity(),
                        max_usage_w=rack.get_max_usage_w(), device_storage=devices,
                        usage_prctg_w=(rack.get_max_usage_w() - rack.get_free_usage_w()) / rack.get_max_usage_w(),
                        used_units=rack.get_units_capacity() - rack.get_free_units(), used_w=rack.get_max_usage_w() - rack.get_free_usage_w())


def to_schemas_device(device: Device.Device) -> schemas.Device:
    return schemas.Device(name=device.get_name(), d_type=device.get_d_type(),
                          description=device.get_description(), serial_num=device.get_serial_num(),
                          num_of_units=device.get_num_of_units(), usage_w=device.get_usage_w())


def balance_racks(racks: list[Rack.Rack], devices: list[Device.Device]):
    racks = sorted(racks, key=lambda r: r.get_max_usage_w(), reverse=True)
    devices = sorted(devices, key=lambda d: d.get_usage_w(), reverse=True)

    tot_max_capacity = sum(r.get_max_usage_w() for r in racks)
    tot_usage = sum(d.get_usage_w() for d in devices)

    uninserted_devices = []

    racks_total = len(racks)
    dev_total = len(devices)

    dev_count = 0
    last_inserted_rack = 0
    for device in devices:
        dev_count += 1
        inserted = False

        rack_order = []
        for i in range(racks_total):
            rack_index = last_inserted_rack + i
            if rack_index >= racks_total:
                rack_index = rack_index - racks_total
            rack_order.append(rack_index)

        current_max_usage_w = 0
        current_max_usg_i = 0
        for rack_index in rack_order:
            current_usage_w = ((racks[rack_index].get_max_usage_w() - racks[rack_index].get_free_usage_w())
                               / racks[rack_index].get_max_usage_w())
            new_current_usage_w = ((racks[rack_index].get_max_usage_w() - racks[rack_index].get_free_usage_w() + device.get_usage_w())
                                   / racks[rack_index].get_max_usage_w())
            next_rack_index = rack_index + 1
            if next_rack_index == racks_total:
                next_rack_index = 0
            next_usage_w = ((racks[next_rack_index].get_max_usage_w() - racks[next_rack_index].get_free_usage_w())
                            / racks[next_rack_index].get_max_usage_w())
            next_free_units = racks[next_rack_index].get_free_units() - device.get_num_of_units()
            if (current_usage_w > next_usage_w and next_free_units >= 0 or
                    (tot_max_capacity != 0 and
                     new_current_usage_w - current_usage_w >= min(0.999, tot_usage / tot_max_capacity)) and dev_count < dev_total - 1):
                if (racks[rack_index].get_free_usage_w() >= current_max_usage_w and
                        racks[rack_index].get_free_usage_w() >= device.get_usage_w() and
                        racks[rack_index].get_free_units() >= device.get_num_of_units()):
                    current_max_usage_w = racks[rack_index].get_free_usage_w()
                    current_max_usg_i = rack_index
                continue
            inserted = racks[rack_index].add_device(device)

            if inserted:
                last_inserted_rack = rack_index
                if rack_index == racks_total - 1:
                    racks = sorted(racks, key=lambda r: r.get_free_usage_w() / r.get_max_usage_w())
                break
        if not inserted:
            if (racks[current_max_usg_i].get_free_usage_w() >= device.get_usage_w() and
                    racks[current_max_usg_i].get_free_units() >= device.get_num_of_units()):
                inserted = racks[current_max_usg_i].add_device(device)
                if not inserted:
                    uninserted_devices.append(device)
            else:
                uninserted_devices.append(device)

    racks = sorted(racks, key=lambda r: r.get_free_usage_w() / r.get_max_usage_w(), reverse=True)

    return racks, devices, uninserted_devices
