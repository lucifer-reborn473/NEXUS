from bytecode_eval_new import *
program = """
fn second_largest(arr) {
    var newarr = sort(arr);
    var n = newarr.Length;
    newarr[n-2];
};
var myArray = [12, 35, 1, 10, 34, 1, 78, 56, 23, 89];
var myArray2 = [35, 12, 1, 78, 34, 56, 89, 10, 23, 1, 47, 19, 50, 8, 29, 3, 41, 22, 6, 37, 25, 9, 31, 4, 44, 2, 40, 7, 36, 5, 48, 11, 38, 15, 42, 13, 45, 18, 39, 14, 46, 16, 43, 17, 49, 20, 33, 21, 32, 30];
var myArray3 = [12, 87, 45, 23, 78, 56, 34, 90, 11, 67, 43, 29, 88, 54, 32, 76, 21, 98, 65, 39, 84, 57, 31, 72, 19, 93, 48, 26, 81, 59, 37, 74, 22, 95, 41, 28, 86, 53, 30, 77, 18, 92, 46, 25, 83, 61, 33, 70, 20, 96, 44, 27, 85, 52, 36, 79, 17, 91, 49, 24, 82, 60, 38, 73, 15, 94, 42, 21, 87, 50, 35, 80, 16, 89, 47, 23, 84, 58, 34, 71, 19, 97, 40, 29, 88, 55, 32, 75, 18, 90, 45, 26, 83, 62, 37, 78, 14, 93, 48, 22];
displayl(second_largest(myArray));
displayl(second_largest(myArray2));
displayl(second_largest(myArray3));
"""

program = """
fn longest_palindromic_subsequence(arr) {
    var n = arr.Length;
    var dp = [];
    for (var i = 0; i < n; i += 1) {
        var row = [];
        for (var j = 0; j < n; j += 1) {
            row.PushBack(0);
        };
        dp.PushBack(row);
    };

    for (var i = 0; i < n; i += 1) {
        dp[i][i] = 1; /> Every single element is a palindrome of length 1
    };

    
    for (var lengt = 2; lengt <= n; lengt += 1) {
        for (var i = 0; i <= n - lengt; i += 1) {
            var j = i + lengt - 1;
            if arr[i] == arr[j] then
                dp[i][j] = dp[i + 1][j - 1] + 2;
            else
                dp[i][j] = max([dp[i + 1][j], dp[i][j - 1]]);
            end;
        };
    };

    dp[0][n - 1]; /> Return the length of the longest palindromic subsequence
};

var myArray = [1, 2, 3, 2, 1, 4, 1, 2, 3, 2, 1];
displayl "Longest Palindromic Subsequence Length: " + string(longest_palindromic_subsequence(myArray));
var medarr= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1];
displayl "Longest Palindromic Subsequence Length: " + string(longest_palindromic_subsequence(medarr));
var longarr = [
    3, 7, 1, 4, 8, 2, 9, 6, 5, 0,
    3, 1, 7, 2, 8, 4, 6, 0, 9, 5,
    1, 3, 2, 7, 4, 8, 5, 0, 6, 9,
    2, 4, 1, 3, 7, 5, 8, 0, 9, 6,
    7, 3, 1, 2, 6, 9, 0, 8, 4, 5,
    5, 4, 8, 0, 9, 6, 2, 1, 3, 7,
    6, 9, 0, 5, 8, 3, 1, 2, 4, 7,
    9, 6, 5, 8, 0, 1, 3, 7, 2, 4,
    0, 5, 6, 9, 8, 3, 7, 2, 1, 4,
    8, 2, 9, 1, 6, 0, 3, 4, 5, 7,
];

displayl "Longest Palindromic Subsequence Length: " + string(longest_palindromic_subsequence(longarr));

"""


# pprint(list(lex(program)))
# pprint(parse(program, SymbolTable()))
# run_program(program,display_bytecode=True)
# execute(program)
x=3
def f():
    print(x)
def g():
    x=5
    return f
h= g()
x=4
h()

x = 3
def g():
    x = 5
    def f():
        print(x)
    return f

h = g()  # h = f (defined in g's scope)
x = 4    # Global x changes to 4
h()      # Call f()

import dis

def power(exp):
    def inner(base):
        return base ** exp
    return inner

square = power(2)
print(square.__closure__)
cube = power(3)

dis.dis(power)
# dis.dis(square)
# dis.dis(cube)
