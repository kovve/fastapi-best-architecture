from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, TimeZone, id_key
from backend.utils.timezone import timezone


class DeviceData(DataClassBase):
    """物联网设备遥测数据表"""

    __tablename__ = 'iot_device_data'

    id: Mapped[id_key] = mapped_column(init=False)
    device_id: Mapped[str] = mapped_column(sa.String(64), index=True, comment='设备唯一标识符')
    metric_key: Mapped[str] = mapped_column(sa.String(128), comment='指标名称（如 temperature, humidity, voltage）')
    metric_value: Mapped[str] = mapped_column(sa.Text, comment='指标值（文本存储，支持数值、布尔、JSON 等）')
    unit: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='单位（如 °C、%、V）')
    quality: Mapped[int | None] = mapped_column(default=None, comment='数据质量标记（0: 坏, 1: 不确定, 2: 好）')
    created_time: Mapped[datetime] = mapped_column(
        TimeZone, init=False, default_factory=timezone.now, comment='数据时间戳'
    )
