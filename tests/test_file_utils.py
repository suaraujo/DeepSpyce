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

from deepspyce import datasets
from deepspyce.utils.files_utils import (
    call_file_method,
    close_file,
    file_exists,
    get_file_attr,
    is_filelike,
    is_opened,
    is_readable,
    is_writable,
    open_file,
    read_file,
    write_to_file,
)

import pytest

# ============================================================================
# CONSTANTS
# ============================================================================

rawpath = datasets.PATH / "20201027_133329_test.raw"
iarpath = datasets.PATH / "J0437-4715_1_A1.iar"

# =============================================================================
# TESTS
# =============================================================================


def test_file_exists(wrong_path: str):

    assert file_exists(rawpath)
    assert not file_exists(wrong_path)


@pytest.mark.parametrize("data", [0.0, [0], (0, 0.0), {0: 0}])
def test_file_exists_wrong_input(data: any):

    with pytest.raises(TypeError):
        file_exists(data)


def test_open_file_read():
    with open_file(iarpath) as f:
        assert f.readable()
        assert not f.writable()

    assert f.closed


def test_open_file_append():
    with open_file(iarpath, mode="a") as f:
        assert not f.readable()
        assert f.writable()

    assert f.closed


def test_open_file_wrong_path(wrong_path: str):

    with pytest.raises(FileNotFoundError):
        open_file(wrong_path)


def test_open_file_no_overwrite():

    with pytest.raises(FileExistsError):
        open_file(rawpath, mode="w", overwrite=False)


def test_is_filelike(stream: callable):
    path = stream()

    assert is_filelike(path)


@pytest.mark.parametrize("data", [0.0, [0], (0, 0.0), {0: 0}])
def test_is_filelike_wrong_input(data: any):

    assert not is_filelike(data)


def test_get_file_attr(stream: callable):
    path = stream()

    assert not get_file_attr(path, "closed")


def test_get_file_attr_wrong_input():
    with pytest.raises(OSError):
        get_file_attr(1, "closed")


def test_get_file_attr_wrong_method(stream: callable):
    path = stream()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = get_file_attr(path, "closing")

    assert result is None


def test_call_file_method(stream: callable):
    path = stream()
    call_file_method(path, "close")

    assert path.closed


def test_call_file_method_wrong_input():

    with pytest.raises(OSError):
        call_file_method(1, "close")


def test_call_file_method_wrong_method(stream: callable):
    path = stream()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = call_file_method(path, "closing")

    assert not path.closed
    assert result is None


def test_is_opened(stream: callable):
    path = stream()

    assert is_opened(path)
    path.close()
    assert not is_opened(path)


def test_is_readable():
    with open_file(iarpath, mode="r") as f:

        assert is_readable(f)
    with open_file(iarpath, mode="a") as f:

        assert not is_readable(f)


def test_is_writable():
    with open_file(iarpath, mode="r") as f:

        assert not is_writable(f)
    with open_file(iarpath, mode="a") as f:

        assert is_writable(f)


def test_close_file(stream: callable):
    path = stream()

    assert not path.closed
    close_file(path)
    assert path.closed


def test_read_file():
    f = read_file(iarpath)

    assert isinstance(f, str)
    assert f[:10] == "Source Nam"
    assert f[-10:] == "s,1\nCal,0\n"


def test_read_file_wrong_uft8():
    with pytest.raises(UnicodeDecodeError):
        read_file(rawpath)


def test_read_file_bin():
    f = read_file(rawpath, "rb")

    assert isinstance(f, bytes)
    assert f[:10] == b"\x00\x00\x00\x00\x00\x00\xc0:\x00\x00"
    assert f[-10:] == b"\xd3\xee\x00\x00\x00\x00\x00\x00\x00\x00"


def test_write_to_file(stream: callable):
    path = stream()
    ptr = path.tell()
    write_to_file(path, b"42")

    assert path.tell() == ptr + 2


def test_write_to_file_none(stream: callable):
    path = stream()
    ptr = path.tell()
    write_to_file(path)

    assert path.tell() == ptr
