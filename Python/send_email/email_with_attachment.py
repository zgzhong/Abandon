import os
import smtplib
from email.message import EmailMessage

# imghdr用来判断图片的格式
import imghdr

import account

msg = EmailMessage()

msg['Subject'] = 'Pictures Experiment'
msg['From'] = 'zhongzegeng.scut@qq.com'
msg['To'] = '550413470@qq.com'
msg.preamble = 'what\'s this?'

# 添加附件到邮箱中
for file in os.listdir('pic'):
    with open('pic/{}'.format(file), 'rb') as fp:
        img_data = fp.read()
    msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data))

with smtplib.SMTP('smtp.qq.com', 587) as s:
    s.starttls()
    s.login(account.smtp_user, account.smtp_pwd)
    s.set_debuglevel(1)
    s.send_message(msg)

