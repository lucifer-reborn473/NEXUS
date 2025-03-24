import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from pprint import pprint

@pytest.mark.parametrize("code, expected_output", [
    # Test 1: Basic assignment and reassignment
    ("""
    array a =[1,2,3,4];
    var b =20;
    a[1]=b;
    displayl a;
    displayl a[2];
    array c=[10,11,12,13];
    c[1]=a[2]+b;
    displayl c;
    """, "[1, 20, 3, 4]\n3\n[10, 23, 12, 13]"),
    
    # Test 2: Access first and last element
    ("""
    array a =[10, 20, 30, 40];
    displayl a[0];
    displayl a[3];
    """, "10\n40"),
    
    # Test 3: Modify using arithmetic operations
    ("""
    array a =[5, 10, 15, 20];
    a[2] = a[2] + a[1];
    a[8-6-1] = a[0] * a[3];
    displayl a;
    """, "[5, 100, 25, 20]")

])
def test_array_operations(code, expected_output, capfd):
    execute(code)
    captured = capfd.readouterr()
    assert captured.out.strip() == expected_output
