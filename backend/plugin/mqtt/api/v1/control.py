from fastapi import APIRouter, Depends

from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.plugin.mqtt.schema.control import SendCommandParam
from backend.plugin.mqtt.service.device_service import device_service

router = APIRouter()


@router.post(
    '/send',
    summary='下发设备控制指令',
    dependencies=[
        Depends(RequestPermission('iot:control:send')),
        DependsRBAC,
    ],
)
async def send_command(obj: SendCommandParam) -> ResponseModel:
    await device_service.send_command(device_id=obj.device_id, command=obj.command, params=obj.params)
    return response_base.success()
