
from fastapi import FastAPI
from fastapi.testclient import TestClient

import uvicorn

from app import schemas
from app import service
from app import repository
from app.exceptions import RackLimitError

# from entities import Device, Rack

# from typing import AsyncIterator, Dict, Any
# from contextlib import asynccontextmanager
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#
#     print('app started')
#
#     yield  # The application runs here
#
#     print('shutting down')

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

client = TestClient(app)


def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


@app.post("/add_rack")
async def add_rack(s_rack: schemas.Rack):
    # print("rack received", s_rack)
    a_rack = service.to_rack(s_rack)
    repository.add_rack(a_rack)
    return "added rack"


# @app.post("/add_racks")
# async def add_rack(racks: list[schemas.Rack]):
#     print("racks received", racks)


@app.post("/add_device")
async def add_device(s_device: schemas.Device):
    # print("device received", s_device)

    a_device = service.to_device(s_device)
    # print("device transformed", a_device)
    repository.add_device(a_device)
    return "added device"


# @app.post("/add_devices")
# async def add_device(devices: list[schemas.Device]):
#     print("devices received", devices)


@app.post("/add_group")
async def add_device(group: schemas.Group):
    # print("group received", group)
    s_racks = group.racks
    s_devices = group.devices

    racks = []
    for s_rack in s_racks:
        a_rack = service.to_rack(s_rack)
        racks.append(a_rack)

    devices = []
    for s_device in s_devices:
        a_device = service.to_device(s_device)
        devices.append(a_device)

    repository.add_racks(racks)
    repository.add_devices(devices)

    return "added group"


@app.post("/do_balance")
async def add_device():
    rack_list = list(repository.rack_dict.values())
    for rack in rack_list:
        rack.reset_free_units()
        rack.reset_free_usage_w()
        rack.set_device_storage([])
    device_list = list(repository.device_dict.values())
    bal_racks, devs, uninserted_devices = service.balance_racks(rack_list, device_list)

    # if len(uninserted_devices) > 0:
    #     raise RackLimitError()

    balanced_racks = []
    for rack in bal_racks:
        s_rack = service.to_schemas_rack(rack)

        balanced_racks.append(s_rack)

    repository.rack_list = balanced_racks

    if len(uninserted_devices) > 0:
        print("Rack limit reached. Not all devices were stored.")

    return balanced_racks


# @app.post("/check_balance")
# async def add_device():


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000, workers=4)


# documentation by default at: http://127.0.0.1:8000/docs
