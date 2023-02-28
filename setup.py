#! /usr/bin/env python

"""A python library for interacting with the VTube Studio API"""

from setuptools import setup, find_packages
import pyvts

DESCRIPTION = "A python library for interacting with the VTube Studio API"
VERSION = pyvts.__version__

setup(name='pyvts',
      version=VERSION,
      description=DESCRIPTION,
      long_description=open("README.md").read(),
      keywords='vtubestudio',
      classifiers=['Development Status :: Alpha',
                   'Intended Audience :: Developers',
                   'License :: MIT',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10'],
      author='Genteki Zhang',
      author_email='zhangkaiyuan.null@gmail.com',
      url='https://github.com/Genteki/pyvts',
      license='MIT',
      packages=find_packages(exclude=['*.tests',
                                      '*.tests.*']),
      install_requires=['websockets',
                        'aiofile'])