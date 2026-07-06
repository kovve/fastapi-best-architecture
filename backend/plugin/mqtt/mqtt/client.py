import asyncio
import json

import aiomqtt

from backend.common.log import log
from backend.core.conf import settings


class MqttClientManager:
    """MQTT 客户端管理器 — 连接/重连/发布/启停"""

    _client_task: asyncio.Task | None = None
    _client: aiomqtt.Client | None = None

    @classmethod
    def get_client(cls) -> aiomqtt.Client | None:
        """获取当前 MQTT 客户端实例（用于发布消息）"""
        return cls._client

    @classmethod
    async def connect_and_listen(cls) -> None:  # noqa: C901
        """连接 MQTT Broker 并持续监听消息"""
        from backend.plugin.mqtt.mqtt.handler import mqtt_handler_registry

        reconnect_attempts = 0

        while reconnect_attempts < settings.MQTT_MAX_RECONNECT_ATTEMPTS:
            try:
                async with aiomqtt.Client(
                    hostname=settings.MQTT_HOST,
                    port=settings.MQTT_PORT,
                    username=settings.MQTT_USERNAME or None,
                    password=settings.MQTT_PASSWORD or None,
                    client_id=settings.MQTT_CLIENT_ID,
                    keepalive=settings.MQTT_KEEPALIVE,
                ) as client:
                    cls._client = client
                    reconnect_attempts = 0
                    log.info(f'[MQTT] Broker 连接成功: {settings.MQTT_HOST}:{settings.MQTT_PORT}')

                    # 订阅所有已注册的 topic
                    for topic_pattern in mqtt_handler_registry.get_topics():
                        await client.subscribe(topic_pattern)
                        log.info(f'[MQTT] 已订阅主题: {topic_pattern}')

                    # 消息接收循环
                    async for message in client.messages:
                        await mqtt_handler_registry.dispatch(message)

            except asyncio.CancelledError:
                log.info('[MQTT] 客户端任务被取消')
                break
            except aiomqtt.MqttError as e:
                reconnect_attempts += 1
                log.error(f'[MQTT] 连接异常 ({reconnect_attempts}/{settings.MQTT_MAX_RECONNECT_ATTEMPTS}): {e}')
                if reconnect_attempts >= settings.MQTT_MAX_RECONNECT_ATTEMPTS:
                    log.error('[MQTT] 达到最大重连次数，停止连接')
                    break
                await asyncio.sleep(settings.MQTT_RECONNECT_DELAY)
            finally:
                cls._client = None

    @classmethod
    def start_listener(cls) -> None:
        """启动 MQTT 监听器（后台 asyncio Task）"""
        if cls._client_task is None or cls._client_task.done():
            cls._client_task = asyncio.create_task(cls.connect_and_listen())

    @classmethod
    async def stop_listener(cls) -> None:
        """停止 MQTT 监听器"""
        if cls._client_task is None:
            return
        if not cls._client_task.done():
            cls._client_task.cancel()
            try:
                await cls._client_task
            except asyncio.CancelledError:
                pass
        cls._client_task = None

    @classmethod
    async def publish(cls, topic: str, payload: dict | str, qos: int = 1) -> None:
        """
        发布 MQTT 消息

        :param topic: 目标主题
        :param payload: 消息内容（dict 自动转 JSON）
        :param qos: QoS 等级
        :return:
        """
        client = cls.get_client()
        if client is None:
            log.warning('[MQTT] 客户端未连接，无法发布消息')
            return
        if isinstance(payload, dict):
            payload = json.dumps(payload, ensure_ascii=False)
        await client.publish(topic, payload, qos=qos)


mqtt_client_manager = MqttClientManager()
