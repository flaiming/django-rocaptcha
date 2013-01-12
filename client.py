import urllib
import urllib2
import sys

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils import translation
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import STATUS_CODE_TEXT

DEFAULT_API_SERVER = "rocaptcha.com"
DEFAULT_VERIFY_SERVER = "rocaptcha.com"
DEFAULT_WIDGET_TEMPLATE = 'rocaptcha/widget.html'

API_SERVER = getattr(settings, "ROCAPTCHA_API_SERVER", DEFAULT_API_SERVER)
VERIFY_SERVER = getattr(settings, "ROCAPTCHA_VERIFY_SERVER", \
        DEFAULT_VERIFY_SERVER)
WIDGET_TEMPLATE = getattr(settings, "ROCAPTCHA_WIDGET_TEMPLATE", \
        DEFAULT_WIDGET_TEMPLATE)


ROCAPTCHA_SUPPORTED_LANUAGES = ('cs', 'en')

class Status:
    #statuses
    OK = "OK"
    ERROR = "ERROR"
    PASSED = "PASSED"
    FAILED = "FAILED"
    BAD_PUBLIC_KEY = "BAD_PUBLIC_KEY"
    BAD_PRIVATE_KEY = "BAD_PRIVATE_KEY"
    TIMEOUT = "TIMEOUT"


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def displayhtml(public_key,
    attrs,
    error=None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""
    #import pdb; pdb.set_trace()
    params = ''
    if error:
        params = '&error=%s' % error
        
    #set language param
    params += '&lang=%s' % translation.get_language()

    server = API_SERVER

    if not 'lang' in attrs:
        attrs['lang'] = settings.LANGUAGE_CODE[:2]

    return render_to_string(WIDGET_TEMPLATE,
            {'api_server': server,
             'public_key': public_key,
             'params': params,
             'options': mark_safe(json.dumps(attrs, indent=2))
             })


def submit(hash,
    angle,
    private_key,
    remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    hash -- The value of hash from the form
    angle -- The value of angle from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (angle and hash and
            len(angle) and len(hash)):
        return RecaptchaResponse(
            is_valid=False,
            error_code='incorrect-captcha-sol'
        )

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
            'key': private_key,
            #'remoteip':  encode_if_necessary(remoteip),
            #'challenge':  encode_if_necessary(hash),
            #'response':  encode_if_necessary(angle),
            })
    
    verify_url = 'http://%s/api/verify/%s/%s/' % (VERIFY_SERVER, encode_if_necessary(hash), encode_if_necessary(angle))

    try:
        request = urllib2.Request(
            url=verify_url,
            data=params,
    #        headers={
    #            "Content-type": "application/x-www-form-urlencoded",
    #            "User-agent": "RoCAPTCHA Python"
    #            }
            )
    
        httpresp = urllib2.urlopen(request)
    
        return_values = json.load(httpresp)
        httpresp.close()
    except Exception:
        return_values = False
    
    #check if json wos successfull
    if (return_values == False):
        return RecaptchaResponse(is_valid=False, error_code=u"Cannot decipher server return value. Sorry.")

    return_code = return_values['status']

    if (return_code == Status.PASSED):
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code=return_code)
