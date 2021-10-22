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


@pytest.fixture(scope="session")
def df_rand():
    def make(
        fmt: np.dtype = ">i8",
        shape: tuple = (2048, 5),
        top: int = 100_000,
        seed: int = None,
    ):
        rng = np.random.default_rng(seed=seed)
        dt = np.dtype(fmt)
        df = pd.DataFrame(rng.integers(top, size=shape), dtype=dt)
        return df

    return make


@pytest.fixture(scope="session")
def df_and_buff(df_rand) -> callable:
    def make(order: str = "C", **kwargs) -> io.BytesIO:
        df = df_rand(**kwargs)
        df_bytes = np.array(df).tobytes(order)
        df_bytes_io = io.BytesIO(df_bytes)
        return df, df_bytes_io

    return make


@pytest.fixture(scope="session")
def stream() -> io.BytesIO:
    def make(data: any = None):
        return io.BytesIO(data)

    return make


@pytest.fixture(scope="session")
def wrong_path():

    return "/Not/A/Valid/Path"
