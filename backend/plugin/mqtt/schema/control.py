from pydantic import Field

from backend.common.schema import SchemaBase


class SendCommandParam(SchemaBase):
    """下发设备指令参数"""

    device_id: str = Field(description='设备唯一标识符')
    command: str = Field(description='指令名称')
    params: dict | None = Field(None, description='指令参数')
