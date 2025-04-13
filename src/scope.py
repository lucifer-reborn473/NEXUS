from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum
from pprint import pprint

class SymbolCategory(Enum):
    VARIABLE = "variable"
    FUNCTION = "function"
    ARRAY = "list"
    CONSTANT = "constant"
    HASH = "dict"
    SCHEMA ="class"
    # Add more categories as needed

@dataclass
class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}  # Format: {identifier: (value, category)}
        self.parent = parent  # enclosing scope

    def define(self, iden, value, category: SymbolCategory):
        self.table[iden] = (value, category)

    def lookup(self, iden, cat=False):
        # print(f"...looking for {iden} with cat={cat}...")
        if iden in self.table:
            return self.table[iden][1] if cat else self.table[iden][0]  # returns category if cat=True, else value
        elif self.parent:  # check in parent (enclosing scope)
            # print(f"here for {iden} in {self.parent.table} with cat={cat}")
            return self.parent.lookup(iden, cat)
        else:
            raise NameError(f"Variable '{iden}' nhi mila!")
        
    # def lookup_fun(self, iden):
    #     if iden in self.table:
    #         print("\n****")
    #         pprint(self.table[iden])
    #         print("****\n")
    #         return (self.table[iden][0], self)
    #     elif self.parent:
    #         return self.parent.lookup_fun(iden)
    #     else:
    #         raise NameError(f"Function '{iden}' nhi mila!")
    def lookup_fun(self, iden):
        if iden in self.table:
            value = self.table[iden]
            # Check if this is a function
            if value[1] == SymbolCategory.FUNCTION:
                func_def = value[0]
                
                # Recursively unwrap nested function definitions
                def unwrap_function(fd):
                    # If it's a wrapped function with category
                    if (isinstance(fd, tuple) and len(fd) == 2 and 
                        isinstance(fd[1], SymbolCategory) and 
                        fd[1] == SymbolCategory.FUNCTION):
                        # Unwrap one level and check again
                        return unwrap_function(fd[0])
                    return fd
                
                # Get the fully unwrapped function definition
                clean_func_def = unwrap_function(func_def)
                return (clean_func_def, self)
            else:
                raise TypeError(f"'{iden}' is not a function")
        elif self.parent:
            return self.parent.lookup_fun(iden)
        else:
            raise NameError(f"Function '{iden}' nhi mila!")



    def inScope(self, iden):
        return iden in self.table

    def find_and_update_arr(self, iden, index, val):
        if iden in self.table and self.table[iden][1] == SymbolCategory.ARRAY:
            array = self.table[iden][0]
            array[index] = val
            self.table[iden] = (array, SymbolCategory.ARRAY)
        elif self.parent:
            self.parent.find_and_update_arr(iden, index, val)
        else:
            raise NameError(f"Variable '{iden}' nhi mila!")
    def find_and_update(self, iden, val):
        if iden in self.table:
            category = self.table[iden][1]
            self.table[iden] = (val, category)
        elif self.parent:
            self.parent.find_and_update(iden, val)
        else:
            raise NameError(f"Variable '{iden}' nhi mila!")

    def copy_scope(self):
        new_scope = SymbolTable(parent=self.parent)
        new_scope.table = self.table.copy()
        return new_scope