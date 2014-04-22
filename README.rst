Django RoCAPTCHA
================
**Django form widget for RoCAPTCHA test.**

.. contents:: Contents
    :depth: 5

`RoCAPTCHA web site <http://rocaptcha.com>`_

Installation
------------

#. Run ``python setup.py install`` to install rocaptcha module.

#. Add ``rocaptcha`` to your ``INSTALLED_APPS`` setting.

#. Add a ``ROCAPTCHA_PUBLIC_KEY`` setting to the project's ``settings.py`` file. This is your public API key as provided by RoCAPTCHA, i.e.::
    
    ROCAPTCHA_PUBLIC_KEY = '49c47baecc3738a36bb99665e290fc'
    
   This can be seperately specified at runtime by passing a ``public_key`` parameter when constructing the ``RoCaptchaField``, see field usage below.

#. Add a ``ROCAPTCHA_PRIVATE_KEY`` setting to the project's ``settings.py`` file. This is your private API key as provided by RoCAPTCHA, i.e.::
    
    ROCAPTCHA_PRIVATE_KEY = 'e5b725f71537ec50ceee5c6a9b27d6'
   
   This can be seperately specified at runtime by passing a ``private_key`` parameter when constructing the ``RoCaptchaField``, see field usage below.

Usage
-----

Field
~~~~~
The quickest way to add RoCAPTCHA to a form is to use the included ``RoCaptchaField`` field type. A ``RoCaptcha`` widget will be rendered with the field validating itself without any further action required from you. For example::

    from django import forms
    from rocaptcha.fields import RoCaptchaField

    class FormWithRoCaptcha(forms.Form):
        captcha = RoCaptchaField()

To allow for runtime specification of keys you can optionally pass ``private_key`` and ``public_key`` parameters to the constructor, i.e.::
    
    captcha = RoCaptchaField(
        public_key='49c47baecc3738a36bb99665e290fc',
        private_key='e5b725f71537ec50ceee5c6a9b27d6'
    )

Credits
-------
Inspired by `Django reCAPTCHA widget <https://github.com/praekelt/django-recaptcha/>`_.
