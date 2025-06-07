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
from astrbot.core.star.filter.command import GreedyStr

@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    # @event_message_type(EventMessageType.ALL)
    # async def helloworld(self, event: AstrMessageEvent):
    #     logger.info("helloworld")
    @filter.command("greed0")
    async def greed0(self, event: AstrMessageEvent, pre: str, content: GreedyStr):
        ret = f"greed0: pre: {pre}, content: {content}"
        yield event.plain_result(ret)
    
    @filter.command("space greed")
    async def space_greed(self, event: AstrMessageEvent, pre: str, content: GreedyStr):
        ret = f"space_greed: pre: {pre}, content: {content}"
        yield event.plain_result(ret)

    @filter.command_group("greed_group")
    def greed_group(self):
        pass

    @greed_group.command("greed1")
    async def greed1(self, event: AstrMessageEvent, pre: str, content: GreedyStr):
        ret = f"greed1: pre: {pre}, content: {content}"
        yield event.plain_result(ret)
    
    @filter.command_group("space greed group")
    async def space_greed_group(self):
        pass
    
    @space_greed_group.command("space greed1")
    async def space_greed1(self, event: AstrMessageEvent, pre: str, content: GreedyStr):
        ret = f"space greed1: pre: {pre}, content: {content}"
        yield event.plain_result(ret)
    
    @space_greed_group.command("space_greed2")
    async def space_greed2(self, event: AstrMessageEvent, pre: str, content: GreedyStr):
        ret = f"space greed2: pre: {pre}, content: {content}"
        yield event.plain_result(ret)



    @filter.command("pic")
    async def pic(self, event: AstrMessageEvent):
        if event.get_platform_name() == "aiocqhttp":
            url = "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhS_yFjBzSh-GLln7UhJe02xCPn8yBj8lhcg_woorMGLiqfZjQMyBHByb2RQgL2jAVoQbNgkRYZ-s6-iuP1AG_ybv3oChA0"
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            rkeys = await client.api.call_action('get_rkey')
            
            rkey_data = next((rkey for rkey in rkeys if rkey['type'] == 'group'), None)
            rkey = rkey_data['rkey']
            
            pic_url = url+rkey
            logger.info(f"pic_url: {pic_url}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
