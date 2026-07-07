import re

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import aiomqtt

from backend.common.log import log


@dataclass
class MqttHandler:
    """MQTT 消息处理器条目"""

    topic_pattern: str
    regex: re.Pattern
    func: Callable[..., Awaitable[None]]
    param_names: list[str]


class MqttHandlerRegistry:
    """MQTT 消息处理器注册表 — 装饰器注册 + 正则匹配分发"""

    def __init__(self) -> None:
        self._handlers: list[MqttHandler] = []

    def register(self, topic: str) -> Callable:
        """
        装饰器：注册 MQTT 消息处理器

        用法::

            @mqtt_handler_registry.register('device/+/data')
            async def handle_device_data(topic: str, payload: str, w0: str) -> None:
                ...

        :param topic: MQTT 主题模式，支持 + 单层通配符
        :return:
        """
        parts = topic.split('/')
        regex_parts: list[str] = []
        param_names: list[str] = []
        wildcard_index = 0

        for part in parts:
            if part == '+':
                param_name = f'w{wildcard_index}'
                regex_parts.append(f'(?P<{param_name}>[^/]+)')
                param_names.append(param_name)
                wildcard_index += 1
            elif part == '#':
                regex_parts.append(r'(?P<w0>.*)')
                param_names.append('w0')
            else:
                regex_parts.append(re.escape(part))

        regex = re.compile('^' + '/'.join(regex_parts) + '$')

        def decorator(func: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
            self._handlers.append(
                MqttHandler(
                    topic_pattern=topic,
                    regex=regex,
                    func=func,
                    param_names=param_names,
                )
            )
            return func

        return decorator

    def get_topics(self) -> list[str]:
        """获取所有已注册的 topic 模式"""
        return [h.topic_pattern for h in self._handlers]

    async def dispatch(self, message: aiomqtt.Message) -> None:
        """
        将收到的 MQTT 消息分发到匹配的处理器

        :param message: aiomqtt 消息对象
        :return:
        """
        topic = str(message.topic)
        payload_str = message.payload.decode('utf-8') if isinstance(message.payload, bytes) else str(message.payload)

        for handler in self._handlers:
            match = handler.regex.match(topic)
            if match:
                kwargs: dict[str, Any] = {
                    'topic': topic,
                    'payload': payload_str,
                }
                kwargs.update(match.groupdict())
                try:
                    await handler.func(**kwargs)
                except Exception as e:
                    log.exception(f'[MQTT] 消息处理器执行失败 [{topic}]: {e}')
                return

        log.warning(f'[MQTT] 未找到匹配的消息处理器: {topic}')


# 全局单例
mqtt_handler_registry = MqttHandlerRegistry()
