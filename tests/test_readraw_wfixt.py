import pytest

import numpy as np

import pandas as pd

import struct as stc

import deepspyce as dspy


@pytest.fixture
def data_df():
    np.random.seed(42)
    df0 = pd.DataFrame(np.random.randint(0, 100000, size=(5, 2048)))
    return df0


@pytest.fixture
def data_raw(data_df):
    df_np0 = data_df.to_numpy(dtype="float64")
    df_np1 = df_np0.flatten()
    n_elem = len(df_np1)

    raw_df0 = stc.pack("d" * n_elem, *df_np1)
    # in order that struct packs all the elements we need to specified the
    # number of elements
    return raw_df0


def test_read(data_df, data_raw):
    df1 = dspy.raw2df(data_raw)
    df0 = data_df

    assert df0 == df1
