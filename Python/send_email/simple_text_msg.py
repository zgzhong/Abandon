"""
根据官方文档的一个简单的发送邮件脚本
https://docs.python.org/3/library/email.examples.html
"""

import smtplib
import account
from email.message import EmailMessage

# 读取信件内容
letter_file = "letter.txt"
with open(letter_file) as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

msg["Subject"] = "Helle me!"
msg["From"] = "550413470@qq.com"
msg["To"] = "zhongzegeng.scut@qq.com"

# 如果使用Docker运行postfix
# 连接代码如下
# s = smtplib.SMTP("127.0.0.1", 25)
# s.login("solink", "solink")

# smtp 服务器使用QQ的服务,
# QQ 的smtp服务使用tls， 端口为587.
s = smtplib.SMTP("smtp.qq.com", 587)
s.starttls()

# 登陆smtp服务器
# account模块存着QQ邮箱的账号和授权码
s.login(account.smtp_user, account.smtp_pwd)

# 输出发送邮件的debug信息
s.set_debuglevel(1)
s.send_message(msg)
s.quit()
