from django import forms
from django.utils.safestring import mark_safe

from rocaptcha import client


class RoCaptcha(forms.widgets.Widget):
    rocaptcha_challenge_name = 'rocaptcha_challenge_field'
    rocaptcha_response_name = 'rocaptcha_response_field'
    rocaptcha_session_id = 'rocaptcha_session_id'

    def __init__(self, public_key, *args, **kwargs):
        self.public_key = public_key
        super(RoCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % client.displayhtml(self.public_key))

    def value_from_datadict(self, data, files, name):
        return {'hash': data.get(self.rocaptcha_challenge_name, None),
            'angle': data.get(self.rocaptcha_response_name, None),
            'session_id': data.get(self.rocaptcha_session_id, None)}
