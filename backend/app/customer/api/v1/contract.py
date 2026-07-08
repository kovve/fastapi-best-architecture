from typing import Annotated

from anyio import open_file
from fastapi import APIRouter, Depends, Path, Query
from starlette.responses import StreamingResponse

from backend.app.customer.schema.contract import CreateContractParam, GetContractDetail, UpdateContractParam
from backend.app.customer.service.contract_service import contract_service
from backend.common.exception import errors
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.core.path_conf import UPLOAD_DIR
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='获取合同详情', dependencies=[DependsJwtAuth])
async def get_contract(
    db: CurrentSession, pk: Annotated[int, Path(description='合同 ID')]
) -> ResponseSchemaModel[GetContractDetail]:
    data = await contract_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取合同列表（按企业）', dependencies=[DependsJwtAuth])
async def get_contract_list(
    db: CurrentSession,
    enterprise_id: Annotated[int | None, Query(description='企业 ID')] = None,
    contract_name: Annotated[str | None, Query(description='合同名称')] = None,
) -> ResponseSchemaModel[list[GetContractDetail]]:
    data = await contract_service.get_by_enterprise(db=db, enterprise_id=enterprise_id, contract_name=contract_name)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建合同',
    dependencies=[DependsJwtAuth],
)
async def create_contract(db: CurrentSessionTransaction, obj: CreateContractParam) -> ResponseModel:
    await contract_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新合同',
    dependencies=[DependsJwtAuth],
)
async def update_contract(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='合同 ID')], obj: UpdateContractParam
) -> ResponseModel:
    count = await contract_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除合同',
    dependencies=[DependsJwtAuth],
)
async def delete_contract(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='合同 ID')]) -> ResponseModel:
    count = await contract_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/{pk}/download', summary='下载合同文件', dependencies=[DependsJwtAuth])
async def download_contract(
    db: CurrentSession, pk: Annotated[int, Path(description='合同 ID')]
) -> StreamingResponse:
    contract = await contract_service.get(db=db, pk=pk)
    if not contract.file_path:
        raise errors.NotFoundError(msg='合同文件不存在')
    filename = contract.file_path.rsplit('/', 1)[-1]
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise errors.NotFoundError(msg='文件不存在')
    file = await open_file(file_path, mode='rb')
    return StreamingResponse(
        file,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )
