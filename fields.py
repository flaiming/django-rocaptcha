import os
import sys
from client import Status

from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from rocaptcha import client
from rocaptcha.widgets import RoCaptcha


class RoCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Incorrect, please try again.'),
        'captcha_private_key_invalid': _(u'Bad private key!')
    }

    def __init__(self, public_key=None, private_key=None, attrs={}, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed ot the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://code.google.com/apis/recaptcha/docs/customization.html
        """
        public_key = public_key if public_key else settings.\
                RECAPTCHA_PUBLIC_KEY
        self.private_key = private_key if private_key else \
                settings.RECAPTCHA_PRIVATE_KEY

        self.widget = RoCaptcha(public_key=public_key, attrs=attrs)
        self.required = False
        super(RoCaptchaField, self).__init__(*args, **kwargs)

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

#        if os.environ.get('RECAPTCHA_TESTING', None) == 'True' and \
#                angle == 'PASSED':
#            return values[0]

        check_captcha = client.submit(hash, \
                angle, private_key=self.private_key, \
                remoteip=self.get_remote_ip())
        if not check_captcha.is_valid:
            if check_captcha.error_code == Status.BAD_PRIVATE_KEY:
                msg = self.error_messages['captcha_private_key_invalid']
            else:
                msg = self.error_messages['captcha_invalid']
            raise forms.util.ValidationError(msg)
        return hash
