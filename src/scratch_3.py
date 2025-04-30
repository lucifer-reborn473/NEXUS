from bytecode_eval_new import *

program = """
fn arrayContains(arr, item) {
    var exists = False;
    for (var i = 0; i < arr.Length; i += 1) {
        if arr[i] == item then {
            exists = True;
            break;
        } end;
    };
    exists;
};

fn countDistinctPrimeFactors(num) {
    if num <= 1 then 0
    else {
        var count = 0;
        var n = num;
        var d = 2;
        var distinct_primes = [];

        if n % 2 == 0 then {
            if not arrayContains(distinct_primes, 2) then {
                 PushBack(distinct_primes, 2);
                 count += 1;
            } end;
            while (n % 2 == 0) { n /= 2; };
        } end;

        d = 3;
        while (d * d <= n) {
            if n % d == 0 then {
                if not arrayContains(distinct_primes, d) then {
                    PushBack(distinct_primes, d);
                    count += 1;
                } end;
                while (n % d == 0) { n /= d; };
            } end;
            d += 2;
        };

        if n > 1 then {
             if not arrayContains(distinct_primes, n) then {
                 count += 1;
             } end;
        } end;
        count;
    } end;
};

fn findLargestNarayana(limit) {
    var a = 1; var b = 1; var c = 1;
    var largest_valid = -1;
    if 1 < limit then largest_valid = 1 end;
    var current_term = 0;

    while (True) {
        current_term = b + a;
        if current_term >= limit then break; end;
        
        var distinct_factors = countDistinctPrimeFactors(current_term);
        if distinct_factors <= 3 then
            largest_valid = current_term;
        end;

        a = b; b = c; c = current_term;
    };
    largest_valid;
};

var limit1 = 100;
var limit2 = 10000;
var limit3 = 1000000;

var result1 = findLargestNarayana(limit1);
var result2 = findLargestNarayana(limit2);
var result3 = findLargestNarayana(limit3);

displayl string(result1);
displayl string(result2);
displayl string(result3);

"""
pprint(list(lex(program)))
pprint(parse(program, SymbolTable()))

# run_program(program,display_bytecode=True)
execute(program)