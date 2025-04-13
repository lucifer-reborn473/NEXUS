import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from pprint import pprint


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

    # Test format string with variable substitution
    ("""
    var a = 5;
    var b = `This is a: {a}`;
    display `This is b: {b}`;
    """, "This is b: This is a: 5"),

    # Test format string with multiple variables
    ("""
    var x = 10;
    var y = 20;
    var z = `x: {x}, y: {y}`;
    display z;
    """, "x: 10, y: 20"),

    # Test format string with expression evaluation
    ("""
    var num = 7;
    var sqnum= num*num;
    var result = `Square of {num} is {sqnum} `;
    display result;
    """, "Square of 7 is 49"),

    # Test format string with nested format strings
    ("""
    var inner = `Inner value`;
    var outer = `Outer contains: {inner}`;
    display outer;
    """, "Outer contains: Inner value"),

    # Test simple typecast
    ("""
    var decimal x = 10.34;
    var integer y = 10;
    displayl (string(x) + "dip" + (string(y)));
    displayl (integer(x) + y);
    """, "10.34dip10\n20"),

    # Test nested typecast
    ("""
    var decimal x = 15.67;
    var string result = string(integer(x));
    displayl result;
    """, "15"),

    # Test typecast within loop
    ("""
    var array nums = [1.1, 2.2, 3.3];
    var integer sum = 0;
    for (var i=0; i<3; i+=1) {
        sum = sum + integer(nums[i]);
    };
    displayl sum;
    """, "6"),

    # Test error in typecast
    ("""
    var string invalid = "not_a_number";
    displayl integer(invalid);
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