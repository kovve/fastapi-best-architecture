from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession
from backend.plugin.mqtt.schema.telemetry import GetTelemetryDetail
from backend.plugin.mqtt.service.device_service import device_service

router = APIRouter()


@router.get('', summary='查询遥测数据', dependencies=[DependsJwtAuth, DependsPagination])
async def query_telemetry(
    db: CurrentSession,
    device_id: Annotated[str | None, Query(description='设备 ID')] = None,
    metric_key: Annotated[str | None, Query(description='指标名称')] = None,
    start_time: Annotated[datetime | None, Query(description='起始时间')] = None,
    end_time: Annotated[datetime | None, Query(description='结束时间')] = None,
) -> ResponseSchemaModel[PageData[GetTelemetryDetail]]:
    page_data = await device_service.query_telemetry(
        db=db,
        device_id=device_id,
        metric_key=metric_key,
        start_time=start_time,
        end_time=end_time,
    )
    return response_base.success(data=page_data)
