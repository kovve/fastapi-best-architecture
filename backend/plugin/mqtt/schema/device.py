from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase
from backend.plugin.mqtt.enums import DeviceStatus


class DeviceSchemaBase(SchemaBase):
    """设备基础模型"""

    device_id: str = Field(description='设备唯一标识符')
    name: str = Field(description='设备名称')
    type: str = Field(description='设备类型')
    status: DeviceStatus = Field(default=DeviceStatus.offline, description='设备状态')
    description: str | None = Field(None, description='设备描述')
    extra_data: str | None = Field(None, description='设备扩展数据 (JSON)')


class CreateDeviceParam(DeviceSchemaBase):
    """创建设备参数"""


class UpdateDeviceParam(DeviceSchemaBase):
    """更新设备参数"""


class GetDeviceDetail(DeviceSchemaBase):
    """设备详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
    last_online: datetime | None = None


class DeleteDeviceParam(SchemaBase):
    """批量删除设备参数"""

    pks: list[int] = Field(description='设备主键 ID 列表')
