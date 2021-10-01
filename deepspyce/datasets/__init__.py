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

"""The deepspyce.datasets module includes utilities to load datasets."""

# ============================================================================
# IMPORTS
# ============================================================================

import os
import pathlib

import numpy as np

import pandas as pd

# ============================================================================
# CONSTANTS
# ============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

# ============================================================================
# FUNCTIONS
# ============================================================================


def load_raw():
    """Load raw data file."""
    path = PATH / "20201027_133329_1m.raw"

    with open(path, "rb") as file:
        raw = file.read()
    return raw


def load_raw_test():
    """Load raw_test data file."""
    path = PATH / "20201027_133329_test.raw"

    with open(path, "rb") as file:
        raw_test = file.read()
    return raw_test


def load_csv_test(fmt: np.dtype = ">i8") -> pd.DataFrame:
    """Load csv_test data file."""
    path = PATH / "20201027_133329_test.csv"

    return pd.read_csv(path, dtype=fmt, header=None)


def load_iar():
    """Load iar data file."""
    path = PATH / "J0437-4715_1_A1.iar"

    with open(path, "r") as file:
        iar = file.read()
    return iar
