from setuptools import setup, find_packages
from nanoservices import __version__

setup(name='nanoservices',
    version=__version__,
    description='model and transformation library for pragmatic mda approach',
    url='https://github.com/dfriedenberger/nanoservices.git',
    author='Dirk Friedenberger',
    author_email='projekte@example.com',
    license='GPLv3',
    packages=find_packages(include=['nanoservices']),
    scripts=['bin/nano-cli']
)