#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [ ]

setup_requirements = [ ]

test_requirements = ['pytest', ]

setup(
    author="Wataru Hirota",
    author_email='w-hirota@ist.osaka-u.ac.jp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="The tool for estimating document similarity",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='docsim',
    name='docsim',
    python_requires='>=3.8',
    packages=find_packages(include=['docsim']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tarohi24/docsim',
    version='0.1.0',
    zip_safe=False,
)
