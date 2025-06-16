import os
from datetime import datetime
from src.notification.sender_email import EmailSender


def test_preview_email():
    EmailSender.preview_email(web_open=False)
    # 检查 previews 目录下是否生成了 html 文件
    preview_dir = "previews"
    check_date = datetime.now()
    preview_file = f"{preview_dir}/preview_测试用户_{check_date.strftime('%Y%m%d')}.html"
    assert os.path.exists(preview_file)
    content = open(preview_file, "r", encoding="utf-8").read()
    assert "测试用户" in content
    assert "今天是您的" in content
    assert "生日快乐" in content
