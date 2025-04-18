import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from evaluator import *


def test_basic_function_sum(capfd):
    """Test basic function definition and call."""
    prog = """
    fn giveSum(a, b){
        a+b;
    };
    displayl giveSum(40, 2);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "42" in captured.out


def test_parameter_same_name_as_global(capfd):
    """Test parameter with same name as global variable."""
    prog = """
    var x="hi";
    fn foo(x){
        x = x-1;
    };
    displayl foo(10);
    displayl x;
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert output[0] == "9"
    assert output[1] == "hi"


def test_inner_function_modifying_parameter(capfd):
    """Test inner function modifying parameter."""
    prog = """
    fn foo(x){
        fn bar(){
            x = x - 1;
        };
        bar() + x;
    };
    displayl foo(10);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "18" in captured.out


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
    }
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
        }
        multiply;
    }
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


def test_lexical_scoping_function_call(capfd):
    """Test lexical scoping in function calls."""
    prog = """
    var x = 9;
    fn bar() {
        x;
    };
    fn foo() {
        var x = 100;
        bar();
    };
    displayl foo();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "9" in captured.out


def test_nested_scoping_with_conditionals(capfd):
    """Test nested scoping with conditionals."""
    prog = """
    var x = 2;
    fn foo(){
        var x = 300;
        x;
    };
    fn bar(x){
        x += 1000;
        x;
    };
    fn baz(x){
        if x<5 then foo() else bar(x) end;
    };
    displayl baz(4);
    displayl baz(6);
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert output[0] == "300"
    assert output[1] == "1006"


def test_closure_with_shadowing(capfd):
    """Test closure with variable shadowing."""
    prog = """
    var x = 5;
    fn foo(){
        var x = 12;
        fn bar(){
            x;
        }
        bar;
    };
    var y = foo();
    displayl y();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "12" in captured.out


def test_nested_closure_with_function_parameter(capfd):
    """Test nested closure with function parameter."""
    prog = """
    fn foo(g){
        g() + 2;
    };
    fn baz(){
        var x = 100;
        fn bar(){
            x;
        }
        foo(bar);
    };
    displayl baz();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "102" in captured.out


def test_recursive_closure(capfd):
    """Test recursive closure."""
    prog = """
    var x = 100;
    fn foo(i){
        fn bar(){
            x+i;
        };
        if i==42 then bar else foo(i+1) end;
    };
    var y = foo(0);
    displayl y();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "142" in captured.out


def test_closure_reference_sharing(capfd):
    """Test that closures share reference to the same environment."""
    prog = """
    var k = 1000;
    fn foo(k){
        fn bar(){
            k = k-1;
            displayl k;
        };
        bar;
    };

    var y = foo(10);
    y();
    var r = y;
    r();
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert output[0] == "9"
    assert output[1] == "8"


def test_complex_recursion_with_function_parameter(capfd):
    """Test complex recursion with function parameter."""
    prog = """
    fn A(k, g){
        fn B(){
            k = k+5;
        };
        if k==0 then g() else A(k-1, B) + g() end;
    };
    fn five(){
        5;
    };
    displayl A(2, five);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "18" in captured.out


def test_man_or_boy(capfd):
    """Test Knuth's Man or Boy test with various k values."""
    prog = """
    fn A(k, x, y, z, w, v) {
        fn B() {
            k = k - 1;
            A(k, B, x, y, z, w);
        };
        
        if k <= 0 then w() + v() else B() end;
    };

    fn one() { 1; };
    fn negone() { 0-1; };
    fn zero() { 0; };

    displayl A(0, one, negone, negone, one, zero);
    displayl A(1, one, negone, negone, one, zero);
    displayl A(2, one, negone, negone, one, zero);
    displayl A(3, one, negone, negone, one, zero);
    displayl A(4, one, negone, negone, one, zero);
    """
    execute(prog)
    captured = capfd.readouterr()
    output = captured.out.strip().split("\n")
    assert len(output) == 5
    assert output[0] == "1"  # k=0
    assert output[1] == "0"  # k=1
    assert output[2] == "-2"  # k=2
    assert output[3] == "0"  # k=3
    assert output[4] == "1"  # k=4


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
