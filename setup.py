#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__='Basile Marchand'
__version__='0.1.0'

name = 'cpp_header_sanitizer'
contact="basile.marchand@gmail.com"

from setuptools import setup, find_packages
import pathlib as pl

here = pl.Path(__file__).parent.absolute()

requirements = []
with open( here / pl.Path("requirements.txt")) as fid:
    content = fid.read().split("\n")
    for line in content:
        if line.startswith( "#" ) or line.startswith( " " ) or line=="":
            continue
        elif line.startswith( "-e" ):
            pname = line.split("#egg=")[1]
            req_line = "{} @ {}".format( pname, line[3:] )
            requirements.append( req_line )
        else:
            requirements.append( line )

with open(here / pl.Path("README.md")) as fid:
    long_description = fid.read()

extras_require = {'test':['pytest',]}


setup(
    name=name,
    version=__version__,
    author_email=contact,
    description="C++ Header file sanitizer",
    long_description=long_description,
    license="",
    url="",
    classifiers=[
        'Development Status :: 1 - Beta',
    ],
    install_requires=requirements,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    entry_points = {
        'console_scripts': ['cppsanitizer=cppsanitizer:main'],
    }
)