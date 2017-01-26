#!/usr/bin/env python

from distutils.core import setup

setup(name='BBChop',
      version='1.0',
      description='Bayesian Binary Chop: Bayesian Search over a repository.',
      author='Ealdwulf Wuffinga',
      url='https://github.com/Ealdwulf/BBChop',
      packages=['BBChop'],
      package_dir = {'BBChop': 'BBChop/source'},
      scripts = ['BBChop/source/bbchop'],
     )

