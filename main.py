from ast import alias
import base64
import json
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.event import CommandResult, MessageChain
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
from astrbot.core.star.filter.command import GreedyStr
from typing import Optional


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("view_plugins")
    async def view_plugins(self, event: AstrMessageEvent):
        plugins = self.context.get_all_stars()
        yield event.plain_result(f"plugins: {plugins}")

    @filter.command("po")
    async def po(
        self,
        event: AstrMessageEvent,
        content: Optional[str] = "",
        options: GreedyStr = GreedyStr,
    ):
        is_content = True if content else False
        yield event.plain_result(
            f"is_content: {is_content}, content: {content}, options: {options}"
        )

    @filter.command("pic")
    async def pic(self, event: AstrMessageEvent):
        if event.get_platform_name() == "aiocqhttp":
            url = "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhS_yFjBzSh-GLln7UhJe02xCPn8yBj8lhcg_woorMGLiqfZjQMyBHByb2RQgL2jAVoQbNgkRYZ-s6-iuP1AG_ybv3oChA0"
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
                AiocqhttpMessageEvent,
            )

            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot  # 得到 client
            rkeys = await client.api.call_action("get_rkey")

            rkey_data = next((rkey for rkey in rkeys if rkey["type"] == "group"), None)
            rkey = rkey_data["rkey"]

            pic_url = url + rkey
            logger.info(f"pic_url: {pic_url}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
