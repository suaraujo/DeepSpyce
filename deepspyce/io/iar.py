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

"""Module with .iar I/O functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import os

from deepspyce.utils.files_utils import read_file

# ============================================================================
# FUNCTIONS
# ============================================================================


def read_iar(iarfile: os.PathLike) -> dict:
    """Read .iar file into dict."""
    iar = read_file(iarfile, "r")
    iar = dict([line.split(",") for line in iar.splitlines()])
    for key, value in iar.items():
        try:
            iar[key] = float(value)
        except ValueError:
            continue

    return iar
