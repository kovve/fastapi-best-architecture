from fastapi import APIRouter

from backend.core.conf import settings

from .v1.device import router as device_router
from .v1.telemetry import router as telemetry_router
from .v1.control import router as control_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}')

v1.include_router(device_router, prefix='/devices', tags=['IoT 设备管理'])
v1.include_router(telemetry_router, prefix='/telemetry', tags=['IoT 遥测数据'])
v1.include_router(control_router, prefix='/control', tags=['IoT 指令下发'])
