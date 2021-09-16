import io

import numpy as np
import pandas as pd
import pytest

import deepspyce as dspy

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def data_df() -> pd.DataFrame:
    np.random.seed(42)
    dt = np.dtype("q")  # 8 bytes
    df0 = pd.DataFrame(np.random.randint(0, 100000, size=(5, 2048), dtype=dt))
    # Con dt nos aseguramos que son int64
    return df0


@pytest.fixture
def data_raw(data_df: pd.DataFrame) -> bytes:

    df_np0 = np.array(data_df, dtype=">q")
    df_np1 = df_np0.flatten()
    # n_elem = len(df_np1)

    raw_df0 = df_np1.tobytes("C")  # esto esta en formato C ---> pasar a F
    # usar struct es un viaje, no encontre la forma de usarlo y que
    # guarde bien los datos para desp volver a leerlo, x mas que
    # supuestamente era la forma correcta de grabarlo

    return raw_df0


@pytest.fixture
def data_file(data_raw: bytes):
    fd = io.BytesIO(
        data_raw
    )  # poner el data en el constructuor xq sino desp hay que usar un seek(0)
    # fd.write()

    return fd


# =============================================================================
# TESTS
# =============================================================================


def test_read(
    data_df: pd.DataFrame, data_raw: callable, data_file: callable,
):

    df1 = dspy.raw2df(data_file(data_raw(data_df)))
    df0 = data_df.transpose()  # verificar trasposición

    pd.testing.assert_frame_equal(df1, df0)


def test_estad(
    data_df: pd.DataFrame, data_raw: callable, data_file: callable,
):
    df1 = dspy.raw2df(data_file(data_raw(data_df)))

    df0 = data_df.transpose()  # verificar trasposición

    a = df1.describe()
    b = df0.describe()

    pd.testing.assert_series_equal(a, b)
