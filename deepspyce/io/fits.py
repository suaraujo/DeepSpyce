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

"""Module with .fits I/O functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime

from astropy.io import fits
from astropy.table import Table

from deepspyce.io.raw import raw_to_df

import numpy as np

import pandas as pd


# ============================================================================
# FUNCTIONS
# ============================================================================


def make_fits_header(
    header: dict = None, template: bool = False
) -> fits.Header:
    """Create a header if desired."""
    if header is None:
        header = dict()
    if not isinstance(header, fits.Header):
        header = fits.Header(header)
    if template:
        # Sample: TREG_091209.cal.acs.txt [Single Dish FITS (SDFITS)]
        header["SIMPLE"] = ("T", "/ conforms to FITS standard")
        header["BITPIX"] = (8, "/ BITS/PIXEL")
        header["NAXIS"] = (0, "/ number of array dimensions")
        header["EXTEND"] = ("T", "/File contains extensions")
        header["DATE"] = (datetime.today().strftime("%y-%m-%d"), "/")
        header["ORIGIN"] = ("IAR", "/ origin of observation")
        header["TELESCOP"] = ("Antena del IAR", "/ the telescope used")
        header["OBSERVAT"] = ("IAR", "/ the observatory")
        header["GUIDEVER"] = (
            "DeepSpyce ver1.0",
            "/ this file was created by DeepSpyce",
        )
        header["FITSVER"] = ("1.6", "/ FITS definition version")
    return header


def df_to_fits(
    df: pd.DataFrame,
    outfile: os.PathLike,
    overwrite: bool = False,
    header: bool = None,
) -> None:
    """Create .fits from dataframe or ndarray."""
    hdr = make_fits_header(header)
    primary_hdu = fits.PrimaryHDU(header=hdr)
    tab = Table(np.asarray(df))
    bintable_hdu = fits.BinTableHDU(tab, header=hdr, name="SINGLE DISH")
    hdul = fits.HDUList([primary_hdu, bintable_hdu])
    hdul.writeto(outfile, overwrite=overwrite)
    return


def raw_to_fits(
    rawfile: os.PathLike,
    outfile: os.PathLike,
    overwrite: bool = False,
    header: bool = None,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> None:
    """Create .fits from .raw file."""
    data = raw_to_df(rawfile, n_channels, fmt, order)
    df_to_fits(data, outfile, overwrite, header)
    return
