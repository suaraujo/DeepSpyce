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

import itertools

import pandas as pd

from deepspyce import datasets

from deepspyce import raw2df


# =============================================================================
# TESTS
# =============================================================================


def test_read(
    df_and_file: callable,
):
    """Test for raw to dataframe conversion."""

    df_and_raw = df_and_file
    fmts = [">i4", "<q", "l"]
    shapes = [(300, 2), (2048, 5), (1024, 4)]
    tops = [100_000, 10_000, 1_000_000]
    orders = ["C", "F"]
    for fmt, shape, top, order in itertools.product(
        fmts, shapes, tops, orders
    ):
        kwargs = dict(fmt=fmt, shape=shape, top=top, order=order)
        original, file = df_and_raw(**kwargs)
        result = raw2df(raw=file, order=order, fmt=fmt, n_channels=shape[0])
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
