from setuptools import setup

setup(
    name="SuperMS",
    description='Supercalifragilisticexpialidocius Monitoring System project',
    author='Daniel Herkel',
    version=0.1,
    url='https://github.com/daniel00oo/CloudBaseSMS',
    scripts=[
        'receive2.py',
        'send.py',
        'Receiver.py',
        'Sender.py',
        'Repeat.py',
        'StorageMongoDB.py',
    ],
    packages=['tools'],
    package_dir={'tools': './tools'},
    package_data={'tools': []},
    install_requires=[
        'pymongo',
        'pika',
    ],
    )