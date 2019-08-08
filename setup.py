#!/usr/bin/env python

from setuptools import setup
import flaggit

setup(
    name='django-flaggit',
    description='Generic content flagging for Django',
    long_description=open('README.md').read(),
    packages=['flaggit', 'flaggit.templatetags'],
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-flaggit',
    version=flaggit.__version__,
    include_package_data=True,
    package_data={'flaggit': ['templates/flaggit/*.html'], },
    zip_safe=False,
)
