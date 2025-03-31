import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from pprint import pprint

@pytest.mark.parametrize("code, expected_output", [
    # Test 1: Basic assignment and reassignment
    ("""
    var a =[1,2,3,4];
    var b =20;
    a[1]=b;
    displayl a;
    displayl a[2];
    var c=[10,11,12,13];
    c[1]=a[2]+b;
    displayl c;
    """, "[1, 20, 3, 4]\n3\n[10, 23, 12, 13]"),
    
    # Test 2: Access first and last element
    ("""
    var a =[10, 20, 30, 40];
    displayl a[0];
    displayl a[3];
    """, "10\n40"),
    
    # Test 3: Modify using arithmetic operations
    ("""
    var a =[5, 10, 15, 20];
    a[2] = a[2] + a[1];
    a[8-6-1] = a[0] * a[3];
    displayl a;
    var b=[20,11];
    a=b;
    displayl a;
    """, "[5, 100, 25, 20]\n[20, 11]"),

])
def test_array_operations(code, expected_output, capfd):
    execute(code)
    captured = capfd.readouterr()
    assert captured.out.strip() == expected_output


@pytest.mark.parametrize("code, expected_output", [
    ("""
    var a = [1,2,3,4,5];
    a.PushFront(0);
    displayl a;
    a.PushBack(6);
    displayl a;
    displayl a.PopFront;
    displayl a[a.Length-1];
    displayl a;
    displayl a.PopBack;
    displayl a;
    displayl a.Length;
    a.Insert(3, 10);
    displayl a;
    a.Remove(1);
    displayl a;
    a.Clear;
    displayl a;
    displayl a.Length;
    """, 
    """[0, 1, 2, 3, 4, 5]
[0, 1, 2, 3, 4, 5, 6]
0
6
[1, 2, 3, 4, 5, 6]
6
[1, 2, 3, 4, 5]
5
[1, 2, 3, 10, 4, 5]
[1, 3, 10, 4, 5]
[]
0""")
])
def test_array_functions(code, expected_output, capfd):
    execute(code)
    captured = capfd.readouterr()
    assert captured.out.strip() == expected_output
