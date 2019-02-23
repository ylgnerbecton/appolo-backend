from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import threading
import requests
import json


'''
	EMAIL THREAD
'''
class EmailThread(threading.Thread):
    def __init__(
            self, subject, body, from_email=None, to_email=None, 
            html=None, fail_silently=False, bcc=None, cc=None, reply_to=None,
            connection=None, attachments=None, headers=None, alternatives=None,
            images=None, files=None
        ):

        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to_email = to_email
        self.html = html
        self.fail_silently = fail_silently
        self.bcc = bcc
        self.connection = connection
        self.attachments = attachments
        self.headers = headers
        self.alternatives = alternatives
        self.cc = cc
        self.reply_to = reply_to
        self.images = images
        self.files = files
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.to_email, 
            self.bcc, self.connection, self.attachments, self.headers, 
            self.alternatives, self.cc, self.reply_to
        )
        
        if self.html:
            msg.attach_alternative(self.html, "text/html")

        for image in self.images:
            msg.attach(image)

        for pdf in self.files:
            msg.attach('recibo-doeja', pdf, 'application/pdf')

        msg.send(self.fail_silently)

# '''
# SMS
# '''
# class Sms(object):

#     def __init__(self, token=settings.SMS_TOKEN):
#         self.token = token 
#         # Gerar token no linux echo -n conta:senha | base64

#     def headers(self):
#         return {
#             'Content-Type': 'application/json',
#             'Authorization': 'Basic %s' % self.token,
#             'Accept': 'application/json'
#         }

#     def send(self, data={}):
#         try:
#             url = 'https://api-rest.zenvia360.com.br/services/send-sms'
#             response = requests.post(url, headers=self.headers(),data=json.dumps(data))
#             if 'Error' in response.text:
#                 raise ValueError('SMS REQUEST ERROR')
#             return True
#         except ValueError as e:
#             url = "https://api-messaging.movile.com/v1/send-sms"
#             payload = "{\"destination\": \"%s\" ,  \"messageText\": \"%s %s\"}" % (data['sendSmsRequest']['to'], data['sendSmsRequest']['from'], data['sendSmsRequest']['msg'])
            
#             headers = {
#                 'username': 'BIURI MARKETPLACE LTDA', 
#                 'authenticationtoken': self.token, 
#                 'content-type': "application/json"
#             }

#             response = requests.post(url, data=payload, headers=headers)
#             if 'errorCode' in response.text:
#                 return False
#             return True


'''
SMS
'''
class Sms(object):

    def __init__(self, token=settings.SMS_TOKEN):
        self.token = token 
        # Gerar token no linux echo -n conta:senha | base64

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' %self.token,
            'Accept': 'application/json'
        }


    def send(self, data={}):
        try:
            url = 'https://api-rest.zenvia360.com.br/services/send-sms'
            response = requests.post(url, headers=self.headers(),data=json.dumps(data))
            if 'Error' in response.text:
                raise ValueError('sms is False')
            return True
        except ValueError as e:
            url = "https://api-messaging.movile.com/v1/send-sms"
            payload = "{\"destination\": \"%s\" ,  \"messageText\": \"%s %s\"}" % (data['sendSmsRequest']['to'], data['sendSmsRequest']['from'], data['sendSmsRequest']['msg'])
            headers = {
                'username': "HIPRO INOVACAO LTDA - EPP",
                'authenticationtoken': "u8wtifbzk4mHXkMAfHYkWeLXWsnyKSdpK_ZUkswt",
                'content-type': "application/json"
                }

            response = requests.post(url, data=payload, headers=headers)
            print(response)
            if 'errorCode' in response.text:
                return False
            return True


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(to, title, body):
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'https://exp.host/--/api/v2/push/send'
    payload = {'to': "ExponentPushToken[%s]" %(to), 'title': title,'body': body}
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return json.loads(res.content.decode('utf-8'))