from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class GetTelemetryDetail(SchemaBase):
    """遥测数据详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    metric_key: str
    metric_value: str
    unit: str | None = None
    quality: int | None = None
    created_time: datetime
