import os
from setuptools import setup, find_packages

VERSION = os.path.join(os.path.dirname(__file__), 'VERSION')
VERSION = open(VERSION, 'r').read().strip()

setup(
    name='grano-client',
    version=VERSION,
    description="Client library for grano, a social network analysis tool.",
    long_description=open('README.rst').read(),
    classifiers=[
        ],
    keywords='data client rest grano sna ddj journalism',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='https://github.com/granoproject/grano-client',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        "requests>=2.2.0",
        "PyYAML==3.10"
    ],
    tests_require=[],
    entry_points=\
    """ """,
)
