import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from bytecode_eval_new import * 
from pprint import pprint

def test_euler_test_1(capfd):
    prog = """
    var x=999;
    var res=0;
    while (x>0){
        if (x%3==0 or x%5==0)
        then
        {
            /~ displayl x; ~/
            res+=x;
        }
        else{
            /~ displayl "Not divisible by 3 or 5"; ~/
        }
        end;
        x-=1;
    };
    displayl res;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "233168" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "233168" in captured.out

def test_euler_test_2(capfd):
    prog = """
    fn compute() {
    var ans = 0;
    var x = 1;  /> Represents the current Fibonacci number being processed
    var y = 2;  /> Represents the next Fibonacci number in the sequence
    
    while (x <= 4000000) {
        if x % 2 == 0 then
            ans += x;
        end;
        
        var temp = y;
        y = x + y;
        x = temp;
    };
    
    string(ans);
    };

    displayl compute();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "4613732" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "4613732" in captured.out

def test_euler_test_3(capfd):
    prog = """
    fn is_prime(n) {
        if n <= 1 then { False; } end;
        var i = 2;
        while (i * i <= n) {
            if (n % i == 0) then { False; } end;
            i += 1;
        };
        True;
    };

    var n = 600851475143;
    var largest_prime_factor = 1;
    var i = 2;
    while (i * i <= n) {
        if (n % i == 0) then {
            if (is_prime(i)) then {
                largest_prime_factor = i;
            } end;
            n /= i;
        } else {
            i += 1;
        } end;
    };
    if (n > 1) then {
        largest_prime_factor = n;
    } end;
    displayl floor(largest_prime_factor);
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "6857" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "6857" in captured.out

def test_euler_test_4(capfd):
    prog = """
    var res=0;
    for (var i=100; i<=1000; i+=1){
        for (var j=100; j<=1000; j+=1){
            var string b= string(i*j);
            var string c= b.Slice(None,None,-1);
            var d = if b==c then i * j else 0 end;
            res=max([res,d]);
        }
    };
    displayl res;
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "906609" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "906609" in captured.out
def test_euler_test_5(capfd):
    prog = """
    fn gcd(a, b) {
        if b == 0 then a else gcd(b, a % b) end;
    };

    fn lcm(a, b) {
        (a / gcd(a, b)) * b;
    };

    fn lcm_range(start, ending) {
        var result = 1;
        for (var i = start; i <= ending; i += 1) {
            result = lcm(result, i);
        };
        result;
    };

    fn compute() {
        var ans = lcm_range(1, 20);
        string(ans);
    };

    displayl compute();
    """
    execute(prog)
    captured = capfd.readouterr()
    assert "232792560" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "232792560" in captured.out
