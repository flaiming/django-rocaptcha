import sys
from client import Status

from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode

from rocaptcha import client
from rocaptcha.widgets import RoCaptcha


class RoCaptchaField(forms.CharField):

    def __init__(self, public_key=None, private_key=None, *args, **kwargs):
        public_key = public_key if public_key else settings.ROCAPTCHA_PUBLIC_KEY
        self.private_key = private_key if private_key else settings.ROCAPTCHA_PRIVATE_KEY

        self.widget = RoCaptcha(public_key=public_key)
        self.required = False
        
        super(RoCaptchaField, self).__init__(*args, **kwargs)
        self.label = "RoCAPTCHA"

    def get_remote_ip(self):
        f = sys._getframe()
        while f:
            if 'request' in f.f_locals:
                request = f.f_locals['request']
                if request:
                    remote_ip = request.META.get('REMOTE_ADDR', '')
                    forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
                    ip = remote_ip if not forwarded_ip else forwarded_ip
                    return ip
            f = f.f_back

    def clean(self, values):
        hash = smart_unicode(values['hash'])
        angle = smart_unicode(values['angle'])

        check_captcha = client.submit(hash, \
                angle, private_key=self.private_key, \
                remoteip=self.get_remote_ip())
        if not check_captcha.is_valid:
            msg = Status.get_message(check_captcha.error_code)
            raise forms.util.ValidationError(msg)
        return hash
