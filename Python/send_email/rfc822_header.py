"""
email 模块可以解析rfc822标准规定的邮件头
"""

from email.parser import BytesParser, Parser
from email.policy import default


# 如果邮件头在文件中，使用下面的代码
# with open(messagefile, 'rb') as fp:
#     headers = BytesParser(policy=default).parse(fp)


# 为了简单，使用字符串来解析
headers = Parser(policy=default).parsestr(
          'From: Foo Bar <user@example.com>\n'
          'To: <Someone_else@example.com>\n'
          'Subject: Test message\n'
          '\n'
          'Body would go here\n')


# Now the header items can be accessed as dictionary:
print('To: {}'.format(headers['to']))
print('From: {}'.format(headers['from']))
print('Subject: {}'.format(headers['subject']))


print('Recipient username: {}'.format(headers['to'].addresses[0].username))
print('Sender name: {}'.format(headers['from'].addresses[0].display_name))
