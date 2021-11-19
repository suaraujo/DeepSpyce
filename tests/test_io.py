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

from deepspyce import datasets, df_to_fits, raw_to_df

import pandas as pd

import pytest

# =============================================================================
# TESTS
# =============================================================================


@pytest.mark.parametrize("fmt", [">i4", "<q", "l"])
@pytest.mark.parametrize("shape", [(300, 2), (2048, 5), (1024, 4)])
@pytest.mark.parametrize("top", [100_000, 10_000, 1_000_000])
@pytest.mark.parametrize("order", ["C", "F"])
def test_raw_to_df(
    df_and_buff: callable, fmt: str, shape: tuple, top: int, order: str
):
    """Test for reading mock raw files to dataframe conversion."""

    original, buff_raw = df_and_buff(
        fmt=fmt, shape=shape, top=top, order=order, seed=42
    )
    result = raw_to_df(
        path_or_stream=buff_raw, n_channels=shape[0], fmt=fmt, order=order
    )
    pd.testing.assert_frame_equal(original, result)


def test_raw_to_df_template():
    """Test for reading template raw file to dataframe conversion."""
    path = datasets.PATH / "20201027_133329_test.raw"
    original = datasets.load_csv_test()
    result = raw_to_df(path_or_stream=path)

    pd.testing.assert_frame_equal(original, result)


@pytest.mark.parametrize("data", [False, 0, 0.0, [0], (0, 0.0), {0: 0}])
def test_raw_to_df_wrong_input(data: any):
    """Test for wrong input at dataframe conversion."""
    with pytest.raises(AttributeError):
        raw_to_df(path_or_stream=data)


def test_raw_to_df_wrong_path(wrong_path):
    """Test for wrong raw path at dataframe conversion."""
    with pytest.raises(FileNotFoundError):
        raw_to_df(path_or_stream=wrong_path)


def test_df_to_fits_wrong_path(wrong_path):
    """Test for wrong Dir at fits conversion."""
    df = datasets.load_csv_test()
    with pytest.raises(IOError):
        df_to_fits(data=df, path_or_stream=wrong_path)


def test_df_to_fits(stream):
    """Test for converting and writing DataFrame into .fits file."""
    df = datasets.load_csv_test()
    path = stream()
    df_to_fits(data=df, path_or_stream=path)

    assert path.tell() == 40320
