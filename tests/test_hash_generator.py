import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

import hashlib
import pytest
from hash_generator import generate_hash


def test_generate_hash_returns_all_algorithms():
    result = generate_hash("hello")
    assert "MD5" in result
    assert "SHA1" in result
    assert "SHA256" in result


def test_md5_correctness():
    result = generate_hash("hello")
    expected = hashlib.md5("hello".encode()).hexdigest()
    assert result["MD5"] == expected


def test_sha1_correctness():
    result = generate_hash("hello")
    expected = hashlib.sha1("hello".encode()).hexdigest()
    assert result["SHA1"] == expected


def test_sha256_correctness():
    result = generate_hash("hello")
    expected = hashlib.sha256("hello".encode()).hexdigest()
    assert result["SHA256"] == expected


def test_empty_string():
    result = generate_hash("")
    assert result["MD5"] == hashlib.md5(b"").hexdigest()
    assert result["SHA256"] == hashlib.sha256(b"").hexdigest()


def test_different_inputs_give_different_hashes():
    r1 = generate_hash("foo")
    r2 = generate_hash("bar")
    assert r1["SHA256"] != r2["SHA256"]
