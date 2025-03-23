prog = """
var x = 2;
fn foo(){
    var x = 300;
    x;
}
fn bar(x){
    x += 1000;
    x;
}
fn baz(x){
    if x<5 then foo() else bar(x) end;
}
displayl baz(4); /~ 300 ~/
displayl baz(6); /~ 1006 ~/
""" # works!

prog2 = """
var x = 179;
fn bar() {
    x;
}
fn foo() {
    var x = 100;
    bar();
}
displayl foo();
""" # works! (prints 179)

prog3 = """
var x = 1000;
fn foo() {
    fn bar() {
        x;
    }
    bar();
}
displayl foo();
""" # works! (prints 1000)

prog4 = """
var x = 1000;
fn foo() {
    var x = 117;
    fn bar() {
        x;
    }
    bar();
}
displayl foo();
""" # works! (prints 117)

prog5 = """
var a = "g-";
fn foo(x, i){
    if i==1 then var a = "l-" else "dummy" end;
    if x==1 then "k" else a + foo(x-1, i+1) end;
}
displayl foo(5,1);
""" #! Error in Cpp, Python but works in TOPL !