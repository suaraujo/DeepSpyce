#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   DeepSpyce Project (https://github.com/suaraujo/DeepSpyce).
# Copyright (c) 2020, Susana Beatriz Araujo Furlan
# License: MIT
#   Full Text: https://github.com/suaraujo/DeepSpyce/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""
This file is for distribute and install DeepSpyce
"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup  # noqa

# =============================================================================
# CONSTANTS
# =============================================================================

REQUIREMENTS = ["numpy", "pandas", "astropy"]

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()

with open(PATH / "deepspyce" / "__init__.py") as fp:
    for line in fp.readlines():
        if line.startswith("__version__ = "):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break


DESCRIPTION = "Reading raw files of radio-astronomical data"


# =============================================================================
# FUNCTIONS
# =============================================================================


def do_setup():
    setup(
        name="deepspyce",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=[
            "Susana Beatriz Araujo Furlan",
            "Marcelo Colazo",
            "Emmanuel Gianuzzi",
            "Gabriel Oio",
        ],
        author_email="saraujo@iar.unlp.edu.ar",
        url="https://github.com/suaraujo/DeepSpyce",
        py_modules=["ez_setup"],
        packages=["deepspyce"],
        # include_package_data=True,
        license="MIT",
        install_requires=REQUIREMENTS,
        keywords=["deepspyce"],
        classifiers=[
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering",
        ],
    )


if __name__ == "__main__":
    do_setup()
