import sys
import os
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from bytecode_eval_new import * 


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
    # Test with execute
    execute(f"displayl({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected
    
    # Test with run_program
    run_program(f"displayl({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected


@pytest.mark.parametrize("expression, expected", [
    ("abs(-5)", str(math.fabs(-5))),
    ("min([1, 2, 3])", str(min([1, 2, 3]))),
    ("max([1, 2, 3])", str(max([1, 2, 3]))),
    ("round(3.14159, 2)", str(round(3.14159, 2))),
    ("ceil(4.2)", str(math.ceil(4.2))),
    ("floor(4.8)", str(math.floor(4.8))),
    ("truncate(4.8)", str(math.trunc(4.8))),
    ("sqrt(16)", str(math.sqrt(16))),
    ("cbrt(27)", str(27 ** (1/3))),
    ("pow(2, 3)", str(math.pow(2, 3))),
    ("exp(1)", str(math.exp(1))),
    ("log(10)", str(math.log(10))),
    ("log10(100)", str(math.log10(100))),
    ("log2(8)", str(math.log2(8))),
    ("sin(0)", str(math.sin(0))),
    ("cos(0)", str(math.cos(0))),
    ("tan(0)", str(math.tan(0))),
    ("asin(1)", str(math.asin(1))),
    ("acos(1)", str(math.acos(1))),
    ("atan(1)", str(math.atan(1))),
    ("atan2(1, 1)", str(math.atan2(1, 1))),
    ("sinh(0)", str(math.sinh(0))),
    ("cosh(0)", str(math.cosh(0))),
    ("tanh(0)", str(math.tanh(0))),
    ("asinh(1)", str(math.asinh(1))),
    ("acosh(2)", str(math.acosh(2))),
    ("atanh(0.5)", str(math.atanh(0.5))),
    ("round(PI,10)", str(round(math.pi,10))),
    ("round(E,10)", str(round(math.e,10)))
])
def test_math_functions(expression, expected, capfd):
    # Test with execute
    execute(f"displayl({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected
    
    # # Test with run_program
    run_program(f"displayl({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected


@pytest.mark.parametrize("program, expected", [
    ("""
    var array nums = [1, 2, 3];
    var integer sum = 0;
    for (var i = 0; i < nums.Length; i += 1) {
        sum += nums[i];
    };
    display(sum + pow(2, 3));  /> Adding math.pow
    """, "14.0"),
    ("""
    var integer fact = 1;
    var integer n = 5;
    while (n > 0) {
        fact *= n;
        n -= 1;
    };
    display(fact + sqrt(16));  /> Adding math.sqrt
    """, "124.0"),
    ("""
    var array nums = [1.1, 2.2, 3.3];
    var integer sum = 0;
    repeat (nums.Length) {
        sum += integer(nums.PopFront);
    };
    display(sum + round(PI, 2));  /> Adding math.pi and round
    """, "9.14"),
    ("""
    var integer base = 2;
    var integer exponent = 3;
    var integer result = pow(base, exponent);
    display(result + log2(8));  /> Adding math.pow and math.log2
    """, "11.0"),
    ("""
    var integer angle = 0;
    var decimal result = sin(angle) + cos(angle) + tan(angle);
    display(round(result, 2));  /> Adding math.sin, math.cos, math.tan, and round
    """, "1.0")
])
def test_combined_cases(program, expected, capfd):
    # Test with execute
    execute(program)
    captured = capfd.readouterr()
    assert captured.out.strip() == expected
    
    # Test with run_program
    run_program(program)
    captured = capfd.readouterr()
    assert captured.out.strip() == expected

if __name__ == "__main__":
    pass