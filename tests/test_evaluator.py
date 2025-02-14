from dataclasses import dataclass
from src.evaluator import e
from src.parser import parse
from src.context import Context

context = Context()

def test_while_loop():
    code = """
    var integer x = 0;
    while x < 5 do
        x = x + 1;
    end
    display x;
    """
    parsed_code = parse(code)
    result = e(parsed_code)
    assert result == 5, f"Expected 5, but got {result}"

def test_while_loop_with_condition():
    code = """
    var integer y = 10;
    while y > 0 do
        y = y - 2;
    end
    display y;
    """
    parsed_code = parse(code)
    result = e(parsed_code)
    assert result == 0, f"Expected 0, but got {result}"

def test_while_loop_with_nested_statements():
    code = """
    var integer z = 0;
    while z < 3 do
        z = z + 1;
        display z;
    end
    """
    parsed_code = parse(code)
    result = e(parsed_code)
    assert result is None  # display returns None

def test_while_loop_with_no_iterations():
    code = """
    var integer a = 5;
    while a < 5 do
        a = a + 1;
    end
    display a;
    """
    parsed_code = parse(code)
    result = e(parsed_code)
    assert result == 5, f"Expected 5, but got {result}"