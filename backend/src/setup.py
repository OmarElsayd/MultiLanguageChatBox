#Adding comment
from setuptools import setup, find_packages
from mlcb_services.util.constant import REQ_LIB_PATH

with open(REQ_LIB_PATH, 'r') as file:
    lib_list = [line.rstrip() for line in file.readlines()]

setup(
    name='mlcb_services',
    version='0.0.1',
    author='Omar Elsayd',
    author_email='omar.elsayd@hotmail.com',
    maintainer='Omar Elsayd',
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.11"],
    install_requires=lib_list,
)
