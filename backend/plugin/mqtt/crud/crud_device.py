import json

from collections.abc import Sequence

from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.common.exception import errors
from backend.plugin.mqtt.model.device import Device
from backend.plugin.mqtt.schema.device import CreateDeviceParam, UpdateDeviceParam
from backend.utils.timezone import timezone


class CRUDDevice(CRUDPlus[Device]):
    """设备数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Device | None:
        """
        获取设备

        :param db: 数据库会话
        :param pk: 主键 ID
        :return:
        """
        return await self.select_model(db, pk, deleted=0)

    async def get_by_device_id(self, db: AsyncSession, device_id: str) -> Device | None:
        """
        通过 device_id 获取设备

        :param db: 数据库会话
        :param device_id: 设备唯一标识符
        :return:
        """
        return await self.select_model_by_column(db, device_id=device_id, deleted=0)

    async def get_select(
        self, name: str | None, type: str | None, status: int | None
    ) -> Select:
        """
        构建设备筛选查询

        :param name: 设备名称（模糊匹配）
        :param type: 设备类型
        :param status: 设备状态
        :return:
        """
        filters: dict = {'deleted': 0}
        if name is not None:
            filters['name__like'] = f'%{name}%'
        if type is not None:
            filters['type'] = type
        if status is not None:
            filters['status'] = status
        return await self.select_order('created_time', 'desc', **filters)

    async def get_all(self, db: AsyncSession) -> Sequence[Device]:
        """
        获取所有设备

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, deleted=0)

    async def create(self, db: AsyncSession, obj: CreateDeviceParam) -> None:
        """
        创建设备

        :param db: 数据库会话
        :param obj: 创建设备参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDeviceParam) -> int:
        """
        更新设备

        :param db: 数据库会话
        :param pk: 主键 ID
        :param obj: 更新设备参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=pk, deleted=0)

    async def update_status(
        self, db: AsyncSession, device_id: str, status: int, metadata: dict | None = None
    ) -> None:
        """
        更新设备状态

        :param db: 数据库会话
        :param device_id: 设备唯一标识符
        :param status: 新状态
        :param metadata: 可选的元数据更新
        :return:
        """
        values: dict = {
            'status': status,
            'last_online': timezone.now(),
        }
        if metadata is not None:
            values['metadata'] = json.dumps(metadata, ensure_ascii=False)
        stmt = update(Device).where(Device.device_id == device_id, Device.deleted == 0).values(**values)
        await db.execute(stmt)

    async def update_last_online(self, db: AsyncSession, device_id: str) -> None:
        """
        更新设备最后在线时间

        :param db: 数据库会话
        :param device_id: 设备唯一标识符
        :return:
        """
        stmt = (
            update(Device)
            .where(Device.device_id == device_id, Device.deleted == 0)
            .values(last_online=timezone.now(), status=1)
        )
        await db.execute(stmt)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除设备（逻辑删除）

        :param db: 数据库会话
        :param pks: 主键 ID 列表
        :return:
        """
        return await self.delete_model_by_column(
            db,
            allow_multiple=True,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id__in=pks,
            deleted=0,
        )


device_dao: CRUDDevice = CRUDDevice(Device)
