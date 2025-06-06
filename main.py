import base64
import json
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.event.filter import (
    command,
    regex,
    llm_tool,
    permission_type,
    PermissionType,
    event_message_type,
    EventMessageType,
)
import astrbot.api.message_components as Comp


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @event_message_type(EventMessageType.ALL)
    async def helloworld(self, event: AstrMessageEvent):
        if event.get_platform_name() == "aiocqhttp":
            files = []
            for msg in event.message_obj.message:
                if isinstance(msg, Comp.Image):
                    files.append(msg.file)

            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            for file in files:
                payloads = {
                    "file_id": file
                }
                ret = await client.api.call_action('get_image', **payloads) # 调用 协议端  API
                logger.info(f"ret: {ret}")


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
