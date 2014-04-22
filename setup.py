#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-rocaptcha",
    version="0.1.0",
    author="Vojtech Oram",
    author_email="vojtech@oram.cz",
    description=("RoCAPTCHA form widget for Django."),
    license = "CC BY 4.0",
    keywords = "captcha rotation animal shelter",
    packages=['rocaptcha'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Utilities",
    ],
    include_package_data=True,
)
