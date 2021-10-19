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

from deepspyce import ReadRaw

import pandas as pd

# ============================================================================
# CONSTANTS
# ============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

# ============================================================================
# FUNCTIONS
# ============================================================================


def load_raw_1m(ret_df: bool = True):
    """Load template raw data file."""
    path = PATH / "20201027_133329_1m.raw"

    if ret_df:
        return ReadRaw(path)
    else:
        with open(path, "rb") as file:
            raw = file.read()
        return raw


def load_raw_test(ret_df: bool = True):
    """Load template raw_test data file."""
    path = PATH / "20201027_133329_test.raw"

    if ret_df:
        return ReadRaw(path)
    else:
        with open(path, "rb") as file:
            raw_test = file.read()
        return raw_test


def load_csv_test() -> pd.DataFrame:
    """Load template csv_test data file."""
    path = PATH / "20201027_133329_test.csv"

    return pd.read_csv(path, dtype=">i8", header=None)


def load_iar():
    """Load template .iar file."""
    path = PATH / "J0437-4715_1_A1.iar"

    with open(path, "r") as file:
        iar = file.read()
    return iar