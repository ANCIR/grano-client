from setuptools import setup, find_packages


setup(
    name='grano-client',
    version='0.2.2',
    description="Client library for grano, a social network analysis tool.",
    long_description=open('README.rst').read(),
    classifiers=[
        ],
    keywords='data client rest grano sna ddj journalism',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='https://github.com/pudo/grano-client',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        "requests>=2.2.0"
    ],
    tests_require=[],
    entry_points=\
    """ """,
)
