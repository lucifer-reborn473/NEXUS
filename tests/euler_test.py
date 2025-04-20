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

# def test_euler_test_4(capfd):
#     prog = """
#     var res=0;
#     for (var i=100; i<=1000; i+=1){
#         for (var j=100; j<=1000; j+=1){
#             var string b= string(i*j);
#             var string c= b.Slice(None,None,-1);
#             var d = if b==c then i * j else 0 end;
#             res=max([res,d]);
#         }
#     };
#     displayl res;
#     """
#     execute(prog)
#     captured = capfd.readouterr()
#     assert "906609" in captured.out

#     run_program(prog)
#     captured = capfd.readouterr()
#     assert "906609" in captured.out
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
def test_euler_test_6(capfd):
    prog = """
    fn compute() {
        var N = 100;
        var s = 0;
        for (var i = 1; i <= N; i += 1) {
            s += i;
        };
        var sa = 0;
        for (var i = 1; i <= N; i += 1) {
            sa += i ** 2;
        };
        string((s ** 2) - sa);
    };
    displayl compute();
    """
    # execute(prog)
    # captured = capfd.readouterr()
    # assert "25164150" in captured.out

    run_program(prog)
    captured = capfd.readouterr()
    assert "25164150" in captured.out

def test_euler_test_7(capfd):
    prog = """
    fn compute() {
        fn isprime(n) {
            if n <= 1 then { 
                return False; 
            } end;
            var i = 2;
            while (i * i <= n) {
                if (n % i == 0) then { 
                    return False; 
                } end;
                i += 1;
            };
            return True;
        };
        var count = 0;
        var current = 2;
        var ans = 0;

        while (count < 10001) {
            if (isprime(current)) then {
                count += 1;
                if (count == 10001) then {
                    ans = current;
                } end;
            } end;
            current += 1;
        };

        string(ans);
    };

    displayl (compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "104743" in captured.out
    
def test_euler_test_8(capfd):
    prog = """
    fn compute() {
        var string NUMBER = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450";
        var ADJACENT = 13;
        
        fn digit_product(s) {
            var string p = s;
            var result = 1;
            var i = 0;
            while (i < p.Length) {
                result *= integer(p[i]);
                i += 1;
            };
            result;
        };

        var max_product = 0;
        var i = 0;
        
        while (i <= (NUMBER.Length - ADJACENT)) {
            var substring = NUMBER.Slice(i, i + ADJACENT);
            var product = digit_product(substring);
            
            if (product > max_product) then {
                max_product = product;
            } end;
            
            i += 1;
        };
        
        string(max_product);
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "23514624000" in captured.out

def test_euler_test_9(capfd):
    prog = """
    fn compute() {
        var PERIMETER = 1000;
        
        for (var a = 1; a < PERIMETER + 1; a += 1) {
            for (var b = a + 1; b < PERIMETER + 1; b += 1) {
                var c = PERIMETER - a - b;
                
                if (a * a + b * b == c * c) then {
                    /> It is now implied that b < c, because we have a > 0
                    return string(a * b * c);
                } end;
            };
        };
        
        return "No solution found";
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "31875000" in captured.out

def test_euler_test_10(capfd):
    prog = """
    fn compute() {
        fn is_prime(n) {
            if n <= 1 then { return False; } end;
            if n <= 3 then { return True; } end;
            if (n % 2 == 0 || n % 3 == 0) then { return False; } end;
            
            var i = 5;
            while (i * i <= n) {
                if (n % i == 0 || n % (i + 2) == 0) then { 
                    return False; 
                } end;
                i += 6;
            };
            
            return True;
        };
        
        /> Generate all primes below 2 million using Sieve of Eratosthenes
        var limit = 2000000;
        var array sieve = [];
        
        /> Initialize sieve array
        for (var i = 0; i < limit; i += 1) {
            sieve.PushBack(True);
        };
        
        /> 0 and 1 are not prime
        sieve[0] = False;
        sieve[1] = False;
        
        /> Apply sieve
        for (var i = 2; i * i < limit; i += 1) {
            if (sieve[i]) then {
                /> Mark all multiples of i as non-prime
                for (var j = i * i; j < limit; j += i) {
                    sieve[j] = False;
                };
            } end;
        };
        
        /> Sum all prime numbers
        var sum = 0;
        for (var i = 0; i < limit; i += 1) {
            if (sieve[i] != 0) then {
                sum += i;
            } end;
        };
        
        return string(sum);
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "142913828922" in captured.out

def test_euler_test_11(capfd):
    prog = """
    fn compute() {
        var array GRID = [
            [ 8, 2,22,97,38,15, 0,40, 0,75, 4, 5, 7,78,52,12,50,77,91, 8],
            [49,49,99,40,17,81,18,57,60,87,17,40,98,43,69,48, 4,56,62, 0],
            [81,49,31,73,55,79,14,29,93,71,40,67,53,88,30, 3,49,13,36,65],
            [52,70,95,23, 4,60,11,42,69,24,68,56, 1,32,56,71,37, 2,36,91],
            [22,31,16,71,51,67,63,89,41,92,36,54,22,40,40,28,66,33,13,80],
            [24,47,32,60,99, 3,45, 2,44,75,33,53,78,36,84,20,35,17,12,50],
            [32,98,81,28,64,23,67,10,26,38,40,67,59,54,70,66,18,38,64,70],
            [67,26,20,68, 2,62,12,20,95,63,94,39,63, 8,40,91,66,49,94,21],
            [24,55,58, 5,66,73,99,26,97,17,78,78,96,83,14,88,34,89,63,72],
            [21,36,23, 9,75, 0,76,44,20,45,35,14, 0,61,33,97,34,31,33,95],
            [78,17,53,28,22,75,31,67,15,94, 3,80, 4,62,16,14, 9,53,56,92],
            [16,39, 5,42,96,35,31,47,55,58,88,24, 0,17,54,24,36,29,85,57],
            [86,56, 0,48,35,71,89, 7, 5,44,44,37,44,60,21,58,51,54,17,58],
            [19,80,81,68, 5,94,47,69,28,73,92,13,86,52,17,77, 4,89,55,40],
            [ 4,52, 8,83,97,35,99,16, 7,97,57,32,16,26,26,79,33,27,98,66],
            [88,36,68,87,57,62,20,72, 3,46,33,67,46,55,12,32,63,93,53,69],
            [ 4,42,16,73,38,25,39,11,24,94,72,18, 8,46,29,32,40,62,76,36],
            [20,69,36,41,72,30,23,88,34,62,99,69,82,67,59,85,74, 4,36,16],
            [20,73,35,29,78,31,90, 1,74,31,49,71,48,86,81,16,23,57, 5,54],
            [ 1,70,54,71,83,51,54,69,16,92,33,48,61,43,52, 1,89,19,67,48]
        ];
        
        var CONSECUTIVE = 4;
        
        fn grid_product(ox, oy, dx, dy, n) {
            var result = 1;
            var i = 0;
            
            while (i < n) {
                result *= GRID[oy + i * dy][ox + i * dx];
                i += 1;
            };
            
            result;
        };
        
        var ans = -1;
        var array width = GRID[0];
        width = width.Length;
        var height = GRID.Length;
        
        for (var y = 0; y < height; y += 1) {
            for (var x = 0; x < width; x += 1) {
                /> Check horizontally (right)
                if (x + CONSECUTIVE <= width) then {
                    var product = grid_product(x, y, 1, 0, CONSECUTIVE);
                    if (product > ans) then {
                        ans = product;
                    } end;
                } end;
                
                /> Check vertically (down)
                if (y + CONSECUTIVE <= height) then {
                    var product = grid_product(x, y, 0, 1, CONSECUTIVE);
                    if (product > ans) then {
                        ans = product;
                    } end;
                } end;
                
                /> Check diagonally (down-right)
                if (x + CONSECUTIVE <= width and y + CONSECUTIVE <= height) then {
                    var product = grid_product(x, y, 1, 1, CONSECUTIVE);
                    if (product > ans) then {
                        ans = product;
                    } end;
                } end;
                
                /> Check diagonally (down-left)
                if (x - CONSECUTIVE >= -1 and y + CONSECUTIVE <= height) then {
                    var product = grid_product(x, y, -1, 1, CONSECUTIVE);
                    if (product > ans) then {
                        ans = product;
                    } end;
                } end;
            };
        };
        string(ans);
        
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "70600674" in captured.out
# def test_euler_test_12(capfd):
#     prog = """
#     fn compute() {
#         var triangle = 0;
#         var i = 1;
        
#         fn num_divisors(n) {
#             var ending = sqrt(n);
#             ending = floor(ending);
            
#             var result = 0;
#             var i = 1;
            
#             while (i <= ending) {
#                 if (n % i == 0) then {
#                     result += 2;
#                 } end;
                
#                 i += 1;
#             }
            
#             if (ending * ending == n) then {
#                 result -= 1;
#             } end;
            
#             return result;
#         };

#         while (True) {
#             triangle += i;
            
#             if (num_divisors(triangle) > 500) then {
#                 return string(triangle);
#             } end;
            
#             i += 1;
#         }
#     };

#     displayl(compute());
#     """
#     run_program(prog)
#     captured = capfd.readouterr()
#     assert "76576500" in captured.out
def test_euler_test_13(capfd):
    prog = """
    var array NUMBERS = [
    37107287533902102798797998220837590246510135740250,
    46376937677490009712648124896970078050417018260538,
    74324986199524741059474233309513058123726617309629,
    91942213363574161572522430563301811072406154908250,
    23067588207539346171171980310421047513778063246676,
    89261670696623633820136378418383684178734361726757,
    28112879812849979408065481931592621691275889832738,
    44274228917432520321923589422876796487670272189318,
    47451445736001306439091167216856844588711603153276,
    70386486105843025439939619828917593665686757934951,
    62176457141856560629502157223196586755079324193331,
    64906352462741904929101432445813822663347944758178,
    92575867718337217661963751590579239728245598838407,
    58203565325359399008402633568948830189458628227828,
    80181199384826282014278194139940567587151170094390,
    35398664372827112653829987240784473053190104293586,
    86515506006295864861532075273371959191420517255829,
    71693888707715466499115593487603532921714970056938,
    54370070576826684624621495650076471787294438377604,
    53282654108756828443191190634694037855217779295145,
    36123272525000296071075082563815656710885258350721,
    45876576172410976447339110607218265236877223636045,
    17423706905851860660448207621209813287860733969412,
    81142660418086830619328460811191061556940512689692,
    51934325451728388641918047049293215058642563049483,
    62467221648435076201727918039944693004732956340691,
    15732444386908125794514089057706229429197107928209,
    55037687525678773091862540744969844508330393682126,
    18336384825330154686196124348767681297534375946515,
    80386287592878490201521685554828717201219257766954,
    78182833757993103614740356856449095527097864797581,
    16726320100436897842553539920931837441497806860984,
    48403098129077791799088218795327364475675590848030,
    87086987551392711854517078544161852424320693150332,
    59959406895756536782107074926966537676326235447210,
    69793950679652694742597709739166693763042633987085,
    41052684708299085211399427365734116182760315001271,
    65378607361501080857009149939512557028198746004375,
    35829035317434717326932123578154982629742552737307,
    94953759765105305946966067683156574377167401875275,
    88902802571733229619176668713819931811048770190271,
    25267680276078003013678680992525463401061632866526,
    36270218540497705585629946580636237993140746255962,
    24074486908231174977792365466257246923322810917141,
    91430288197103288597806669760892938638285025333403,
    34413065578016127815921815005561868836468420090470,
    23053081172816430487623791969842487255036638784583,
    11487696932154902810424020138335124462181441773470,
    63783299490636259666498587618221225225512486764533,
    67720186971698544312419572409913959008952310058822,
    95548255300263520781532296796249481641953868218774,
    76085327132285723110424803456124867697064507995236,
    37774242535411291684276865538926205024910326572967,
    23701913275725675285653248258265463092207058596522,
    29798860272258331913126375147341994889534765745501,
    18495701454879288984856827726077713721403798879715,
    38298203783031473527721580348144513491373226651381,
    34829543829199918180278916522431027392251122869539,
    40957953066405232632538044100059654939159879593635,
    29746152185502371307642255121183693803580388584903,
    41698116222072977186158236678424689157993532961922,
    62467957194401269043877107275048102390895523597457,
    23189706772547915061505504953922979530901129967519,
    86188088225875314529584099251203829009407770775672,
    11306739708304724483816533873502340845647058077308,
    82959174767140363198008187129011875491310547126581,
    97623331044818386269515456334926366572897563400500,
    42846280183517070527831839425882145521227251250327,
    55121603546981200581762165212827652751691296897789,
    32238195734329339946437501907836945765883352399886,
    75506164965184775180738168837861091527357929701337,
    62177842752192623401942399639168044983993173312731,
    32924185707147349566916674687634660915035914677504,
    99518671430235219628894890102423325116913619626622,
    73267460800591547471830798392868535206946944540724,
    76841822524674417161514036427982273348055556214818,
    97142617910342598647204516893989422179826088076852,
    87783646182799346313767754307809363333018982642090,
    10848802521674670883215120185883543223812876952786,
    71329612474782464538636993009049310363619763878039,
    62184073572399794223406235393808339651327408011116,
    66627891981488087797941876876144230030984490851411,
    60661826293682836764744779239180335110989069790714,
    85786944089552990653640447425576083659976645795096,
    66024396409905389607120198219976047599490197230297,
    64913982680032973156037120041377903785566085089252,
    16730939319872750275468906903707539413042652315011,
    94809377245048795150954100921645863754710598436791,
    78639167021187492431995700641917969777599028300699,
    15368713711936614952811305876380278410754449733078,
    40789923115535562561142322423255033685442488917353,
    44889911501440648020369068063960672322193204149535,
    41503128880339536053299340368006977710650566631954,
    81234880673210146739058568557934581403627822703280,
    82616570773948327592232845941706525094512325230608,
    22918802058777319719839450180888072429661980811197,
    77158542502016545090413245809786882778948721859617,
    72107838435069186155435662884062257473692284509516,
    20849603980134001723930671666823555245252804609722,
    53503534226472524250874054075591789781264330331690,
];
    fn compute(arr) {
        var string val=SUM(arr);
        return val.Slice(0, 10);
    };
    displayl compute(NUMBERS);
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "5537376230" in captured.out

def test_euler_test_15(capfd):
    prog = """
    fn compute() {
        fn factorial(n) {
            var result = 1;
            for (var i = 2; i <= n; i += 1) {
                result *= i;
            };
            result;
        };
        
        fn binomial_coefficient(n, k) {
            /> Handle edge cases
            if (k > n) then { return 0; } end;
            if (k == 0 or k == n) then { return 1; } end;
            
            /> Optimize by using the smaller k value due to symmetry: C(n,k) = C(n,n-k)
            if (k > n - k) then {
                k = n - k;
            } end;
            
            /> Calculate using the formula C(n,k) = n!/(k!(n-k)!)
            /> But compute it efficiently to avoid overflow
            var result = 1;
            for (var i = 1; i <= k; i += 1) {
                result *= (n - k + i);
                result /= i;
            };
            
            return result;
        };
        
        string(floor(binomial_coefficient(40, 20)));
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "137846528820" in captured.out

def test_euler_test_16(capfd):
    prog = """
    fn compute() {
        /> Calculate 2^1000
        var n = 2 ** 1000;
        
        /> Convert to string
        var string n_str = string(n);
        
        /> Sum the digits
        var sum = 0;
        for (var i = 0; i < n_str.Length; i += 1) {
            sum += integer(n_str[i]);
        };
        
        return string(sum);
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "1366" in captured.out


def test_euler_test_17(capfd):
    prog = """
    fn compute() {
        var array ONES = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"
        ];
        
        var array TENS = [
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
        ];
        
        fn to_english(n) {
            if (0 <= n and n < 20) then {
                return ONES[n];
            } end;
            
            if (20 <= n and n < 100) then {
                var integer tens_digit = n / 10;
                var integer ones_digit = n % 10;
                
                if (ones_digit != 0) then {
                    return TENS[tens_digit] + ONES[ones_digit];
                } else {
                    return TENS[tens_digit];
                } end;
            } end;
            
            if (100 <= n and n < 1000) then {
                var integer hundreds_digit = n / 100;
                var integer remainder = n % 100;
                
                if (remainder != 0) then {
                    return ONES[hundreds_digit] + "hundred" + "and" + to_english(remainder);
                } else {
                    return ONES[hundreds_digit] + "hundred";
                } end;
            } end;
            
            if (1000 <= n and n < 1000000) then {
                var integer thousands = n / 1000;
                var integer remainder = n % 1000;
                
                if (remainder != 0) then {
                    return to_english(thousands) + "thousand" + to_english(remainder);
                } else {
                    return to_english(thousands) + "thousand";
                } end;
            } end;
            
            return "Error: Number out of range";
        };
        
        var integer sum = 0;
        
        for (var integer i = 1; i <= 1000; i += 1) {
            var string word = to_english(i);
            sum += word.Length;
        };
        
        return string(sum);
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "21124" in captured.out

def test_euler_test_18(capfd):
    prog = """
    fn compute() {
        var array triangle = [  /> Mutable
            [75],
            [95,64],    
            [17,47,82],
            [18,35,87,10],
            [20, 4,82,47,65],
            [19, 1,23,75, 3,34],
            [88, 2,77,73, 7,63,67],
            [99,65, 4,28, 6,16,70,92],
            [41,41,26,56,83,40,80,70,33],
            [41,48,72,33,47,32,37,16,94,29],
            [53,71,44,65,25,43,91,52,97,51,14],
            [70,11,33,28,77,73,17,78,39,68,17,57],
            [91,71,52,38,17,14,91,43,58,50,27,29,48],
            [63,66, 4,68,89,53,67,30,73,16,69,87,40,31],
            [ 4,62,98,27,23, 9,70,98,73,93,38,53,60, 4,23]
        ];
        
        var integer height = triangle.Length;

        /> Process the triangle from bottom to top
        for (var i = height - 2; i >= 0; i -= 1) {
            var array idx = triangle[i];
            var width = idx.Length ;  /> Get the width of the current row    
            
            for (var j = 0; j < width; j += 1) {
                /> For each position, add the maximum of the two possible paths below
                var integer path1 = triangle[i + 1][j];
                var integer path2 = triangle[i + 1][j + 1];
                
                if (path1 > path2) then {
                    triangle[i][j] = triangle[i][j] + path1;
                } else {
                    triangle[i][j] = triangle[i][j] + path2;
                } end;
            };
            
        };
        /> The top element now contains the maximum path sum
        return string(triangle[0][0]);
    };

    displayl(compute());
    """
    run_program(prog)
    captured = capfd.readouterr()
    assert "1074" in captured.out