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
    var limit = 4 * 10^6;
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

