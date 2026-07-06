from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, id_key


class Device(Base):
    """物联网设备表"""

    __tablename__ = 'iot_device'

    id: Mapped[id_key] = mapped_column(init=False)
    device_id: Mapped[str] = mapped_column(
        sa.String(64), unique=True, index=True, comment='设备唯一标识符 (MQTT client_id 或自定义 ID)'
    )
    name: Mapped[str] = mapped_column(sa.String(128), comment='设备名称')
    type: Mapped[str] = mapped_column(sa.String(64), comment='设备类型（如 sensor, actuator, gateway）')
    status: Mapped[int] = mapped_column(default=0, comment='设备状态（0: 离线, 1: 在线, 2: 异常）')
    description: Mapped[str | None] = mapped_column(sa.String(512), default=None, comment='设备描述')
    extra_data: Mapped[str | None] = mapped_column(
        sa.Text, default=None, comment='设备扩展数据 (JSON 格式，如位置、固件版本等)'
    )
    last_online: Mapped[datetime | None] = mapped_column(
        TimeZone, default=None, comment='最后在线时间'
    )
