from fastapi import APIRouter

from backend.core.conf import settings

from .v1.device import router as device_router
from .v1.telemetry import router as telemetry_router
from .v1.control import router as control_router

device_router_obj = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/devices', tags=['IoT 设备管理'])
device_router_obj.include_router(device_router)

telemetry_router_obj = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/telemetry', tags=['IoT 遥测数据'])
telemetry_router_obj.include_router(telemetry_router)

control_router_obj = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/control', tags=['IoT 指令下发'])
control_router_obj.include_router(control_router)
