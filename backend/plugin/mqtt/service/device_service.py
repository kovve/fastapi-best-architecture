import json

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.log import log
from backend.common.pagination import paging_data
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.plugin.mqtt.crud.crud_device import device_dao
from backend.plugin.mqtt.crud.crud_device_data import device_data_dao
from backend.plugin.mqtt.enums import DeviceStatus
from backend.plugin.mqtt.model.device import Device
from backend.plugin.mqtt.schema.device import CreateDeviceParam, UpdateDeviceParam
from backend.plugin.mqtt.ws.websocket_manager import ws_manager


class DeviceService:
    """设备管理服务类 — 唯一业务入口（DB + 缓存 + WebSocket）"""

    # ======================== 缓存辅助 ========================

    @staticmethod
    async def _cache_device_status(device_id: str, status: int) -> None:
        """
        缓存设备在线状态

        :param device_id: 设备唯一标识符
        :param status: 设备状态
        :return:
        """
        key = f'iot:device:{device_id}:status'
        try:
            await redis_client.set(key, status, ex=120)
        except Exception as e:
            log.warning(f'[DeviceService] 缓存设备状态失败: {e}')

    @staticmethod
    async def _get_cached_status(device_id: str) -> int | None:
        """
        获取缓存的设备状态

        :param device_id: 设备唯一标识符
        :return:
        """
        key = f'iot:device:{device_id}:status'
        try:
            value = await redis_client.get(key)
            if value is not None:
                return int(value)
        except Exception as e:
            log.warning(f'[DeviceService] 获取缓存状态失败: {e}')
        return None

    # ======================== MQTT 侧（无 HTTP 上下文）========================

    @staticmethod
    async def handle_telemetry(device_id: str, metrics: list[dict]) -> None:
        """
        处理设备遥测数据 — 持久化 + 缓存更新 + 前端推送

        :param device_id: 设备唯一标识符
        :param metrics: 指标列表 [{"key": "temp", "value": 25.5, "unit": "°C"}, ...]
        :return:
        """
        try:
            async with async_db_session.begin() as db:
                # 批量写入遥测数据
                for metric in metrics:
                    metric_value = metric['value']
                    if not isinstance(metric_value, str):
                        metric_value = json.dumps(metric_value, ensure_ascii=False)
                    await device_data_dao.create(
                        db,
                        device_id=device_id,
                        metric_key=metric['key'],
                        metric_value=metric_value,
                        unit=metric.get('unit'),
                        quality=metric.get('quality'),
                    )

                # 更新设备最后在线时间 + 状态
                await device_dao.update_last_online(db, device_id)

            log.info(f'[DeviceService] 已处理 {len(metrics)} 条遥测数据: device={device_id}')

            # 缓存设备在线状态
            await DeviceService._cache_device_status(device_id, DeviceStatus.online)

            # Socket.IO 推送实时数据到前端
            await ws_manager.emit_device_telemetry(device_id, metrics)

        except Exception as e:
            log.exception(f'[DeviceService] 处理遥测数据失败: device={device_id}, error={e}')

    @staticmethod
    async def handle_status_change(device_id: str, status: int, extra_data: dict | None = None) -> None:
        """
        处理设备状态变更 — 持久化 + 缓存更新 + 前端推送

        :param device_id: 设备唯一标识符
        :param status: 新状态
        :param extra_data: 可选的扩展数据更新
        :return:
        """
        try:
            async with async_db_session.begin() as db:
                device = await device_dao.get_by_device_id(db, device_id)
                if device:
                    await device_dao.update_status(db, device_id, status, extra_data)
                else:
                    log.warning(f'[DeviceService] 未注册设备上报状态: {device_id}')

            # 缓存设备状态
            await DeviceService._cache_device_status(device_id, status)

            # Socket.IO 推送状态变更
            await ws_manager.emit_device_status_change(device_id, status)

        except Exception as e:
            log.exception(f'[DeviceService] 处理设备状态变更失败: device={device_id}, error={e}')

    # ======================== REST API 侧（HTTP 上下文）========================

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Device:
        """
        获取设备详情

        :param db: 数据库会话
        :param pk: 主键 ID
        :return:
        """
        device = await device_dao.get(db, pk)
        if not device:
            raise errors.NotFoundError(msg='设备不存在')

        # 用 Redis 缓存的实时状态覆盖 DB 静态状态
        cached_status = await DeviceService._get_cached_status(device.device_id)
        if cached_status is not None:
            device.status = cached_status

        return device

    @staticmethod
    async def get_list(
        *,
        db: AsyncSession,
        name: str | None,
        type: str | None,
        status: int | None,
    ) -> dict:
        """
        分页查询设备列表

        :param db: 数据库会话
        :param name: 设备名称（模糊匹配）
        :param type: 设备类型
        :param status: 设备状态
        :return:
        """
        stmt = await device_dao.get_select(name, type, status)
        return await paging_data(db, stmt)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDeviceParam) -> None:
        """
        创建设备

        :param db: 数据库会话
        :param obj: 创建设备参数
        :return:
        """
        existing = await device_dao.get_by_device_id(db, obj.device_id)
        if existing:
            raise errors.ConflictError(msg=f'设备 {obj.device_id} 已存在')
        await device_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDeviceParam) -> int:
        """
        更新设备

        :param db: 数据库会话
        :param pk: 主键 ID
        :param obj: 更新设备参数
        :return:
        """
        device = await device_dao.get(db, pk)
        if not device:
            raise errors.NotFoundError(msg='设备不存在')

        if device.device_id != obj.device_id:
            existing = await device_dao.get_by_device_id(db, obj.device_id)
            if existing:
                raise errors.ConflictError(msg=f'设备 {obj.device_id} 已存在')

        count = await device_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除设备（逻辑删除）

        :param db: 数据库会话
        :param pks: 主键 ID 列表
        :return:
        """
        count = await device_dao.delete(db, pks)
        return count

    @staticmethod
    async def query_telemetry(
        *,
        db: AsyncSession,
        device_id: str | None = None,
        metric_key: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> dict:
        """
        查询遥测数据（分页）

        :param db: 数据库会话
        :param device_id: 设备唯一标识符
        :param metric_key: 指标名称
        :param start_time: 起始时间
        :param end_time: 结束时间
        :return:
        """
        stmt = await device_data_dao.get_select(device_id, metric_key, start_time, end_time)
        return await paging_data(db, stmt)

    @staticmethod
    async def send_command(device_id: str, command: str, params: dict | None = None) -> None:
        """
        下发设备控制指令

        :param device_id: 设备唯一标识符
        :param command: 指令名称
        :param params: 指令参数
        :return:
        """
        from backend.plugin.mqtt.mqtt.client import mqtt_client_manager

        # 验证设备存在且在线
        async with async_db_session() as db:
            device = await device_dao.get_by_device_id(db, device_id)
            if not device:
                raise errors.NotFoundError(msg=f'设备 {device_id} 不存在')

        # 用缓存优先判断在线状态
        cached_status = await DeviceService._get_cached_status(device_id)
        is_online = cached_status == DeviceStatus.online if cached_status is not None else device.status == DeviceStatus.online

        if not is_online:
            raise errors.RequestError(msg=f'设备 {device_id} 当前离线，无法下发指令')

        # 构建 MQTT 消息并发布
        topic = settings.MQTT_DEVICE_CONTROL_TOPIC.format(device_id=device_id)
        payload = {
            'command': command,
            'params': params or {},
        }

        await mqtt_client_manager.publish(topic, payload, qos=1)
        log.info(f'[DeviceService] 指令已下发: device={device_id}, command={command}')


device_service = DeviceService()
