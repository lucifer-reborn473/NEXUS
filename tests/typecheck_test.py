import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from pprint import pprint


import pytest
from evaluator import execute

@pytest.mark.parametrize("code, expected_output", [
    # Test integer type
    ("""
    var integer x = 10;
    displayl x;
    """, "10"),
    
    # Test decimal type
    ("""
    var decimal y = 3.14;
    displayl y;
    """, "3.14"),
    
    # Test uinteger type (non-negative integer)
    ("""
    var uinteger z = 5;
    displayl z;
    """, "5"),
    
    # Test uinteger type with negative value (should raise error)
    ("""
    var uinteger z = -5;
    displayl z;
    """, "5"),
    
    # Test string type
    ("""
    var string s = "Hello, World!";
    displayl s;
    """, "Hello, World!"),
    
    # Test array type
    ("""
    var array arr = [1, 2, 3];
    displayl arr;
    """, "[1, 2, 3]"),
    
    # Test array type with invalid value (should raise error)
    ("""
    var array arr = "not an array";
    displayl arr;
    """, ValueError),
    
    # Test Hash type
    ("""
    var Hash h = {"key": "value"};
    displayl h;
    """, "{'key': 'value'}"),
    
    # Test Hash type with invalid value (should raise error)
    ("""
    var Hash h = [1, 2, 3];
    displayl h;
    """, ValueError),
    
    # Test boolean type
    ("""
    var boolean b = True;
    displayl b;
    """, "True"),
    
    # Test boolean type with implicit casting
    ("""
    var boolean b = 0;
    displayl b;
    """, "False"),
    
    # Test no type specified
    ("""
    var x = 42;
    displayl x;
    """, "42"),
    
    # Test unknown type (should raise error)
    ("""
    var array u = 10;
    displayl u;
    """, ValueError),
])
def test_var_type_declarations(code, expected_output, capfd):
    try:
        execute(code)
        captured = capfd.readouterr()
        assert captured.out.strip() == expected_output
    except Exception as e:
        assert isinstance(e, expected_output)

if __name__ == "__main__":
    prog="""var Hash h = [1, 2, 3];
    displayl h;"""
    execute(prog)