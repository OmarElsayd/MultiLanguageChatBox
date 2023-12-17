from setuptools import setup, find_packages
from rtvt_services.const import req_lib_path

with open(req_lib_path, 'r') as file:
    lib_list = [line.rstrip() for line in file.readlines()]

setup(
    name='rtvt_services',
    version='0.0.1',
    author='Omar Elsayd',
    author_email='omar.elsayd@hotmail.com',
    maintainer='Omar Elsayd',
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.11"],
    install_requires=lib_list,
)