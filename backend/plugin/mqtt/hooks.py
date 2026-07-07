from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.common.log import log

# 在模块导入时加载所有 MQTT 消息处理器
# 必须在 connect_and_listen 之前确保所有 @mqtt_handler_registry.register() 装饰器已执行
from backend.plugin.mqtt.mqtt import handlers  # noqa: F401
from backend.plugin.mqtt.mqtt.client import mqtt_client_manager


def setup(app: FastAPI) -> None:
    """插件 setup hook — 在应用注册阶段执行，用于确认插件已加载"""
    log.info('[MQTT Plugin] 插件已加载，准备注册 lifespan hook')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    MQTT 插件 lifespan hook

    :param app: FastAPI 应用实例
    :return:
    """
    # 启动 MQTT 客户端（后台 asyncio Task）
    mqtt_client_manager.start_listener()
    log.info('[MQTT Plugin] MQTT 客户端监听器已启动')

    try:
        yield
    finally:
        # 停止 MQTT 客户端
        await mqtt_client_manager.stop_listener()
        log.info('[MQTT Plugin] MQTT 客户端监听器已停止')
