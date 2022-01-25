#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   DeepSpyce Project (https://github.com/suaraujo/DeepSpyce).
# Copyright (c) 2020, Susana Beatriz Araujo Furlan
# License: MIT
#   Full Text: https://github.com/suaraujo/DeepSpyce/blob/master/LICENSE

# ============================================================================
# DOCS
# ============================================================================

"""The deepspyce.io module provides input/output tools."""

# =============================================================================
# IMPORTS
# =============================================================================

from .filterbank import (  # noqa
    df_to_filterbank,  # noqa
    iar_to_fil_header,  # noqa
    raw_to_filterbank,  # noqa
)  # noqa
from .fits import df_to_fits, make_fits_header, raw_to_fits  # noqa
from .iar import read_iar  # noqa
from .raw import raw_to_df  # noqa
