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

from deepspyce import Raw2df, ReadRaw, datasets

import pandas as pd

import pytest

# =============================================================================
# TESTS
# =============================================================================


@pytest.mark.parametrize("fmt", [">i4", "<q", "l"])
@pytest.mark.parametrize("shape", [(300, 2), (2048, 5), (1024, 4)])
@pytest.mark.parametrize("top", [100_000, 10_000, 1_000_000])
@pytest.mark.parametrize("order", ["C", "F"])
def test_Raw2df(
    df_and_file: callable, fmt: str, shape: tuple, top: int, order: str
):
    """Test for buffered raw to dataframe conversion."""

    original, raw_file = df_and_file(
        fmt=fmt, shape=shape, top=top, order=order, seed=42
    )
    result = Raw2df(raw=raw_file, order=order, fmt=fmt, n_channels=shape[0])
    pd.testing.assert_frame_equal(original, result)


def test_Raw2df_fixed():
    """Test for buffered template raw to dataframe conversion."""
    original = datasets.load_csv_test()
    result = Raw2df(raw=io.BytesIO(datasets.load_raw_test(ret_df=False)))

    pd.testing.assert_frame_equal(original, result)


def test_ReadRaw_fixed():
    """Test for reading template raw to dataframe conversion."""
    path = datasets.PATH / "20201027_133329_test.raw"
    original = datasets.load_csv_test()
    result = ReadRaw(path=path)

    pd.testing.assert_frame_equal(original, result)


def test_WrongPath(Wrong_Path):
    """Test for wrong raw path at dataframe conversion."""
    with pytest.raises(FileNotFoundError):
        ReadRaw(path=Wrong_Path)


# def test_estad(
#     data_df: pd.DataFrame, data_file: io.BufferedReader,
# ):

#     df0 = raw2df(data_file)
#     df1 = data_df

#     a = df0.describe()
#     b = df1.describe()

#     pd.testing.assert_frame_equal(a, b)
