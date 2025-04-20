import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *
from pprint import pprint

code1="""
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

code2="""
    var limit = 4 * 10**6;
    var a = 1;
    var b= 2;
    var sum = 0;
    while (b < limit){
        if (b%2==0) then{
            sum+=b;
        }
        end;
        var temp = a + b;
        a = b;
        b = temp;
    };
    displayl sum;
"""
# Problem 3: Largest prime factor
code_3 = """
fn is_prime(n) {
    if n <= 1 then { False; } end;
    var i = 2;
    while (i * i <= n) {
        if (n % i == 0) then { False; } end;
        i += 1;
    };
    True;
}

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
displayl largest_prime_factor;
"""

# Problem 4: Largest palindrome product
code_4 = """
fn is_palindrome(n) {
    var reversed = 0;
    var original = n;
    while (n > 0) {
        reversed = reversed * 10 + n % 10;
        n /= 10;
    };
    original == reversed;
};

var largest_palindrome = 0;
var i = 999;
while (i >= 100) {
    var j = 999;
    while (j >= i) {
        var product = i * j;
        if (is_palindrome(product) and product > largest_palindrome) then {
            largest_palindrome = product;
        } end;
        j -= 1;
    };
    i -= 1;
};
displayl largest_palindrome;
"""

# Problem 5: Smallest multiple
code_5 = """
fn gcd(a, b) {
    while (b != 0) {
        var temp = b;
        b = a % b;
        a = temp;
    };
    a;
}

fn lcm(a, b) {
    (a * b) / gcd(a, b);
}

var result = 1;
var i = 1;
while (i <= 20) {
    result = lcm(result, i);
    i += 1;
};
displayl result;
"""

# Problem 6: Sum square difference
code_6 = """
var sum_of_squares = 0;
var square_of_sum = 0;
var i = 1;
while (i <= 100) {
    sum_of_squares += i * i;
    square_of_sum += i;
    i += 1;
};
square_of_sum *= square_of_sum;
displayl square_of_sum - sum_of_squares;
"""

# Problem 7: 10001st prime
code_7 = """
fn is_prime(n) {
    if n <= 1 then { false; } end;
    var i = 2;
    while (i * i <= n) {
        if (n % i == 0) then { false; } end;
        i += 1;
    };
    true;
}

var count = 0;
var num = 2;
while (count < 10001) {
    if (is_prime(num)) then {
        count += 1;
    } end;
    num += 1;
};
displayl num - 1;
"""

# Problem 8: Largest product in a series
code_8 = """
var series = "73167176531330624919225119674426574742355349194934";
var max_product = 0;
var i = 0;
while (i <= 1000 - 13) {
    var product = 1;
    var j = 0;
    while (j < 13) {
        product *= series[i + j] - '0';
        j += 1;
    };
    if (product > max_product) then {
        max_product = product;
    } end;
    i += 1;
};
displayl max_product;
"""

# Problem 9: Special Pythagorean triplet
code_9 = """
var a = 1;
while (a < 1000) {
    var b = a + 1;
    while (b < 1000 - a) {
        var c = 1000 - a - b;
        if (a * a + b * b == c * c) then {
            displayl a * b * c;
            break;
        } end;
        b += 1;
    };
    a += 1;
};
"""

# Problem 10: Summation of primes
code_10 = """
fn is_prime(n) {
    if n <= 1 then { false; } end;
    var i = 2;
    while (i * i <= n) {
        if (n % i == 0) then { false; } end;
        i += 1;
    };
    true;
}

var sum = 0;
var i = 2;
while (i < 2 * 10^6) {
    if (is_prime(i)) then {
        sum += i;
    } end;
    i += 1;
};
displayl sum;
"""

# Problem 11: Largest product in a grid
# This problem requires a 2D array, which is not directly supported in the given syntax. 
# Here's a simplified version using a 1D array:

code_11 = """
var grid = [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8];
var max_product = 0;
var i = 0;
while (i < 20 - 3) {
    var product = 1;
    var j = 0;
    while (j < 4) {
        product *= grid[i + j];
        j += 1;
    };
    if (product > max_product) then {
        max_product = product;
    } end;
    i += 1;
};
displayl max_product;
"""

# Problem 12: Highly divisible triangular number
code_12 = """
fn count_divisors(n) {
    var count = 0;
    var i = 1;
    while (i * i <= n) {
        if (n % i == 0) then {
            if (i * i == n) then {
                count += 1;
            } else {
                count += 2;
            } end;
        } end;
        i += 1;
    };
    count;
}

var triangle_num = 1;
var i = 2;
while (count_divisors(triangle_num) < 500) {
    triangle_num += i;
    i += 1;
};
displayl triangle_num;
"""

# Problem 13: Large sum
# This problem requires handling large numbers, which might not be directly supported in the given syntax.

# Problem 14: Longest Collatz sequence
code_14 = """
fn collatz_length(n) {
    var length = 1;
    while (n != 1) {
        if (n % 2 == 0) then {
            n /= 2;
        } else {
            n = 3 * n + 1;
        } end;
        length += 1;
    };
    length;
}

var max_length = 0;
var max_start = 0;
var i = 1;
while (i < 1000000) {
    var length = collatz_length(i);
    if (length > max_length) then {
        max_length = length;
        max_start = i;
    } end;
    i += 1;
};
displayl max_start;
"""

# Problem 15: Lattice paths
# This problem requires combinatorics, which might not be directly supported in the given syntax.

# Problem 16: Power digit sum
code_16 = """
var power = 2^1000;
var sum = 0;
while (power > 0) {
    sum += power % 10;
    power /= 10;
};
displayl sum;
"""

# Problem 17: Number letter counts
# This problem requires string manipulation, which might not be directly supported in the given syntax.

# Problem 18: Maximum path sum I
# This problem requires a 2D array, which is not directly supported in the given syntax.

# Problem 19: Counting Sundays
code_19 = """
var year = 1901;
var month = 1;
var day = 1;
var day_of_week = 1;  // 1 = Monday
var count = 0;
while (year < 2001) {
    if (day_of_week == 0 and day == 1) then {
        count += 1;
    } end;
    day += 1;
    if (day > 31) then {
        day = 1;
        month += 1;
        if (month > 12) then {
            month = 1;
            year += 1;
        } end;
    } end;
    day_of_week = (day_of_week + 1) % 7;
};
displayl count;
"""

# Problem 20: Factorial digit sum
code_20 = """
fn factorial(n) {
    if (n == 0 or n == 1) then { 1; } end;
    n * factorial(n - 1);
}

var fact = factorial(100);
var sum = 0;
while (fact > 0) {
    sum += fact % 10;
    fact /= 10;
};
displayl sum;
"""


prog="""
array a= ["meow","meow","nigga"];
displayl a[a.Length -2];
if a[0] == 1 then{
    displayl "True";
}
else{
    displayl "False";
}
end;

"""
pprint(parse(code_3))
execute(code_3)