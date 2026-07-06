from datetime import datetime

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.mqtt.model.device_data import DeviceData


class CRUDDeviceData(CRUDPlus[DeviceData]):
    """设备遥测数据数据库操作类"""

    async def create(
        self,
        db: AsyncSession,
        device_id: str,
        metric_key: str,
        metric_value: str,
        unit: str | None = None,
        quality: int | None = None,
    ) -> None:
        """
        创建遥测数据记录

        :param db: 数据库会话
        :param device_id: 设备唯一标识符
        :param metric_key: 指标名称
        :param metric_value: 指标值
        :param unit: 单位
        :param quality: 数据质量
        :return:
        """
        obj = DeviceData(
            device_id=device_id,
            metric_key=metric_key,
            metric_value=metric_value,
            unit=unit,
            quality=quality,
        )
        db.add(obj)
        await db.flush()

    async def get_select(
        self,
        device_id: str | None,
        metric_key: str | None,
        start_time: datetime | None,
        end_time: datetime | None,
    ) -> Select:
        """
        构建遥测数据筛选查询

        :param device_id: 设备唯一标识符
        :param metric_key: 指标名称
        :param start_time: 起始时间
        :param end_time: 结束时间
        :return:
        """
        filters: dict = {}
        if device_id is not None:
            filters['device_id'] = device_id
        if metric_key is not None:
            filters['metric_key'] = metric_key
        if start_time is not None:
            filters['created_time__ge'] = start_time
        if end_time is not None:
            filters['created_time__le'] = end_time
        return await self.select_order('created_time', 'desc', **filters)


device_data_dao: CRUDDeviceData = CRUDDeviceData(DeviceData)
