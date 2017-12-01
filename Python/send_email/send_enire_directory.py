import os
import smtplib

# 根据文件的扩展名猜测文件的MIME类型
import mimetypes

# 构造命令行选项
from argparse import ArgumentParser

from email.message import EmailMessage
from email.header import Header
from email.policy import SMTP

import account


def main():
    parser = ArgumentParser(description="""\
将文件夹中的内容作为MIME信息发送出去。
除非指定 -o 选项。否则，邮件将会被递送到本机的SMTP服务器。
消息将作为邮件被递送出去，当然你的本机必须运行SMTP服务。
""")

    parser.add_argument('-d', '--directory',
                        help="""指定要发送的文件夹, 将使用当前文件夹。
                        文件夹中只有常规文件会被发送出去。不会递归地发送子目录
                        """)
    parser.add_argument('-o', '--output',
                        metavar='FILE',
                        help="""将构建的消息(message) 写到FILE中
                        而不是递送到smtp服务器去。
                        """)
    parser.add_argument('-s', '--sender', required=True,
                        help='The value of the From: header(required)')
    parser.add_argument('-r', '--recipient', required=True,
                        action='append', metavar='RECIPIENT',
                        default=[], dest='recipients',
                        help='A To: header value (at least one required)')
    args = parser.parse_args()
    directory = args.directory
    if not directory:
        directory = '.'
    
    # 构建email消息
    msg = EmailMessage()
    msg['Subject'] = "文件夹中 {} 的内容".format(os.path.abspath(directory))
    msg['To'] = ', '.join(args.recipients)
    msg['From'] = args.sender
    msg.preamble = 'You won\'t see this sentence in message'
    # 如果要使用中文，要用Header编码
    # msg.preamble = Header('你不会在正文中看到这段字的', 'utf-8').encode()
    
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue    # 忽略非文件项
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
    
    if args.output:
        with open(args.output, 'wb') as fp:
            fp.write(msg.as_bytes(policy=SMTP))
    else:
        with smtplib.SMTP('smtp.qq.com', 587) as s:
            s.starttls()
            s.login(account.smtp_user, account.smtp_pwd)
            s.set_debuglevel(1)
            s.send_message(msg)

if __name__ == '__main__':
    main()
