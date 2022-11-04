from setuptools import setup

setup(
    name='data_simulator',
    version='',
    packages=['api', 'api.kafka', 'api.tests', 'api.helpers', 'api.sensors', 'api.raspberrypi', 'model', 'generators',
              'generators.kafka', 'kafka', 'tests', 'helpers', 'sensors', 'raspberrypi'],
    package_dir={'': 'api'},
    url='',
    license='',
    author='anaescobar',
    author_email='ana.escobar-llamazares@edu.dsti.institute',
    description=''
)
