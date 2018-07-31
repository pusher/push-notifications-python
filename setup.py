from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    author='Pusher',
    author_email='support@pusher.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    dependency_links=dependency_links,
    description='Pusher Push Notifications Python server SDK',
    include_package_data=True,
    install_requires=install_requires,
    long_description=long_description,
    name='pusher_push_notifications',
    packages=find_packages(exclude=['tests']),
    version=__version__,
)
