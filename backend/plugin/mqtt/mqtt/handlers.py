"""MQTT 消息处理器 — 设备遥测数据与状态变更"""

import json

from backend.common.log import log
from backend.plugin.mqtt.mqtt.handler import mqtt_handler_registry


@mqtt_handler_registry.register('device/+/data')
async def handle_device_data(topic: str, payload: str, w0: str) -> None:
    """
    处理设备遥测数据消息

    topic 模式: device/{device_id}/data
    payload 格式: {"metrics": [{"key": "temperature", "value": 25.5, "unit": "°C"}, ...]}

    :param topic: MQTT 主题
    :param payload: 消息体
    :param w0: 从 topic 提取的设备 ID
    :return:
    """
    device_id = w0
    log.info(f'[MQTT] 接收 topic={topic}  payload ={payload} w0 = {w0}')
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        log.warning(f'[MQTT] 设备数据消息 JSON 解析失败: device={device_id}, payload={payload[:100]}')
        return

    metrics = data.get('metrics', [])
    if not metrics:
        log.warning(f'[MQTT] 设备数据消息缺少 metrics 字段: device={device_id}')
        return

    from backend.plugin.mqtt.service.device_service import device_service

    await device_service.handle_telemetry(device_id=device_id, metrics=metrics)


@mqtt_handler_registry.register('device/+/status')
async def handle_device_status(topic: str, payload: str, w0: str) -> None:
    """
    处理设备状态变更消息

    topic 模式: device/{device_id}/status
    payload 格式: {"status": 1, "metadata": {...}}

    :param topic: MQTT 主题
    :param payload: 消息体
    :param w0: 从 topic 提取的设备 ID
    :return:
    """
    device_id = w0
    log.info(f'[MQTT] 接收 topic={topic}  payload ={payload} w0 = {w0}')
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        log.warning(f'[MQTT] 设备状态消息 JSON 解析失败: device={device_id}')
        return

    status = data.get('status', 0)
    extra_data = data.get('extra_data')

    from backend.plugin.mqtt.service.device_service import device_service

    await device_service.handle_status_change(device_id=device_id, status=status, extra_data=extra_data)
