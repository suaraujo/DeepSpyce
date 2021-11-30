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

"""Module with .raw I/O functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import os

from deepspyce.utils.files_utils import read_file

import numpy as np

import pandas as pd

# ============================================================================
# FUNCTIONS
# ============================================================================


def raw_to_df(
    rawfile: os.PathLike,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Read a binary raw data file, and returns a dataframe."""
    bin_raw = read_file(rawfile, "rb")
    dt = np.dtype(fmt)
    np_data = np.frombuffer(bin_raw, dtype=dt)
    bytes_per_data = dt.alignment
    total_bytes = len(bin_raw)
    n_records = int(total_bytes / n_channels / bytes_per_data)
    np_data = np_data.reshape(n_channels, n_records, order=order)

    return pd.DataFrame(np_data)
