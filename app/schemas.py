
from pydantic import BaseModel


class Device(BaseModel):
    d_type: str
    name: str
    description: str
    serial_num: int
    num_of_units: int
    usage_w: int


class Rack(BaseModel):
    usage_prctg_w: float | None = None
    name: str
    description: str
    serial_num: int
    units_capacity: int
    max_usage_w: int
    used_units: int | None = None
    used_w: int | None = None
    device_storage: list[Device]


class Group(BaseModel):
    racks: list[Rack]
    devices: list[Device]
