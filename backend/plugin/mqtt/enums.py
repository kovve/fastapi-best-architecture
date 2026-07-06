from backend.common.enums import IntEnum


class DeviceStatus(IntEnum):
    """设备状态"""

    offline = 0
    online = 1
    error = 2


class DataQuality(IntEnum):
    """数据质量"""

    bad = 0
    uncertain = 1
    good = 2
