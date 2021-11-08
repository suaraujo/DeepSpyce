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

"""Module with core functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import io
import os
from datetime import datetime

from astropy.io import fits
from astropy.table import Table

import numpy as np

import pandas as pd

# ============================================================================
# FUNCTIONS
# ============================================================================


def buff_raw_to_df(
    buff_raw: io.BufferedReader,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Convert buffered raw data to dataframe."""
    # Transformamos de str(bytes) a np.array
    data = buff_raw.read()
    dt = np.dtype(fmt)
    np_data = np.array(np.frombuffer(data, dtype=dt))
    bytes_per_data = dt.alignment
    total_bytes = buff_raw.tell()
    n_records = int(total_bytes / n_channels / bytes_per_data)
    np_data = np_data.reshape(n_channels, n_records, order=order)

    return pd.DataFrame(np_data)


def df_to_fits(
    data: pd.DataFrame, path_or_stream: str, overwrite: bool = False
) -> None:
    """Create .fits from dataframe."""
    # Sample: TREG_091209.cal.acs.txt [Single Dish FITS (SDFITS)]
    hdr = fits.Header()
    hdr["SIMPLE"] = ("T", "/ conforms to FITS standard")
    hdr["BITPIX"] = (8, "/ BITS/PIXEL")
    hdr["NAXIS"] = (0, "/ number of array dimensions")
    hdr["EXTEND"] = ("T", "/File contains extensions")
    hdr["DATE"] = (datetime.today().strftime("%y-%m-%d"), "/")
    hdr["ORIGIN"] = ("IAR", "/ origin of observation")
    hdr["TELESCOP"] = ("Antena del IAR", "/ the telescope used")
    # hdr["OBSERVAT"] = ("IAR", "/ the observatory")
    hdr["GUIDEVER"] = (
        "DeepSpyce ver1.0",
        "/ this file was created by DeepSpyce",
    )
    hdr["FITSVER"] = ("1.6", "/ FITS definition version")

    primary_hdu = fits.PrimaryHDU(header=hdr)
    tab = Table(np.asarray(data))
    bintable_hdu = fits.BinTableHDU(tab, header=hdr, name="SINGLE DISH")
    hdul = fits.HDUList([primary_hdu, bintable_hdu])
    hdul.writeto(path_or_stream, overwrite=overwrite)

    return


def read_raw(
    path_or_stream,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Read a raw data file, and returns a dataframe."""
    if isinstance(path_or_stream, (str, bytes, os.PathLike)):
        if os.path.isfile(path_or_stream):
            with open(path_or_stream, "rb") as raw:
                return buff_raw_to_df(
                    raw, n_channels=n_channels, fmt=fmt, order=order
                )
        else:
            raise FileNotFoundError(
                "{} is not a valid path".format(path_or_stream)
            )
    else:
        return buff_raw_to_df(
            path_or_stream, n_channels=n_channels, fmt=fmt, order=order
        )
