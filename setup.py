from importlib.metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
    name='coachbot_simulation',
    version='1.0',
    description='',
    author='Devesh Bhura',
    author_email='deveshbhura2023@u.northwestern.edu',
    url='',
    packages=find_packages(),
    entry_points={'console_scripts':['coachbot_simulation = coachbot_simulation.__main__:main'],},
)