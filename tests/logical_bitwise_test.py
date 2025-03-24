import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *


@pytest.mark.parametrize("expression, expected", [
    ("3 < 5 and 4 > 2", "True"),
    ("5 > 10 or 2 < 3", "True"),
    ("not 4 > 3", "False"),
    ("3 == 3 and 4 != 2", "True"),
    ("5 <= 10 or 8 >= 20", "True"),
    ("not (4 > 5 and 3 < 1)", "True"),
    ("3 == 3 and 4 == 4", "True"),
    ("5 < 2 or 7 > 10", "False")
])
def test_logical_operations(expression, expected, capfd):
    execute(f"display({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected


@pytest.mark.parametrize("expression, expected", [
    ("3 & 1", "1"),
    ("3 | 1", "3"),
    ("3 ^ 1", "2"),
    ("~5", "-6"),
    ("5 << 2", "20"),
    ("8 >> 2", "2"),
    ("1024 & 512", "0"),
    ("-5 << 2", "-20"),
    ("-5 >> 2", "-2")
])
def test_bitwise_operations(expression, expected, capfd):
    execute(f"display({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected