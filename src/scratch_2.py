from bytecode_eval_new import *


program = """
/> Function to calculate and print Pascal's Triangle
fn printPascal(height) {

    for (var row = 0; row < height; row += 1) {
        var value = 1; 
        var line_str = ""; 

        
        for (var col = 0; col <= row; col += 1) {
            line_str += string(value) + " "; 
            if col < row then
                 value = floor(value * (row - col) / (col + 1));
            end;
        };
        
        displayl line_str; /> Print the completed row with a newline
    };
};

var triangleHeight = 50;

displayl "Height " + string(triangleHeight) + " is:"; 
printPascal(triangleHeight);

"""


program = """

/> Function to find a triplet a, b, c such that a + b = c
fn findTripletSumEqualsThird(arr) {
    var n = arr.Length;
    
    if n < 3 then
        "N";
    else {
        arr= sort(arr); 

        var result_str = "N"; /> Default result if no triplet is found
        var found = False;

        
        for (var i = n - 1; i >= 2; i -= 1) {
            var c = arr[i];
            var left = 0;     
            var right = i - 1;  

            /> Use two pointers to find 'a' and 'b' such that a + b = c [4][6]
            while (left < right) {
                var a = arr[left];
                var b = arr[right];
                var current_sum = a + b;

                if current_sum == c then {
                    result_str = string(a) + " " + string(b) + " " + string(c);
                    found = True;
                    breakout; 
                }
                else {
                    if current_sum < c then left += 1 else  right -= 1 end;
                   
                } end;
            };

            /> If a triplet was found in the inner loop, exit the outer loop too
            if found then
                breakout;
            end;
        };

        result_str; /> Return the result ("N" or "a b c")
    } end;
};


var numbers1 = [5, 32, 1, 7, 10, 2];

displayl "Output: " + findTripletSumEqualsThird(numbers1); /> Should output "2 5 7" after sorting

var numbers2 = [1, 2, 4, 8, 16];

displayl "Output: " + findTripletSumEqualsThird(numbers2); /> Should output "N"

var numbers3 = [12, 3, 7, 1, 9, 5, 2, 8, 4, 6, 15, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205];

displayl "Output: " + findTripletSumEqualsThird(numbers3); /> Should output "4 6 10" after sorting

var numbers4 = [12, 3, 7, 1, 9, 5, 2, 8, 4, 6, 15, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335, 340, 345, 350, 355, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425, 430, 435, 440, 445, 450, 455];

displayl "Output: " + findTripletSumEqualsThird(numbers4); 
"""

program ="""


fn isSubsetSumRec(arr, n, target_sum) {
    if target_sum == 0 then
        True;
    else {
        if n==0 then False;

        else{
          if arr[n - 1] > target_sum then
               isSubsetSumRec(arr, n - 1, target_sum);
           
          else{
             (isSubsetSumRec(arr, n - 1, target_sum) or 
         isSubsetSumRec(arr, n - 1, target_sum - arr[n - 1]));
          }end;
        }end;
    } end;
   
};

fn isSubsetSum(arr, target) {
    var array_length = arr.Length;
    if isSubsetSumRec(arr, array_length, target) then "YES" else "NO" end;
    
};


var numbers = [3, 1, 4, 12, 5, 2]; 
var target_value = 9;
displayl target_value - numbers [2];
displayl "Array: [3, 1, 4, 12, 5, 2], Target: " + string(target_value);
displayl isSubsetSum(numbers, target_value); /> Expected: 3 1 5 or 4 5 or 3 4 2 etc.

var numbers2 = [
    341835794,
    129262015,
    446653186,
    173151548,
    257363959,
    420346099,
    420455834,
    320952346,
    100086772,
    427405173,
    260698675,
    108105182,
    457738910,
    389289752,
    145505875,
    161482628,
    377188110,
    244711243,
    380815083,
    188171290,
    123832180,
    232578136,
    298963308,
    334715643,
    481403633,
    354891731,
    220805776,
    199507932,
    235721041,
    488103709
]; /> Array declared with []
var target_value2 = 488103709 + 220805776;
/> displayl "Array: [1, 8, 2, 5], Target: " + string(target_value2);
displayl isSubsetSum(numbers2, target_value2);

var numbers3=  [
    327285663,
    433995612,
    446583812,
    188541247,
    194600543,
    300157004,
    380418159,
    337672726,
    228681054,
    336574819,
    228071553,
    432851990
];

var target_value3 = 1489926782;

displayl isSubsetSum(numbers3, target_value3);

"""


# pprint(list(lex(program)))
pprint(parse(program, SymbolTable()))

# run_program(program,display_bytecode=True)
execute(program)