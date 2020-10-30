import deepspyce as dspy

import pytest


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def vacio_path():
    return "datasets/vacio.raw"


@pytest.fixture
def vacio_df(vacio_path):
    return dspy.read_raw(vacio_path)


# =============================================================================
# TESTS
# =============================================================================

def test_read_raw(vacio_df):
    assert df.mean() == 25
    assert df.std() == .3
