#!/usr/bin/env python
# coding: utf-8

import os
import email
import smtplib
import mimetypes

from io import BytesIO

from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class EmailAgent:
    def __init__(self, name, user, passwd):
        self.name = name
        self.user = user
        self.passwd = passwd
        self.to_list = []
        self.cc_list = []

    def _decode_(sefl,s):
        if type(s) is str:
            return s
        else:
            return s.decode(chardet.detect(s)['encoding'])

    def send(self,email_info):
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
        # server = smtplib.SMTP_SSL("smtp.163.com")
        server.login(self.user, self.passwd)
        server.sendmail("<%s>" % self.user,self.to_list + self.cc_list, email_info.as_string())
        server.close()

    def build_email_to_send(self, subject, content):
        attach = MIMEMultipart()
        if isinstance(content, str) or (type(content) is str):
            txt = MIMEText(self._decode_(content).encode('utf-8'),_charset='utf-8')
            attach.attach(txt)
        else:
            attach.attach(content)
        attach["Subject"] = self._decode_(subject)
        if self.user is not None:
            attach["From"] = "%s<%s>" % (self.name, self.user)
        if self.to_list:
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            attach["Cc"] = ";".join(self.cc_list)
        return attach
    
    def add_html_attch(self,attach,html):
        context = MIMEText(html,_subtype='html',_charset='utf-8')
        attach.attach(context)
        return attach

    def get_attachment(self, file_path):
        data = open(file_path, 'rb')
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        email.encoders.encode_base64(file_msg)
        file_msg.add_header(
            'Content-Disposition',
            'attachment', 
            filename=('gbk', '', file_path))
        return file_msg
    
    def add_image_attach(self,attach,img,tag):
        if isinstance(img, str) or (type(img) is str):
            with open(img,'rb') as fp:
                msgImage = MIMEImage(fp.read())
        else:
            memf = BytesIO()
            img.save(memf, "JPEG")
            msgImage = MIMEImage(memf.getvalue())
        msgImage.add_header('Content-ID','<%s>'%tag)
        attach.attach(msgImage)

    def add_net_report(self,attach,name,report,product):
        self.add_image_attach(attach,'images/image002.png','logo')
        self.add_image_attach(attach,'images/image004.png','qrcode')
        self.add_image_attach(attach,report,'net_report')
        with open('resource/mail_template.html') as fp:
            html = fp.read().format(name=name,logo="cid:logo",
                qrcode="cid:qrcode",net_report="cid:net_report",product=product)
        context = MIMEText(html,_subtype='html',_charset='utf-8')
        attach.attach(context)
        return attach