from src.notification.notification_base import NotificationBase
from src.core.checker import Recipient
from typing import Dict
import httpx
import logging

logger = logging.getLogger(__name__)


class ServerChanSender(NotificationBase):
    def __init__(self, sckey: str):
        self.sckey = sckey

    def render_content(self, name: str, template_file: str, extra_info: Dict) -> str:
        # 只渲染纯文本内容
        lines = [f"亲爱的{name}："]
        if extra_info.get("days_until", 0) == 0:
            if extra_info.get("solar_match") and extra_info.get("lunar_match"):
                lines.append("今天是您的阳历和农历生日，祝您生日快乐！🎉")
            elif extra_info.get("solar_match"):
                lines.append("今天是您的阳历生日，祝您生日快乐！🎉")
            else:
                lines.append("今天是您的农历生日，祝您生日快乐！🎉")
        else:
            if extra_info.get("solar_match") and extra_info.get("lunar_match"):
                lines.append(f"{extra_info['days_until']}天后是您的阳历和农历生日！")
            elif extra_info.get("solar_match"):
                lines.append(f"{extra_info['days_until']}天后是您的阳历生日！")
            else:
                lines.append(f"{extra_info['days_until']}天后是您的农历生日！")
        # 追加命理和节日信息
        lines.append(f"生肖：{extra_info.get('zodiac', '')}")
        lines.append(f"星座：{extra_info.get('constellation', '')}")
        if extra_info.get("solar_term"):
            lines.append(f"节气：{extra_info['solar_term']}")
        if extra_info.get("lunar_festival"):
            lines.append(f"农历节日：{extra_info['lunar_festival']}")
        if extra_info.get("solar_festival"):
            lines.append(f"阳历节日：{extra_info['solar_festival']}")
        return "\n".join(lines)

    async def send(self, recipient: Recipient, content: str, days_until: int, age: int):
        # Server酱推送API
        url = f"https://sctapi.ftqq.com/{self.sckey}.send"
        title = f"生日提醒- {recipient.name} - {age}岁 - {days_until}天后"
        data = {"title": title, "desp": content}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            if resp.status_code == 200 and resp.json().get("code") == 0:
                logger.info(f"Server酱推送成功: {recipient.name}")
            else:
                logger.error(f"Server酱推送失败: {recipient.name}, 响应: {resp.text}")
                raise Exception(f"Server酱推送失败: {resp.text}")
