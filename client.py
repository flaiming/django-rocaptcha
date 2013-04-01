import urllib
import urllib2

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

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
    WRONG_RESPONSE = "WRONG_RESPONSE"
    WRONG_HASH = "WRONG_HASH"
    
    MESSAGES = {
        FAILED: _(u'Image was not positioned upright, please try again.'),
        BAD_PRIVATE_KEY: _(u'You have submitted bad private key.'),
        TIMEOUT: _(u'Timeout for solving test has passed. Please try again.'),
        WRONG_RESPONSE: _(u'Response value is not present or is in wrong format.'),
        WRONG_HASH: _(u'You have submitted bad image hash code.'),
        ERROR: _(u'Unknown error, please try again later.'),
    }
    
    @classmethod
    def get_message(cls, status):
        try:
            return cls.MESSAGES[status]
        except:
            return cls.MESSAGES[cls.ERROR]


class RoCaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml(public_key):
    """Gets the HTML to display for RoCATPCHA
    
    public_key -- The public api key"""
    params = ''
    #sets language code
    params += '&lang=%s' % translation.get_language()

    return render_to_string(WIDGET_TEMPLATE,
            {'api_server': API_SERVER,
             'public_key': public_key,
             'params': params
             })


def submit(hash,
    angle,
    private_key,
    remoteip):
    """
    Submits a RoCATPCHA request for verification. Returns RoCaptchaResponse
    for the request.

    hash -- The value of hash from the form
    angle -- The value of angle from the form
    private_key -- your RoCATPCHA private key
    remoteip -- the user's ip address
    """

    if not (hash and len(hash)):
        return RoCaptchaResponse(
            is_valid=False,
            error_code=Status.WRONG_HASH
        )
    
    if not (angle and len(angle)):
        return RoCaptchaResponse(
            is_valid=False,
            error_code=Status.WRONG_RESPONSE
        )

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
            'key': encode_if_necessary(private_key),
            'hash': encode_if_necessary(hash),
            'remoteip':  encode_if_necessary(remoteip),
            'response':  encode_if_necessary(angle),
            })
    
    verify_url = 'http://%s/api/verify/' % VERIFY_SERVER
    
    try:
        request = urllib2.Request(
            url=verify_url,
            data=params,
            headers={
                "Content-type": "application/x-www-form-urlencoded",
                "User-agent": "RoCAPTCHA Python"
                }
            )
        httpresp = urllib2.urlopen(request)
        return_values = json.load(httpresp)
        httpresp.close()
    except Exception as e:
        return_values = False
    
    #check if request was successfull
    if (return_values == False):
        return RoCaptchaResponse(is_valid=False, error_code=Status.ERROR)

    #get status value
    return_code = return_values['status']

    if (return_code == Status.PASSED):
        return RoCaptchaResponse(is_valid=True)
    else:
        return RoCaptchaResponse(is_valid=False, error_code=return_code)
