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

import warnings

from astropy.io import fits as astrofits

from deepspyce import datasets
from deepspyce.io.filterbank import (
    check_header_start_end,
    df_to_filterbank,
    fixed_header_start_end,
    iar_to_fil_header,
    raw_to_filterbank,
)
from deepspyce.io.fits import df_to_fits, make_fits_header, raw_to_fits
from deepspyce.io.iar import read_iar
from deepspyce.io.raw import raw_to_df
from deepspyce.utils import files_utils

import pandas as pd

import pytest

# ============================================================================
# CONSTANTS
# ============================================================================

rawpath = datasets.PATH / "20201027_133329_test.raw"
iarpath = datasets.PATH / "J0437-4715_1_A1.iar"

# =============================================================================
# TESTS
# =============================================================================


class TestRaw:
    @pytest.mark.parametrize("fmt", [">i4", "<q", "l"])
    @pytest.mark.parametrize("shape", [(300, 2), (2048, 5), (1024, 4)])
    @pytest.mark.parametrize("top", [100_000, 10_000, 1_000_000])
    @pytest.mark.parametrize("order", ["C", "F"])
    def test_raw_to_df(
        self,
        df_and_buff: callable,
        fmt: str,
        shape: tuple,
        top: int,
        order: str,
    ):
        """Test for reading mock raw files to dataframe conversion."""

        original, buff_raw = df_and_buff(
            fmt=fmt, shape=shape, top=top, order=order, seed=42
        )
        result = raw_to_df(buff_raw, n_channels=shape[0], fmt=fmt, order=order)

        pd.testing.assert_frame_equal(original, result)

    def test_raw_to_df_template(self):
        """Test for reading template raw file to dataframe conversion."""
        original = datasets.load_csv_test()
        result = raw_to_df(rawpath)

        pd.testing.assert_frame_equal(original, result)

    @pytest.mark.parametrize(
        "data", [False, 0, 0.0, [0], (0, 0.0), {0: 0}, bytes(0)]
    )
    def test_raw_to_df_wrong_input(self, data: any):
        """Test for wrong input at dataframe conversion."""

        with pytest.raises(OSError):
            raw_to_df(data)

    def test_raw_to_df_wrong_path(self, wrong_path: str):
        """Test for wrong raw path at dataframe conversion."""

        with pytest.raises(FileNotFoundError):
            raw_to_df(wrong_path)


class TestFits:
    def test_make_fits_header_empty(self):
        """Test for making empty header."""
        header = make_fits_header()

        assert header == astrofits.Header()

    def test_make_fits_header_template(self):
        """Test for making template header."""
        header = make_fits_header(template=True)

        assert isinstance(header, astrofits.header.Header)
        assert header["ORIGIN"] == "IAR"

    def test_make_fits_header_given(self):
        """Test for making template header."""
        hdr = astrofits.Header()
        hdr["MAGICNUM"] = 42
        header = make_fits_header(hdr)

        assert isinstance(header, astrofits.header.Header)
        assert header == hdr

    def test_make_fits_header_given_and_template(self):
        """Test for making template header."""
        hdr = astrofits.Header()
        hdr["MAGICNUM"] = 42
        header = make_fits_header(hdr, template=True)

        assert isinstance(header, astrofits.header.Header)
        assert header["MAGICNUM"] == 42
        assert header["ORIGIN"] == "IAR"

    def test_df_to_fits(self, stream: callable, df_rand: callable):
        """Test for writing DataFrame into .fits file."""
        df = df_rand()
        path = stream()
        df_to_fits(df, path)

        assert path.tell() == 89280

    def test_df_to_fits_wrong_path(self, wrong_path: str, df_rand: callable):
        """Test for wrong Dir at fits conversion."""
        df = df_rand()

        with pytest.raises(OSError):
            df_to_fits(df, wrong_path)

    def test_df_to_fits_and_header(self, stream: callable, df_rand: callable):
        """Test for writing DataFrame into .fits file."""
        df = df_rand()
        hdr = astrofits.Header()
        hdr["MAGICNUM"] = 42
        path = stream()
        df_to_fits(df, path, header=hdr)

        assert path.tell() == 89280

    def test_raw_to_fits(self, stream: callable, df_and_buff: callable):
        """Test for writing raw data into .fits file."""
        path = stream()
        _, rawstream = df_and_buff()
        raw_to_fits(rawstream, path)

        assert path.tell() == 89280


class TestIar:
    def test_read_iar(self):
        """Test for convering .iar dict to header dict."""
        iardict = read_iar(iarpath)

        assert isinstance(iardict, dict)


class TestFilterbank:
    def test_check_header_start_end(self):
        """Test for checking HEADER_START and HEADER_END."""
        bad = dict()
        good = dict({"HEADER_START": None, "HEADER_END": None})
        mix0 = dict({"HEADER_START": None})
        mix1 = dict({"HEADER_END": None})
        mix2 = dict({"HEADER_END": None, "HEADER_START": None})
        wrong = dict(
            {"HEADER_START": True, "MAGIC_NUMBER": 42, "HEADER_END": "NO"}
        )
        terrible = dict(
            {"HEADER_END": "NO", "HEADER_START": True, "MAGIC_NUMBER": 42}
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert check_header_start_end(bad, True) == (None, None)
            assert check_header_start_end(good, True) == (True, True)
            assert check_header_start_end(mix0, True) == (True, None)
            assert check_header_start_end(mix1, True) == (None, True)
            assert check_header_start_end(mix2, True) == (False, False)
            assert check_header_start_end(wrong, True) == (False, False)
            assert check_header_start_end(terrible, True) == (False, False)

    def test_fixed_header_start_end(self):
        """Test for fixing HEADER_START and HEADER_END."""
        bad = dict()
        good = dict({"HEADER_START": None, "HEADER_END": None})
        mix0 = dict({"HEADER_START": None})
        mix1 = dict({"HEADER_END": None})
        mix2 = dict({"HEADER_END": None, "HEADER_START": None})
        wrong = dict(
            {"HEADER_START": True, "MAGIC_NUMBER": 42, "HEADER_END": "NO"}
        )
        terrible = dict(
            {"HEADER_END": "NO", "HEADER_START": True, "MAGIC_NUMBER": 42}
        )
        expected = dict(
            {"HEADER_START": None, "MAGIC_NUMBER": 42, "HEADER_END": None}
        )

        assert fixed_header_start_end(bad) == good
        assert fixed_header_start_end(good) == good
        assert fixed_header_start_end(mix0) == good
        assert fixed_header_start_end(mix1) == good
        assert fixed_header_start_end(mix2) == good
        assert fixed_header_start_end(mix2) == good
        assert fixed_header_start_end(wrong) == expected
        assert fixed_header_start_end(terrible) == expected

    def test_iar_to_fil_header_file(self):
        """Test for building header from .iar template file."""
        header = iar_to_fil_header(iarpath)

        assert isinstance(header, dict)
        assert header["data_type"] == 1

    def test_iar_to_fil_header_dict(self):
        """Test for building header from .iar template dict."""
        iardict = read_iar(iarpath)
        header = iar_to_fil_header(iardict)

        assert isinstance(header, dict)
        assert header["data_type"] == 1

    def test_iar_to_fil_header_encode(self):
        """Test for building enconded header from .iar template dict."""
        iardict = read_iar(iarpath)
        header = iar_to_fil_header(iardict, encode=True)
        bin_data_type_1 = b"\t\x00\x00\x00data_type\x01\x00\x00\x00"

        assert isinstance(header, bytes)
        assert bin_data_type_1 in header

    def test_df_to_filterbank(self, stream: callable, df_rand: callable):
        """Test for building .fil from dataframe."""
        df = df_rand()
        outf = stream()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df_to_filterbank(df, outfile=outf)

        assert outf.tell() == 81950

    def test_df_to_filterbank_no_output(self, df_rand: callable):
        """Test for building .fil from dataframe, without output."""
        df = df_rand()

        with pytest.raises(OSError):
            df_to_filterbank(df)

    def test_df_to_filterbank_with_header(
        self, stream: callable, df_rand: callable
    ):
        """Test for building .fil from dataframe, with header."""
        outf = stream()
        header = dict({"MAGICN": 42})
        df = df_rand()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df_to_filterbank(df, header=header, outfile=outf)

        assert outf.tell() == 81964

    def test_df_to_filterbank_with_header_template(
        self, stream: callable, df_rand: callable
    ):
        """Test for building .fil from dataframe, with header."""
        outf = stream()
        header = iar_to_fil_header(iarpath)
        df = df_rand()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df_to_filterbank(df, header=header, outfile=outf)

        assert outf.tell() == 82297

    @pytest.mark.parametrize("data", [False, 0, 0.0, [0], (0, 0.0)])
    def test_df_to_filterbank_wrong_header(
        self, stream: callable, data: any, df_rand: callable
    ):
        """Test for building .fil from dataframe, with wrong header."""
        df = df_rand()
        outf = stream()

        with pytest.raises(TypeError):
            df_to_filterbank(df, header=data, outfile=outf)

    def test_raw_to_filterbank(self, stream: callable, df_and_buff: callable):
        """Test for building .fil from raw file."""
        outf = stream()
        _, rawstream = df_and_buff()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw_to_filterbank(rawstream, outfile=outf)

        assert outf.tell() == 81950
        assert files_utils.is_opened(outf)
