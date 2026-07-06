from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.mqtt.schema.device import (
    CreateDeviceParam,
    DeleteDeviceParam,
    GetDeviceDetail,
    UpdateDeviceParam,
)
from backend.plugin.mqtt.service.device_service import device_service

router = APIRouter()


@router.get('/{pk}', summary='获取设备详情', dependencies=[DependsJwtAuth])
async def get_device(
    db: CurrentSession, pk: Annotated[int, Path(description='设备 ID')]
) -> ResponseSchemaModel[GetDeviceDetail]:
    device = await device_service.get(db=db, pk=pk)
    return response_base.success(data=device)


@router.get('', summary='分页获取设备列表', dependencies=[DependsJwtAuth, DependsPagination])
async def get_devices(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='设备名称')] = None,
    type: Annotated[str | None, Query(description='设备类型')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetDeviceDetail]]:
    page_data = await device_service.get_list(db=db, name=name, type=type, status=status)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建设备',
    dependencies=[
        Depends(RequestPermission('iot:device:add')),
        DependsRBAC,
    ],
)
async def create_device(db: CurrentSessionTransaction, obj: CreateDeviceParam) -> ResponseModel:
    await device_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新设备',
    dependencies=[
        Depends(RequestPermission('iot:device:edit')),
        DependsRBAC,
    ],
)
async def update_device(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='设备 ID')],
    obj: UpdateDeviceParam,
) -> ResponseModel:
    count = await device_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除设备',
    dependencies=[
        Depends(RequestPermission('iot:device:del')),
        DependsRBAC,
    ],
)
async def delete_devices(db: CurrentSessionTransaction, obj: DeleteDeviceParam) -> ResponseModel:
    count = await device_service.delete(db=db, pks=obj.pks)
    if count > 0:
        return response_base.success()
    return response_base.fail()
