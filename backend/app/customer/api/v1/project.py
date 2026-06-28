from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.customer.schema.project_record import CreateProjectRecordParam, GetProjectRecordDetail, UpdateProjectRecordParam
from backend.app.customer.service.project_record_service import project_record_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取申报项目详情', dependencies=[DependsJwtAuth])
async def get_project_record(
    db: CurrentSession, pk: Annotated[int, Path(description='记录 ID')]
) -> ResponseSchemaModel[GetProjectRecordDetail]:
    return response_base.success(data=await project_record_service.get(db=db, pk=pk))


@router.get('', summary='获取申报项目列表（按企业）', dependencies=[DependsJwtAuth])
async def get_project_record_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    project_name: Annotated[str | None, Query(description='项目名称')] = None,
) -> ResponseSchemaModel[list[GetProjectRecordDetail]]:
    return response_base.success(
        data=await project_record_service.get_by_enterprise(db=db, enterprise_id=enterprise_id, project_name=project_name)
    )


@router.post('', summary='创建申报项目', dependencies=[DependsJwtAuth])
async def create_project_record(db: CurrentSessionTransaction, obj: CreateProjectRecordParam) -> ResponseModel:
    await project_record_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', summary='更新申报项目', dependencies=[DependsJwtAuth])
async def update_project_record(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')], obj: UpdateProjectRecordParam
) -> ResponseModel:
    count = await project_record_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()


@router.delete('/{pk}', summary='删除申报项目', dependencies=[DependsJwtAuth])
async def delete_project_record(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='记录 ID')]) -> ResponseModel:
    count = await project_record_service.delete(db=db, pk=pk)
    return response_base.success() if count > 0 else response_base.fail()
