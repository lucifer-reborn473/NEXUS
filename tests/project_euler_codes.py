import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import pytest
from evaluator import *


code1="""
    var x=999g;
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

execute(code1)