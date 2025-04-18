import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from bytecode_eval_new import * 

@pytest.mark.parametrize("expression, expected", [
    ("if 5 < 10 then 1 else 0 end", "1"),
    ("if 5 < 10 then if 2 < 3 then 1 else 0 end else 0 end", "1"),
    ("if 0 < 1 then 1 else 0 end", "1"),
    ("if 2 < 3 then if 4 > 5 then 0 else 1 end else 2 end", "1"),
    ("if 5 == 5 then 10 end", "10")
])
def test_conditional_expressions(expression, expected, capfd):
    execute(f"display({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected

    run_program(f"display({expression})")
    captured = capfd.readouterr()
    assert captured.out.strip() == expected

def test_for_loop_sum(capfd):
    code2 = """
    var integer sum=0;
    for (var i=1;i<10;i+=1){
        sum+=i;
    };
    displayl sum;
    display "done";
    """
    execute(code2)
    captured = capfd.readouterr()
    assert "45" in captured.out
    assert "done" in captured.out

    run_program(code2)
    captured = capfd.readouterr()
    assert "45" in captured.out
    assert "done" in captured.out

def test_loop_function(capfd):
    prog = """fn loopFunction(n) {
        var i = 0;
        while (i < n) {
            displayl(i);
            i = i + 1;
        };
    };
    var x = 5;
    displayl("Calling loopFunction with x=5");
    loopFunction(x); 
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "Calling loopFunction with x=5" in captured.out
    assert captured.out.strip().endswith("0\n1\n2\n3\n4")

    run_program(prog)
    captured = capfd.readouterr()
    assert "Calling loopFunction with x=5" in captured.out
    assert captured.out.strip().endswith("0\n1\n2\n3\n4")

def test_char_ascii_operations(capfd):
    prog = """var a= char (66);
    displayl a;
    var b= ascii("A");
    displayl b;
    var c= char (ascii('x') + ascii (char(1)));
    displayl c;"""
    execute(prog)
    captured = capfd.readouterr()
    assert "B" in captured.out
    assert "65" in captured.out
    assert "y" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "B" in captured.out
    assert "65" in captured.out
    assert "y" in captured.out

def test_conditional_execution_1(capfd):
    prog = """var x = 10;
    displayl if x > 5 then 
                { 
                    if x > 8 
                    then 
                        displayl "greater than 8"; end; 
                } 
            else { 
                displayl "less than 5";
                displayl "not greater than 5";
             } end;"""
    execute(prog)
    captured = capfd.readouterr()
    assert "greater than 8" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "greater than 8" in captured.out
    
def test_while_loop_divisibility(capfd):
    prog = """
    var x=1000;
    while (x>0){
        if (x%3==0 or x%5==0)
        then
        {
            displayl x;
        }
        else{
            displayl "Not divisible by 3 or 5";
        }
        end;
        x=x-1;
    };
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "1000" in captured.out
    assert "999" in captured.out
    assert "Not divisible by 3 or 5" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "1000" in captured.out
    assert "999" in captured.out
    assert "Not divisible by 3 or 5" in captured.out

def test_function_return_value(capfd):
    prog = """
    fn foo() {
        if 2==2 then {
            42; 
        }
        else {

        } end;
    };
    displayl foo();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "42" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "42" in captured.out

def test_variable_scope_in_loop(capfd):
    prog = """
    var u = 100;
    for(var u=0; u<3; u+=1){
        var b = 2;
        displayl b;
    }
    displayl 179;
    displayl u;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "2" in captured.out
    assert "179" in captured.out
    assert "100" in captured.out

    # run_program(prog)
    # captured = capfd.readouterr()
    # assert "2" in captured.out
    # assert "179" in captured.out
    # assert "100" in captured.out

def test_fibonacci_function(capfd):
    prog = """
    displayl "Fibonacci:";

    fn fib(a) {
        if (a==1 or a==2) then 1 else fib(a-1) + fib(a-2) end;
    };
    displayl "----";
    var x = 20;
    displayl x;
    displayl fib(x);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "Fibonacci:" in captured.out
    assert "20" in captured.out
    assert "6765" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "Fibonacci:" in captured.out
    assert "20" in captured.out
    assert "6765" in captured.out

def test_conditional_execution_2(capfd):
    prog = """var x = 0;
    displayl if x > 5 then 
                { 
                    if x > 8 
                    then 
                        displayl "greater than 8"; end; 
                } 
            else { 
                displayl "less than 5";
                displayl "not greater than 5";
             } end;"""
    execute(prog)
    captured = capfd.readouterr()
    assert "less than 5" in captured.out
    assert "not greater than 5" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "less than 5" in captured.out
    assert "not greater than 5" in captured.out

@pytest.mark.parametrize("input_value, expected_output", [
        ("42", "42"),  # Integer input
        ("3.14", "3.14"),  # Float input
        ("Hello, World!", "Hello, World!"),  # String input
        ("", ""),  # Empty input
        ("true", "true"),  # Boolean-like string input
        ("null", "null"),  # Null-like string input
        ("special_chars!@#$%^&*()", "special_chars!@#$%^&*()"),  # Special characters
        ("123abc", "123abc"),  # Alphanumeric input
        ("   spaced input   ", "   spaced input   "),  # Input with leading/trailing spaces
        ("'quoted'", "'quoted'"),  # Quoted string input
    ])
def test_feed_input_handling(input_value, expected_output, monkeypatch, capfd):
    prog = """
    var a = feed("Enter input:");
    displayl a;
    """
    # Mock the input function to simulate user input
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    execute(prog)
    captured = capfd.readouterr()
    assert expected_output in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert expected_output in captured.out

def test_array_and_hash_operations(capfd):
    prog = """
    var arr = [1, 2, 3];
    var hash = {"key1": 10, "key2": 20};

    arr.PushBack(4);
    hash.Add("key3", 30);

    displayl ("array display:");
    for (var integer i = 0; i < arr.Length; i = i + 1) {
        displayl arr[i];
    }
    fn multiply(a, b) {
        a * b;
    };
    displayl multiply(hash["key1"], 2);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "array display:" in captured.out
    assert "1" in captured.out
    assert "2" in captured.out
    assert "3" in captured.out
    assert "4" in captured.out
    assert "20" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "array display:" in captured.out
    assert "1" in captured.out
    assert "2" in captured.out
    assert "3" in captured.out
    assert "4" in captured.out
    assert "20" in captured.out

def test_conditional_and_loop_execution(capfd):
    prog = """
    var x = 10;

    if x > 5 then {
        displayl "x is greater than 5";
    } else {
        displayl "x is 5 or less";
    } end;

    while (x > 0) {
        displayl x;
        x = x - 1;
    }
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "x is greater than 5" in captured.out
    assert "10" in captured.out
    assert "9" in captured.out
    assert "8" in captured.out
    assert "7" in captured.out
    assert "6" in captured.out
    assert "5" in captured.out
    assert "4" in captured.out
    assert "3" in captured.out
    assert "2" in captured.out
    assert "1" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "x is greater than 5" in captured.out
    assert "10" in captured.out
    assert "9" in captured.out
    assert "8" in captured.out
    assert "7" in captured.out
    assert "6" in captured.out
    assert "5" in captured.out
    assert "4" in captured.out
    assert "3" in captured.out
    assert "2" in captured.out
    assert "1" in captured.out

def test_function_multiply(capfd):
    prog = """
    fn multiply(a, b) {
        a * b;
    };

    var result = multiply(5, 4);
    displayl result;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "20" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "20" in captured.out

def test_repeat_loop_with_array(capfd):
    prog = """
    var array h = [1, 2, 3];
    var sum = 0;
    repeat (h.Length) {
        sum += h.PopFront;
    }
    displayl sum;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "6" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "6" in captured.out

def test_repeat_loop_fixed_iterations(capfd):
    prog = """
    repeat (10) {
        displayl 1;
    }
    """
    execute(prog)
    captured = capfd.readouterr()
    assert captured.out.strip().count("1") == 10

    run_program(prog)
    captured = capfd.readouterr()
    assert captured.out.strip().count("1") == 10

def test_repeat_loop_with_function_calls(capfd):
    prog = """
    fn increment(x) {
        x + 1;
    };
    var sum = 0;
    repeat (5) {
        sum = increment(sum);
    }
    displayl sum;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "5" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "5" in captured.out

@pytest.mark.parametrize("prog, expected", [
    ("""
    fn factorial(n) {
        if n == 0 then 1 else n * factorial(n - 1) end;
    };
    displayl factorial(5);
    """, "120"),
    ("""
    fn gcd(a, b) {
        if b == 0 then a else gcd(b, a % b) end;
    };
    displayl gcd(48, 18);
    """, "6"),
    ("""
    fn power(base, expp) {
        if expp == 0 then 1 else base * power(base, expp - 1) end;
    };
    displayl power(2, 10);
    """, "1024"),
    ("""
    fn sum_of_digits(n) {
        if n <= 0 then 0 else (n % 10) + sum_of_digits(floor(n / 10)) end;
    };
    displayl sum_of_digits(1234);
    """, "10"),
    ("""
    fn fibonacci(n) {
        if n == 1 or n == 2 then 1 else fibonacci(n - 1) + fibonacci(n - 2) end;
    };
    displayl fibonacci(7);
    """, "13")
])
def test_recursive_functions(prog, expected, capfd):
    execute(prog)
    captured = capfd.readouterr()
    assert expected in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert expected in captured.out

 
def test_for_loop_with_comment_block(capfd):
    prog = """
    var integer sum=0;
    for (var i=1;i<10;i+=1){
        sum+=i;
    }; 
    var i=1;
    /~i= i+ sum;
    displayl i;~/
    displayl sum;
    display "done";
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "45" in captured.out
    assert "done" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "45" in captured.out
    assert "done" in captured.out

# def test_nested_for_while_repeat(capfd):
#     prog = """
#     var sum = 0;
#     for (var i = 0; i < 3; i += 1) {
#         var j = 0;
#         while (j < 2) {
#             repeat (2) {
#                 sum += i + j;
#             }
#             j += 1;
#         }
#     }
#     displayl sum;
#     """
#     execute(prog)
#     captured = capfd.readouterr()
#     assert "18" in captured.out

#     # run_program(prog)
#     # captured = capfd.readouterr()
#     # assert "18" in captured.out

# def test_nested_if_else_with_loops(capfd):
#     prog = """
#     var x = 5;
#     if x > 3 then {
#         for (var i = 0; i < 2; i += 1) {
#             if i == 1 then {
#                 displayl "Inside nested if";
#             } else {
#                 displayl "Inside else";
#             } end;
#         }
#     } else {
#         displayl "Outer else";
#     } end;
#     """
#     execute(prog)
#     captured = capfd.readouterr()
#     assert "Inside nested if" in captured.out
#     assert "Inside else" in captured.out

#     # run_program(prog)
#     # captured = capfd.readouterr()
#     # assert "Inside nested if" in captured.out
#     # assert "Inside else" in captured.out

# def test_random_mixed_loops_and_conditions(capfd):
#     prog = """
#     var total = 0;
#     for (var i = 0; i < 3; i += 1) {
#         if (i % 2 == 0 ) then {
#             var j = 0;
#             while (j < 2) {
#                 repeat (2) {
#                     total += i + j;
#                 }
#                 j += 1;
#             }
#         } else {
#             displayl "Odd index";
#         } end;
#     }
#     displayl total;
#     """
#     execute(prog)
#     captured = capfd.readouterr()
#     assert "12" in captured.out
#     assert "Odd index" in captured.out

#     # run_program(prog)
#     # captured = capfd.readouterr()
#     # assert "12" in captured.out
#     # assert "Odd index" in captured.out

# def test_nested_functions_with_loops_and_conditions(capfd):
#     prog = """
#     fn outerFunction(x) {
#         fn innerFunction(y) {
#             if y > 0 then {
#                 var sum = 0;
#                 for (var i = 0; i < y; i += 1) {
#                     sum += i;
#                 }
#                 sum;
#             } else {
#                 0;
#             } end;
#         };
#         innerFunction(x);
#     };
#     displayl outerFunction(5);
#     """
#     execute(prog)
#     captured = capfd.readouterr()
#     assert "10" in captured.out

#     # run_program(prog)
#     # captured = capfd.readouterr()
#     # assert "10" in captured.out

if __name__ =="__main__":
    prog="""
    var integer sum=2;
    for (var i=1;i<10;i+=1){
        sum+=i;
    }; 
    var i=1;
    /~i= i+ sum;
    displayl i;~/
    displayl sum;
    display "done";
"""

    
    # pprint(list(lex(prog)))
    pprint(parse(prog))
    execute(prog)

