'''
send email module
'''

import os
import time
import random
import smtplib
from time import strftime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((\
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def SendSSLEmail(file_path, object_id):
    mailto_list = ["", ""]
    from_addr = ""
    pwd = ''
    smtp_server = ""
    to_list = mailto_list
    msg = MIMEMultipart()
    msg['From'] = from_addr
    # msg['To'] = _format_addr(u'doggy <%s>' % to_addr)
    msg['To'] = ";".join(to_list)
    title = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()) + '-ai_anomaly_detection'
    msg['Subject'] = Header(title, 'utf-8').encode()
    Text_msg = title + ' ' +'the testing state of instrument SyncEdge is abnormal!!!!!!!!!!!!!!'
    msg.attach(MIMEText(Text_msg, 'html', 'utf-8'))

    with open(file_path, 'rb') as f:
        img_name = object_id + '.jpg'
        mime = MIMEBase('image', 'jpg', filename = img_name)
        mime.add_header('Content-Disposition', 'attachment', filename = object_id)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)
    
    server = smtplib.SMTP_SSL(smtp_server)
    server.set_debuglevel(1)
    server.login(from_addr, pwd)
    server.sendmail(from_addr, to_list, msg.as_string())
    server.quit()

if __name__ == '__main__':
    mailto_list = ["", ""]
    file_path = '../model/a.jpg'
    object_id = 'a'
    # mailto_list = ["5645297@qq.com","490171@qq.com","4257399@qq.com","11356346@qq.com"]
    SendSSLEmail(file_path, object_id)
