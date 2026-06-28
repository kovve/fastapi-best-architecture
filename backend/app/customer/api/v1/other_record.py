from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.other_record import CreateOtherRecordParam, GetOtherRecordDetail, UpdateOtherRecordParam
from backend.app.customer.service.other_record_service import other_record_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取其他记录详情', dependencies=[DependsJwtAuth])
async def get_other_record(
    db: CurrentSession, pk: Annotated[int, Path(description='记录 ID')]
) -> ResponseSchemaModel[GetOtherRecordDetail]:
    return response_base.success(data=await other_record_service.get(db=db, pk=pk))


@router.get('', summary='获取其他记录列表（按企业）', dependencies=[DependsJwtAuth])
async def get_other_record_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    record_type: Annotated[str | None, Query(description='记录类型')] = None,
    title: Annotated[str | None, Query(description='标题')] = None,
) -> ResponseSchemaModel[list[GetOtherRecordDetail]]:
    return response_base.success(
        data=await other_record_service.get_by_enterprise(
            db=db, enterprise_id=enterprise_id, record_type=record_type, title=title
        )
    )


@router.post('', summary='创建其他记录', dependencies=[DependsJwtAuth])
async def create_other_record(db: CurrentSessionTransaction, obj: CreateOtherRecordParam) -> ResponseModel:
    await other_record_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', summary='更新其他记录', dependencies=[DependsJwtAuth])
async def update_other_record(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')], obj: UpdateOtherRecordParam
) -> ResponseModel:
    count = await other_record_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()


@router.delete('/{pk}', summary='删除其他记录', dependencies=[DependsJwtAuth])
async def delete_other_record(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')]) -> ResponseModel:
    count = await other_record_service.delete(db=db, pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
