from setuptools import setup, find_packages

# Get version
try:
    from church import __version__ as version
except ImportError:
    version = '0.0.1'

setup(
    name="church",
    version=version,
    description="A comprehensive church management system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'frappe'
    ]
)