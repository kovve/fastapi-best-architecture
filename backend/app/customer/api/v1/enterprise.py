from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.enterprise import CreateEnterpriseParam, GetEnterpriseDetail, UpdateEnterpriseParam
from backend.app.customer.service.enterprise_service import enterprise_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取企业详情', dependencies=[DependsJwtAuth])
async def get_enterprise(
    db: CurrentSession, pk: Annotated[int, Path(description='企业 ID')]
) -> ResponseSchemaModel[GetEnterpriseDetail]:
    data = await enterprise_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取企业列表', dependencies=[DependsJwtAuth])
async def get_enterprise_list(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='企业名称')] = None,
    credit_code: Annotated[str | None, Query(description='统一社会信用代码')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[list[GetEnterpriseDetail]]:
    data = await enterprise_service.get_all(db=db, name=name, credit_code=credit_code, status=status)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建企业',
    dependencies=[DependsJwtAuth],
)
async def create_enterprise(db: CurrentSessionTransaction, obj: CreateEnterpriseParam) -> ResponseModel:
    await enterprise_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新企业',
    dependencies=[DependsJwtAuth],
)
async def update_enterprise(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='企业 ID')], obj: UpdateEnterpriseParam
) -> ResponseModel:
    count = await enterprise_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除企业',
    dependencies=[DependsJwtAuth],
)
async def delete_enterprise(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='企业 ID')]) -> ResponseModel:
    count = await enterprise_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
