from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.financial_data import (
    CreateFinancialDataParam,
    GetFinancialDataDetail,
    UpdateFinancialDataParam,
)
from backend.app.customer.service.financial_data_service import financial_data_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取财务数据详情', dependencies=[DependsJwtAuth])
async def get_financial_data(
    db: CurrentSession, pk: Annotated[int, Path(description='财务数据 ID')]
) -> ResponseSchemaModel[GetFinancialDataDetail]:
    data = await financial_data_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取财务数据列表（按企业）', dependencies=[DependsJwtAuth])
async def get_financial_data_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    year: Annotated[int | None, Query(description='财务年度')] = None,
) -> ResponseSchemaModel[list[GetFinancialDataDetail]]:
    data = await financial_data_service.get_by_enterprise(db=db, enterprise_id=enterprise_id, year=year)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建财务数据',
    dependencies=[DependsJwtAuth],
)
async def create_financial_data(db: CurrentSessionTransaction, obj: CreateFinancialDataParam) -> ResponseModel:
    await financial_data_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新财务数据',
    dependencies=[DependsJwtAuth],
)
async def update_financial_data(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='财务数据 ID')], obj: UpdateFinancialDataParam
) -> ResponseModel:
    count = await financial_data_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除财务数据',
    dependencies=[DependsJwtAuth],
)
async def delete_financial_data(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='财务数据 ID')]
) -> ResponseModel:
    count = await financial_data_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
