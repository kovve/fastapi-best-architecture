from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.patent import CreatePatentParam, GetPatentDetail, UpdatePatentParam
from backend.app.customer.service.patent_service import patent_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取专利详情', dependencies=[DependsJwtAuth])
async def get_patent(
    db: CurrentSession, pk: Annotated[int, Path(description='专利 ID')]
) -> ResponseSchemaModel[GetPatentDetail]:
    return response_base.success(data=await patent_service.get(db=db, pk=pk))


@router.get('', summary='获取专利列表（按企业）', dependencies=[DependsJwtAuth])
async def get_patent_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    patent_name: Annotated[str | None, Query(description='专利名称')] = None,
) -> ResponseSchemaModel[list[GetPatentDetail]]:
    return response_base.success(
        data=await patent_service.get_by_enterprise(db=db, enterprise_id=enterprise_id, patent_name=patent_name)
    )


@router.post('', summary='创建专利', dependencies=[DependsJwtAuth])
async def create_patent(db: CurrentSessionTransaction, obj: CreatePatentParam) -> ResponseModel:
    await patent_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', summary='更新专利', dependencies=[DependsJwtAuth])
async def update_patent(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='专利 ID')], obj: UpdatePatentParam
) -> ResponseModel:
    count = await patent_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()


@router.delete('/{pk}', summary='删除专利', dependencies=[DependsJwtAuth])
async def delete_patent(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='专利 ID')]) -> ResponseModel:
    count = await patent_service.delete(db=db, pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
