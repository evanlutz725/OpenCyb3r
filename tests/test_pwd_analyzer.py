import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

import pytest
from pwd_analyzer import check_password_strength


def test_weak_password():
    # short, lowercase only -> scores 1 (lowercase criterion only)
    assert check_password_strength("abc") == 1


def test_only_length():
    assert check_password_strength("abcdefghijklmno") == 2  # length + lowercase


def test_moderate_password():
    score = check_password_strength("Abcdefgh1")
    assert 2 <= score <= 4


def test_strong_password():
    score = check_password_strength("Str0ng!Pass#2024")
    assert score == 5


def test_all_criteria():
    # >= 12 chars, upper, lower, number, special
    score = check_password_strength("Hello@World1!")
    assert score == 5


def test_missing_special_char():
    score = check_password_strength("HelloWorld123")
    assert score == 4  # length + upper + lower + number, no special


def test_missing_number():
    score = check_password_strength("Hello@World!!")
    assert score == 4  # length + upper + lower + special, no number


def test_score_range():
    for pwd in ["a", "Abc123!", "Abcdefghij1@"]:
        score = check_password_strength(pwd)
        assert 0 <= score <= 5
