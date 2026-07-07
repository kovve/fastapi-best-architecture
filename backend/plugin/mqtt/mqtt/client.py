import asyncio
import json
import sys
import threading

import aiomqtt

from backend.common.log import log
from backend.core.conf import settings


class MqttClientManager:
    """MQTT 客户端管理器 — 连接/重连/发布/启停

    MQTT 客户端运行在独立线程中，使用专用的 SelectorEventLoop。
    这是因为 Granian 在 Windows 上硬编码使用 ProactorEventLoop
    （见 granian/_loops.py build_asyncio_loop），而 ProactorEventLoop
    不支持 aiomqtt 所需的 add_writer()，会抛出 NotImplementedError。
    """

    _client_task: asyncio.Task | None = None
    _client: aiomqtt.Client | None = None
    _loop: asyncio.AbstractEventLoop | None = None
    _thread: threading.Thread | None = None

    @classmethod
    def get_client(cls) -> aiomqtt.Client | None:
        """获取当前 MQTT 客户端实例（用于发布消息）"""
        return cls._client

    @classmethod
    async def connect_and_listen(cls) -> None:  # noqa: C901
        """连接 MQTT Broker 并持续监听消息"""
        from backend.plugin.mqtt.mqtt.handler import mqtt_handler_registry

        # 数值型配置从 .env 读取时为字符串，需显式转换
        port = int(settings.MQTT_PORT)
        keepalive = int(settings.MQTT_KEEPALIVE)
        max_attempts = int(settings.MQTT_MAX_RECONNECT_ATTEMPTS)
        reconnect_delay = int(settings.MQTT_RECONNECT_DELAY)

        reconnect_attempts = 0
        log.info(f'[MQTT] Broker 连接开始: {settings.MQTT_HOST}:{port}')

        while reconnect_attempts < max_attempts:
            try:
                async with aiomqtt.Client(
                    hostname=settings.MQTT_HOST,
                    port=port,
                    username=settings.MQTT_USERNAME or None,
                    password=settings.MQTT_PASSWORD or None,
                    identifier=settings.MQTT_CLIENT_ID,
                    keepalive=keepalive,
                ) as client:
                    cls._client = client
                    reconnect_attempts = 0
                    log.info(f'[MQTT] Broker 连接成功: {settings.MQTT_HOST}:{port}')

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
                log.error(f'[MQTT] MQTT 协议异常 ({reconnect_attempts}/{max_attempts}): {e}')
                if reconnect_attempts >= max_attempts:
                    log.error('[MQTT] 达到最大重连次数，停止连接')
                    break
                await asyncio.sleep(reconnect_delay)
            except Exception as e:
                reconnect_attempts += 1
                log.error(f'[MQTT] 连接异常 ({reconnect_attempts}/{max_attempts}): {type(e).__name__}: {e}')
                if reconnect_attempts >= max_attempts:
                    log.error('[MQTT] 达到最大重连次数，停止连接')
                    break
                await asyncio.sleep(reconnect_delay)
            finally:
                cls._client = None

    @classmethod
    def _run_loop(cls) -> None:
        """在独立线程中运行专用事件循环

        Windows 上显式创建 SelectorEventLoop（而非 Granian 的 ProactorEventLoop），
        因为 aiomqtt 依赖 add_writer()，而 ProactorEventLoop 不支持该方法。
        """
        if sys.platform == 'win32':
            cls._loop = asyncio.SelectorEventLoop()
        else:
            cls._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls._loop)
        cls._client_task = cls._loop.create_task(cls.connect_and_listen())
        try:
            cls._loop.run_until_complete(cls._client_task)
        except asyncio.CancelledError:
            pass
        finally:
            cls._loop.close()
            cls._loop = None
            cls._client_task = None

    @classmethod
    def start_listener(cls) -> None:
        """启动 MQTT 监听器（独立线程 + 专用事件循环）"""
        if cls._thread is None or not cls._thread.is_alive():
            cls._thread = threading.Thread(target=cls._run_loop, daemon=True)
            cls._thread.start()

    @classmethod
    async def stop_listener(cls) -> None:
        """停止 MQTT 监听器"""
        if cls._loop is None or cls._thread is None:
            return
        if cls._client_task is not None and not cls._client_task.done():
            cls._loop.call_soon_threadsafe(cls._client_task.cancel)
        cls._thread.join(timeout=10)
        cls._thread = None

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
        # 确保发布操作在 MQTT 客户端的事件循环上执行（跨线程安全）
        if cls._loop is not None:
            future = asyncio.run_coroutine_threadsafe(
                client.publish(topic, payload, qos=qos),
                cls._loop,
            )
            await asyncio.wrap_future(future)
        else:
            await client.publish(topic, payload, qos=qos)


mqtt_client_manager = MqttClientManager()
