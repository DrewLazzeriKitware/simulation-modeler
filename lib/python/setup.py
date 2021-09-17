#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages

# perform the install
setup(
    name="pf-web",
    license="BSD-3-Clause",
    classifiers=[],
    keywords="Pywebvue components for parflow",
    packages=find_packages("src", exclude=("tests.*", "tests")),
    package_dir={"": "src"},
    package_data={},
    install_requires=[],
)
