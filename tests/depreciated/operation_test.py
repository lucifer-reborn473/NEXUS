import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *


def test_is_even_false(capfd):
    prog = """var a = 112911;
    var isEven = if a%2==0 then True else False end;
    displayl isEven;"""
    
    execute(prog)
    
    captured = capfd.readouterr()
    assert "False" in captured.out
    print("test passed")

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




# def test_edge_cases():
#     with pytest.raises(ZeroDivisionError):
#         e("5 / 0")  # Division by zero
#     with pytest.raises(TypeError):
#         e("3 + 'a'")  # Invalid operation
#     assert e("9999999 * 1234567") == 12345668765433  # Large numbers
#     assert e("0.0001 * 0.0002") == 2e-08  # Small numbers
#     assert e("1 << 1024") > 0  # Extremely large shift
#     assert e("5 == 5 and 'a' == 'a'") == True

if __name__=="__main__":
    prog="display ~5;"
    execute(prog)
    print(list(lex(prog)))
    print(parse(prog))