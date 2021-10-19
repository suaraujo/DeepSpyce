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

from deepspyce import datasets, df2Fits

import pytest

# =============================================================================
# TESTS
# =============================================================================


def test_WrongDir(Wrong_Path):
    """Test for wrong Dir at fits conversion."""
    df = datasets.load_csv_test()
    with pytest.raises(IOError):
        df2Fits(data=df, path=Wrong_Path)


def test_df2Fits(tmp_file_path):
    """Test for converting and writing DataFrame into .fits file."""
    df = datasets.load_csv_test()
    path = tmp_file_path(filename="data.fits")
    df2Fits(data=df, path=path)
    assert path.exists()
    assert path.size() == 40320
