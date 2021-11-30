#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   DeepSpyce Project (https://github.com/suaraujo/DeepSpyce).
# Copyright (c) 2020, Susana Beatriz Araujo Furlan
# License: MIT
#   Full Text: https://github.com/suaraujo/DeepSpyce/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Auxiliar functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import warnings

import numpy as np

# ============================================================================
# FUNCTIONS
# ============================================================================


def data_to_bytes(
    data=np.ndarray, fmt: np.dtype = ">i8", order: str = "F"
) -> bytes:
    """Convert common data array to bytes."""
    return np.asarray(data, dtype=np.dtype(fmt)).tobytes(order)


def deepwarn(message):
    """Generate a warning."""
    warnings.warn(message, stacklevel=2)

    return
