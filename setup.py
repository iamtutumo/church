from setuptools import setup, find_packages
import os

# Get the directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# Read the contents of requirements.txt file
try:
    with open(os.path.join(HERE, 'requirements.txt'), 'r') as f:
        install_requires = f.read().strip().split("\n")
except FileNotFoundError:
    install_requires = []

# get version from __version__ variable in church/__init__.py
from church import __version__ as version

setup(
    name="church",
    version=version,
    description="A comprehensive church management system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)