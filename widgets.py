from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from rocaptcha import client


class RoCaptcha(forms.widgets.Widget):
    rocaptcha_challenge_name = 'rocaptcha_challenge_field'
    rocaptcha_response_name = 'rocaptcha_response_field'

    def __init__(self, public_key=None, attrs={}, *args, \
            **kwargs):
        self.public_key = public_key if public_key else \
                settings.ROCAPTCHA_KEY
        self.js_attrs = attrs
        super(RoCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % client.displayhtml(self.public_key, self.js_attrs))

    def value_from_datadict(self, data, files, name):
        return {'hash': data.get(self.rocaptcha_challenge_name, None),
            'angle': data.get(self.rocaptcha_response_name, None)}
