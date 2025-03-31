import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *


@pytest.mark.parametrize("expression, expected", [
    ("2 + 3", "5"),
    ("10 - 4", "6"),
    ("5 * 6", "30"),
    ("20 / 4", "5.0"),
    ("(5 + 3) * 2 - 4 / 2", "14.0"),
    ("-5 + 2", "-3"),
    ("3 * (4 + 2) / 3 - 1", "5.0"),
    ("3 + 2 * 4", "11"),
    ("-6 / 2", "-3.0")
])
def test_arithmetic_operations(expression, expected, capfd):
    execute(f"display({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected