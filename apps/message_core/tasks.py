import json
import string
import random

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.conf import settings

import requests

from apps.message_core.views import EmailThread, Sms

def send_push_message(to, title, body, data={}):
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'https://exp.host/--/api/v2/push/send'
    payload = {'to': to, 'title': title,'body': body, 'data': data}
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return json.loads(res.content.decode('utf-8'))


def generate_number(size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_sms_confirmation(celphone, code):
    data =   {
        "sendSmsRequest": {
            "from": settings.SMS_FROM,
            "to": "55%s" % (celphone.translate(str.maketrans('','',"()- "))),
            "msg": "Seu código de confirmação é %s" % (code),
            "callbackOption": "NONE",
            "aggregateId": "1111"
        }
    }
    return data
