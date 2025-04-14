import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from evaluator import *


def test_nested_function_recursion(capfd):
    """Test lexical scoping with nested functions and recursion."""
    prog = """
    fn foo(i){
        fn bar(){
            i;
        };
        fn baz(){
            bar();
        };
        if i==10 then baz() else foo(i+1) end;
    };
    displayl foo(0);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "10" in captured.out


def test_lexical_scope_shadowing(capfd):
    """Test that inner functions access variables from their lexical parent."""
    prog = """
    var x = 1000;
    fn foo() {
        fn bar() {
            x;
        }
        var x = 117;
        bar();
    }
    displayl foo();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "117" in captured.out


def test_function_as_parameter(capfd):
    """Test passing functions as parameters."""
    prog = """
    var x = 100;
    fn bar(){
        x;
    }
    fn foo(g){ 
        g() + 2;
    }
    displayl foo(bar);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "102" in captured.out


def test_function_returning_function(capfd):
    """Test returning and assigning functions."""
    prog = """
    fn foo(){
        fn bar(){
            x+2;
        }
        bar;
    }
    var x = 40;
    var y = foo();
    displayl y();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "42" in captured.out


def test_recursive_fibonacci(capfd):
    """Test standard recursive function."""
    prog = """
    fn fib(n){
        if n==1 or n==2 then 1 else fib(n-1) + fib(n-2) end;
    };
    displayl fib(10);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "55" in captured.out


def test_recursive_factorial(capfd):
    """Test recursive factorial function."""
    prog = """
    fn fact(n){
        if n <= 1 then 1 else n * fact(n-1) end;
    };
    displayl fact(5);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "120" in captured.out


def test_multiple_function_parameters(capfd):
    """Test functions with multiple parameters."""
    prog = """
    fn add(a, b, c) {
        a + b + c;
    }
    displayl add(10, 20, 30);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "60" in captured.out


def test_deeply_nested_function_access(capfd):
    """Test accessing variables through multiple nested scope layers."""
    prog = """
    fn outer(x) {
        fn middle(y) {
            fn inner(z) {
                x + y + z;
            }
            inner(30);
        }
        middle(20);
    }
    displayl outer(10);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "60" in captured.out


def test_parameter_shadowing(capfd):
    """Test parameter shadowing in nested functions."""
    prog = """
    fn outer(x) {
        fn inner(x) {
            x + 10;
        }
        inner(x * 2);
    }
    displayl outer(5);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "20" in captured.out


def test_recursive_sum(capfd):
    """Test recursive sum function."""
    prog = """
    fn sum(n) {
        if n <= 0 then 0 else n + sum(n-1) end;
    }
    displayl sum(5);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "15" in captured.out


def test_recursive_sum_with_helpers(capfd):
    """Test recursive function with helper functions."""
    prog = """
    fn sum_range(start, endd) {
        fn is_valid() {
            start <= endd;
        };
        
        if is_valid() then
            start + sum_range(start+1, endd)
        else
            0
        end;
    };
    displayl sum_range(1, 5);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "15" in captured.out


def test_higher_order_function(capfd):
    """Test higher-order function that creates function factories."""
    prog = """
    fn multiplier(factor) {
        fn multiply(n) {
            n * factor;
        };
        multiply;
    };
    var double = multiplier(2);
    var triple = multiplier(3);
    displayl double(5);
    displayl triple(5);
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert len(output) == 2
    assert output[0] == "10"
    assert output[1] == "15"


def test_function_array(capfd):
    """Test storing and calling functions from arrays."""
    prog = """
    fn add(a, b) {
        a + b;
    }
    fn subtract(a, b) {
        a - b;
    }
    fn multiply(a, b) {
        a * b;
    }
    var operations = [add, subtract, multiply];
    displayl operations[0](10, 5);
    displayl operations[1](10, 5);
    displayl operations[2](10, 5);
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert len(output) == 3
    assert output[0] == "15"
    assert output[1] == "5"
    assert output[2] == "50"


def test_function_capturing_local_state(capfd):
    """Test functions capturing local state."""
    prog = """
    fn counter() {
        var count = 0;
        fn increment() {
            count = count + 1;
            count;
        }
        increment;
    }
    var c = counter();
    displayl c();
    displayl c();
    displayl c();
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert len(output) == 3
    assert output[0] == "1"
    assert output[1] == "2"
    assert output[2] == "3"


def test_recursion_with_changing_scope(capfd):
    """Test recursion with scope variables changing each call."""
    prog = """
    fn count_down(n) {
        displayl n;
        if n > 0 then {
            var temp = n - 1;
            count_down(temp);
        } end;
    }
    count_down(3);
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert len(output) == 4
    assert output[0] == "3"
    assert output[1] == "2"
    assert output[2] == "1"
    assert output[3] == "0"


if __name__ == "__main__":
    # Simple test case for direct execution
    prog = """
    fn foo(i){
        fn bar(){
            i;
        };
        fn baz(){
            bar();
        };
        if i==10 then baz() else foo(i+1) end;
    };
    displayl foo(0);
    """
    execute(prog)
