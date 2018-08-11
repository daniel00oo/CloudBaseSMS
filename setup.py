from setuptools import setup

setup(
    name="SuperMS",
    description='Supercalifragilisticexpialidocius Monitoring System project',
    author='Daniel Herkel',
    version=0.1,
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
    )