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


def Raw2df(
    raw: io.BufferedReader,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Convert buffered raw data to dataframe."""
    # Transformamos de str(bytes) a np.array
    data = raw.read()
    dt = np.dtype(fmt)
    np_data = np.array(np.frombuffer(data, dtype=dt))
    bytes_per_data = dt.alignment
    total_bytes = raw.tell()
    n_records = int(total_bytes / n_channels / bytes_per_data)
    np_data = np_data.reshape(n_channels, n_records, order=order)

    return pd.DataFrame(np_data)


def df2Fits(
    data: pd.DataFrame, path: str = "test.fits", overwrite: bool = True
) -> None:
    """Create .fits from dataframe."""
    DIR = os.path.dirname(path)
    if (DIR != "") and (not os.path.isdir(DIR)):
        raise IOError("{} is not an existing directory.".format(DIR))
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

    Primary_hdu = fits.PrimaryHDU(header=hdr)
    Tab = Table(np.asarray(data))
    BinTable_hdu = fits.BinTableHDU(Tab, header=hdr, name="SINGLE DISH")
    hdul = fits.HDUList([Primary_hdu, BinTable_hdu])
    hdul.writeto(path, overwrite=overwrite)

    return


def ReadRaw(
    path: str,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Read a raw data file, and returns a dataframe."""
    if os.path.isfile(path):
        with open(path, "rb") as raw:
            return Raw2df(raw, n_channels=n_channels, fmt=fmt, order=order)
    else:
        raise FileNotFoundError("{} is not a valid Path".format(path))
