SNS Custom Email CGI
===================

**No longer maintained** - I no longer use this (but it's still somewhat interesting)

## What

This is a CGI (common gateway interface) script (to be run by a webserver) that works as an HTTP
endpoint for AWS (Amazon web services) SNS (simple notification service), and sends a minimalistic
email with each notification (or subscription confirmation).

## Why

I was motivated to make this script because I switched to a cheap cell service provider and then
discovered that it didn't receive texts from short-code numbers, which Amazon SNS uses to send
notifications. Amazon SNS can also send emails, so I had it send them to the free email -> sns
gateway that would text my number. The subscription emails use anchor tags for the subscription
confirmation link, and the gateway strips the actual link when turning it into a plain-text
text, so I can't confirm. I can instead send them to my actual email address, and have gmail
forward them to the gateway, and confirm by accessing the link in gmail... but both that process
and the notification email contents were extensive and ugly.

So, I created this silly script that receives Amazon SNS http-type notifications, and sends a
more minimal email (in my case, to the gateway) and inserts the subscription confirmation link
as plain text. As a bonus, I can tweak the message however I like (and the gateway sends the
emails as MMS, which don't have the 160-character limit!).

## How

First, you need a webhost that runs python cgi scripts. Then, to use this script without too much
enhancement, you need that webhost to offer smtp service to send emails locally without any
credentials. This is actually common for old-style unix hosting, to have an smtp server listening
on localhost (from a bash script you could use "mail" or "sendmail" to use it to send email).

Just edit the handful of configuration variables at the top of sns_custom_email.cgi, put the
file on your webhost, and make sure it's executable and any `.htaccess` or similar configuration
files are edited as necessary to make it run as cgi. Configure an SNS "http" endpoint of
`http://example-host.com/example-path/sns_custom_email.cgi`. Test it by using curl to make some
requests to it, and use your webhost's error log to troubleshoot. Example curl usage:

```
curl -v -H "Content-Type: text/plain; charset=UTF-8" --data-binary \
'{"Type": "Notification", "TopicArn": "arn:aws:sns:us-east-1:123456789012:MyTopic", "Subject": "test", "Message": "test message"}' \
http://example-host.com/example-path/sns_custom_email.cgi
```

You can find more complete example messages in the [AWS SNS HTTP Endpoint Docs](http://docs.aws.amazon.com/sns/latest/dg/SendMessageToHttp.html).

I use NearlyFreeSpeech.net, which has python 2.6. This script may not work with python 3.x, but I
welcome pull requests to fix that (or reports that it does work).

NearlyFreeSpeech.net offers unauthenticated smtp service at "sitemail.nearlyfreespeech.net",
only to the web server user (so you can't test it from a shell over ssh), so that's what I
set my "smtp_host" to.
