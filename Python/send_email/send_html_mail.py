import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from email.header import Header

import account

msg = EmailMessage()
msg['Subject'] = "¡™£¢∞§¶•ªºœ∑´®†¥¨ˆøπ“æ÷≥¬˚µ∆˜˙∫©∫©∫ƒ√∂"
msg['From'] = Address(Header("神明大人", 'utf-8').encode(), "550413470", "qq.com")
msg['to'] = (Address(Header("愚蠢的人类", 'utf-8').encode(), "244143261", "qq.com"),
             Address(Header("神明大人", 'utf-8').encode(), "zhongzegeng.scut", "qq.com"))

msg.set_content("""\
Salut!

Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
""")

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.
asparagus_cid = make_msgid()
msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cela 
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a> déjeuner.
    </p>
    <img src="cid:{asparagus_cid}" />
  </body>
</html>
""".format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')


with open("pic/pic2.jpg", 'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg', cid=asparagus_cid)

with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))

with smtplib.SMTP('smtp.qq.com', '587') as s:
    s.starttls()
    s.login(account.smtp_user, account.smtp_pwd)
    s.send_message(msg)

