#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   DeepSpyce Project (https://github.com/suaraujo/DeepSpyce).
# Copyright (c) 2020, Susana Beatriz Araujo Furlan
# License: MIT
#   Full Text: https://github.com/suaraujo/DeepSpyce/blob/master/LICENSE


# ============================================================================
# IMPORTS
# ============================================================================

import io

from deepspyce import datasets, raw2df

import pandas as pd

import pytest

# =============================================================================
# TESTS
# =============================================================================


@pytest.mark.parametrize("fmt", [">i4", "<q", "l"])
@pytest.mark.parametrize("shape", [(300, 2), (2048, 5), (1024, 4)])
@pytest.mark.parametrize("top", [100_000, 10_000, 1_000_000])
@pytest.mark.parametrize("order", ["C", "F"])
def test_read(
    df_and_file: callable, fmt: str, shape: tuple, top: int, order: str
):
    """Test for raw to dataframe conversion."""

    original, raw_file = df_and_file(
        fmt=fmt, shape=shape, top=top, order=order, seed=42
    )
    result = raw2df(raw=raw_file, order=order, fmt=fmt, n_channels=shape[0])
    pd.testing.assert_frame_equal(original, result)


def test_read_fixed():
    """Fixed test for raw to dataframe conversion."""
    original = datasets.load_csv_test()
    result = raw2df(io.BytesIO(datasets.load_raw_test()))

    pd.testing.assert_frame_equal(original, result)


# def test_estad(
#     data_df: pd.DataFrame, data_file: io.BufferedReader,
# ):

#     df0 = raw2df(data_file)
#     df1 = data_df

#     a = df0.describe()
#     b = df1.describe()

#     pd.testing.assert_frame_equal(a, b)
