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

import numpy as np

import pandas as pd

import pytest


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def df_and_file() -> callable:
    def df_rand(
        fmt: np.dtype = ">i8", shape: tuple = (2048, 5), top: int = 100_000
    ) -> pd.DataFrame:
        rng = np.random.RandomState(42)
        dt = np.dtype(fmt)
        df = pd.DataFrame(rng.randint(top, size=shape), dtype=dt)

        return df

    def df_and_raw(
        fmt: np.dtype = ">i8",
        shape: tuple = (2048, 5),
        top: int = 100_000,
        order: str = "C",
        df_rand: callable = df_rand,
    ) -> io.BytesIO:
        df = df_rand(fmt=fmt, shape=shape, top=top)
        df_bytes = np.array(df).tobytes(order)
        df_bytes_io = io.BytesIO(df_bytes)

        return df, df_bytes_io

    return df_and_raw
