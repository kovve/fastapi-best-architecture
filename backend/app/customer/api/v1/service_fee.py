from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.service_fee import CreateServiceFeeParam, GetServiceFeeDetail, UpdateServiceFeeParam
from backend.app.customer.service.service_fee_service import service_fee_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取服务费详情', dependencies=[DependsJwtAuth])
async def get_service_fee(
    db: CurrentSession, pk: Annotated[int, Path(description='记录 ID')]
) -> ResponseSchemaModel[GetServiceFeeDetail]:
    return response_base.success(data=await service_fee_service.get(db=db, pk=pk))


@router.get('', summary='获取服务费列表（按企业）', dependencies=[DependsJwtAuth])
async def get_service_fee_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    payment_status: Annotated[str | None, Query(description='收款状态')] = None,
) -> ResponseSchemaModel[list[GetServiceFeeDetail]]:
    return response_base.success(
        data=await service_fee_service.get_by_enterprise(db=db, enterprise_id=enterprise_id, payment_status=payment_status)
    )


@router.post('', summary='创建服务费', dependencies=[DependsJwtAuth])
async def create_service_fee(db: CurrentSessionTransaction, obj: CreateServiceFeeParam) -> ResponseModel:
    await service_fee_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', summary='更新服务费', dependencies=[DependsJwtAuth])
async def update_service_fee(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')], obj: UpdateServiceFeeParam
) -> ResponseModel:
    count = await service_fee_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()


@router.delete('/{pk}', summary='删除服务费', dependencies=[DependsJwtAuth])
async def delete_service_fee(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')]) -> ResponseModel:
    count = await service_fee_service.delete(db=db, pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
