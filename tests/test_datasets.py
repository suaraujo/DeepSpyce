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


import numpy as np

import pandas as pd

import deepspyce.datasets as datasets

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


def test_load_raw():
    """Test for loading raw_test file."""
    result = datasets.load_raw_test()

    assert isinstance(result, bytes)
    assert len(result) == 32768


def test_load_raw_big():
    """Test for the size of the raw_test file."""
    result = datasets.load_raw()

    assert isinstance(result, bytes)
    assert len(result) == 11796480
    with pytest.raises(UnicodeDecodeError):
        result.decode()


def test_load_iar():
    """Test for the size of the raw_test file."""
    result = datasets.load_iar()

    assert isinstance(result, str)
    assert len(result) == 370
    assert len(result.splitlines()) == 16
    assert len([letter for letter in result if letter.isupper()]) == 46
