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

from deepspyce import datasets, df_to_fits

import pytest

# =============================================================================
# TESTS
# =============================================================================


def test_wrong_path(wrong_path):
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
