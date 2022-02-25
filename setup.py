from setuptools import setup, find_packages


setup(
    version='1.6',
    packages=find_packages(include=['scapy']),
    install_requires=[
        'scapy>=2.3.2',
    ]
)
