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

from deepspyce import datasets

import numpy as np

import pandas as pd

import pytest

# =============================================================================
# TESTS
# =============================================================================


def test_load_csv():
    """Test for loading csv_test file."""
    result = datasets.load_csv_test()
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2048, 2)
    np.testing.assert_almost_equal(result[0].mean(), 16174.182128, 6)
    np.testing.assert_almost_equal(result[1].mean(), 16153.399902, 6)


def test_load_raw_bin():
    """Test for opening raw_test file."""
    result = datasets.load_raw_test(ret_df=False)

    assert isinstance(result, bytes)
    assert len(result) == 32768


def test_load_raw_1m_bin():
    """Test for the size of the raw_test_1m file."""
    result = datasets.load_raw_1m(ret_df=False)

    assert isinstance(result, bytes)
    assert len(result) == 11796480
    with pytest.raises(UnicodeDecodeError):
        result.decode()


def test_load_raw_df():
    """Test for opening raw_test file as DataFrame."""
    result = datasets.load_raw_test()

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2048, 2)
    np.testing.assert_almost_equal(result[0].mean(), 16174.182128, 6)
    np.testing.assert_almost_equal(result[1].mean(), 16153.399902, 6)


def test_load_raw_1m_df():
    """Test for opening raw_test_1m file as DataFrame."""
    result = datasets.load_raw_1m()

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2048, 720)
    np.testing.assert_almost_equal(result[0].mean(), 16174.182128, 6)
    np.testing.assert_almost_equal(result.iloc[0].mean(), 48768.425, 3)
    np.testing.assert_almost_equal(result.iloc[2047].mean(), 0.0, 5)


def test_load_iar():
    """Test for opening test iar file."""
    result = datasets.load_iar()

    assert isinstance(result, dict)
    assert len(result) == 16
    assert result["Source Name"] == "J0437-4715_1_A1"
    assert result["Reference DM"] == 2.64476
    np.testing.assert_allclose(
        [type(v) == float for v in list(result.values())[1:]], True
    )
