import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

import pytest
from encryption_tool import (
    caesar_encrypt, caesar_decrypt,
    xor_encrypt, xor_decrypt,
    aes_encrypt, aes_decrypt,
)


# ── Caesar ──────────────────────────────────────────────────────────────────

def test_caesar_encrypt_basic():
    assert caesar_encrypt("ABC", 1) == "BCD"


def test_caesar_decrypt_basic():
    assert caesar_decrypt("BCD", 1) == "ABC"


def test_caesar_roundtrip():
    plaintext = "Hello World"
    assert caesar_decrypt(caesar_encrypt(plaintext, 13), 13) == plaintext


def test_caesar_wraparound():
    assert caesar_encrypt("Z", 1) == "A"
    assert caesar_encrypt("z", 1) == "a"


def test_caesar_preserves_non_alpha():
    assert caesar_encrypt("Hello, World! 123", 5) == "Mjqqt, Btwqi! 123"


def test_caesar_zero_shift():
    assert caesar_encrypt("No change", 0) == "No change"


# ── XOR ─────────────────────────────────────────────────────────────────────

def test_xor_encrypt_returns_hex():
    result = xor_encrypt("hello", "key")
    assert all(c in "0123456789abcdef" for c in result)


def test_xor_roundtrip():
    plaintext = "Secret message!"
    key = "mykey"
    assert xor_decrypt(xor_encrypt(plaintext, key), key) == plaintext


def test_xor_different_keys_give_different_ciphertext():
    enc1 = xor_encrypt("hello", "key1")
    enc2 = xor_encrypt("hello", "key2")
    assert enc1 != enc2


def test_xor_empty_string():
    assert xor_decrypt(xor_encrypt("", "key"), "key") == ""


# ── AES ─────────────────────────────────────────────────────────────────────

def test_aes_roundtrip():
    plaintext = "This is a secret"
    key = "mypassword"
    assert aes_decrypt(aes_encrypt(plaintext, key), key) == plaintext


def test_aes_different_encryptions_differ():
    # AES CBC uses random IV, so two encryptions of the same plaintext differ
    enc1 = aes_encrypt("hello", "key")
    enc2 = aes_encrypt("hello", "key")
    assert enc1 != enc2


def test_aes_short_key_padded():
    # Key shorter than 16 bytes should still work (padded internally)
    plaintext = "Padded key test"
    assert aes_decrypt(aes_encrypt(plaintext, "short"), "short") == plaintext


def test_aes_long_key_truncated():
    # Key longer than 16 bytes should still work (truncated internally)
    plaintext = "Truncated key test"
    long_key = "this_is_a_very_long_key_that_exceeds_16_bytes"
    assert aes_decrypt(aes_encrypt(plaintext, long_key), long_key) == plaintext


def test_aes_empty_string():
    assert aes_decrypt(aes_encrypt("", "key"), "key") == ""
