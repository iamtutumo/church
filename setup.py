from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in church/__init__.py
from church import __version__ as version

setup(
    name="church",
    version=version,
    description="A comprehensive church management system",
    author="Tutu Moses",
    author_email="etu.moses@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)