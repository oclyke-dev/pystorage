#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name='blue_heron',
  version='0.0.0',
  url='https://github.com/oclyke-dev/pystorage',
  license='MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  include_package_data=True,
  zip_safe=False,
  classifiers=[
    'Topic :: Utilities'
  ],
  keywords = [
    'micropython',
    'json',
    'config',
    'storage',
  ],
  scripts=[
  ],
  package_data={
    'src/storage': [
    ],
  },
)
