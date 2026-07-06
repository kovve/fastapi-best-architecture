from datetime import datetime

from backend.common.log import log
from backend.common.socketio.server import sio


class WebSocketManager:
    """WebSocket 推送管理器 — 基于 Socket.IO 封装，统一事件名和数据结构"""

    @staticmethod
    async def emit_device_telemetry(device_id: str, metrics: list[dict]) -> None:
        """
        推送设备遥测数据

        :param device_id: 设备唯一标识符
        :param metrics: 指标列表
        :return:
        """
        await sio.emit(
            'device_telemetry',
            {
                'device_id': device_id,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat(),
            },
        )

    @staticmethod
    async def emit_device_status_change(device_id: str, status: int) -> None:
        """
        推送设备状态变更

        :param device_id: 设备唯一标识符
        :param status: 设备状态
        :return:
        """
        await sio.emit(
            'device_status_change',
            {
                'device_id': device_id,
                'status': status,
            },
        )


ws_manager = WebSocketManager()
