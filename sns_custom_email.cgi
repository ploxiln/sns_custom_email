#!/usr/bin/env python

#### CONFIGURATION ####

src_email = 'alert@myhost.example'
dst_email = 'myuser@myemail.example'
smtp_host = 'localhost'
smtp_port = 587

#######################

import sys
import json
import smtplib
from email.mime.text import MIMEText

# lazy, only do HTTP 200 responses
print("Content-Type: text/plain")
print("")     # end of headers

def panic(text, msgdict):
    fulltext = "%s (%r)" % (text, msgdict)
    print(fulltext)
    sys.stderr.write(fulltext)
    sys.exit(1)

postdata = sys.stdin.read()
try:
    msg = json.loads(postdata)
except Exception:
    panic("Failed to decode post data as json", postdata[:500])

msg_subject = ""
msg_body = ""

if 'Type' not in msg:
    panic("Type not in msg", msg)

if msg['Type'] == "SubscriptionConfirmation":
    if 'TopicArn' in msg and 'SubscribeURL' in msg:
        msg_subject = "Subscribe"
        msg_topic = msg['TopicArn'].split(':')[-2]
        msg_body = "to %s:\n\n%s" % (msg_topic, msg['SubscribeURL'])
    else:
        panic("SubscriptionConfirmation lacking TopicArn or SubscribeURL", msg)

elif msg['Type'] == "Notification":
    if 'Message' in msg:
        msg_subject = 'Alert'
        if 'Subject' in msg:
            msg_subject = msg['Subject']
        elif 'TopicArn' in msg:
            msg_subject = msg['TopicArn'].split(':')[-1]
        msg_body = msg['Message'].decode('string_escape')
    else:
        panic("Notification lacking Subject or Message", msg)

else:
    panic("unrecognized message Type", msg)

emailmsg = MIMEText(msg_body)
emailmsg['Subject'] = msg_subject
emailmsg['From'] = src_email
emailmsg['To'] = dst_email

try:
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.sendmail(src_email, [dst_email], emailmsg.as_string())
except Exception as exc:
    panic("failed to send email", exc)

print("Notification received and sent OK")
sys.exit(0)
