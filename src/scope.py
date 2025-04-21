from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum
from pprint import pprint
from copy import copy

class SymbolCategory(Enum):
    VARIABLE = "variable"
    ARRAY = "list"
    HASH = "dict"
    SCHEMA ="class"
    FIXED = "fixed"
    STRING = "string"
    FUNCTION = "function"
    BOOLEAN = "boolean"

def map_type_to_enum(type_str: str) -> SymbolCategory:
    type_mapping = {
        "integer": SymbolCategory.VARIABLE,
        "uinteger": SymbolCategory.VARIABLE,
        "boolean": SymbolCategory.VARIABLE,
        "decimal": SymbolCategory.VARIABLE,
        "string": SymbolCategory.STRING,
        "array": SymbolCategory.ARRAY,
        "Hash": SymbolCategory.HASH,
    }
    return type_mapping.get(type_str, None)

@dataclass
class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}  # Format: {iden: (value, category)}
        self.parent = parent  # enclosing scope

    def define(self, iden, value, category: SymbolCategory):
        self.table[iden] = (value, category)

    def lookup(self, iden, cat=False, giveParent=False):
        if iden in self.table:
            if not giveParent:
                return self.table[iden][1] if cat else self.table[iden][0]  # returns category if cat=True, else value
            else:
                return (self.table[iden][1], self) if cat else (self.table[iden][0], self)
        
        elif self.parent:
            return self.parent.lookup(iden, cat, giveParent)
        
        else:
            raise NameError(f"Variable '{iden}' not found!")
        
    def lookup_fun(self, iden):
        if iden in self.table:
            value = self.table[iden]
            return (value[0], self)
        elif self.parent:
            return self.parent.lookup_fun(iden)
        else:
            raise NameError(f"Function '{iden}' not found!")


    def inScope(self, iden):
        return iden in self.table

    def find_and_update_arr(self, iden, index, val):
        if iden in self.table:
            category = self.table[iden][1]
            if category == SymbolCategory.FIXED:
                raise ValueError(f"Error: Cannot modify elements of fixed array '{iden}'")
            
            if category == SymbolCategory.ARRAY:
                array = self.table[iden][0]
                array[index] = val
                self.table[iden] = (array, SymbolCategory.ARRAY)
        elif self.parent:
            self.parent.find_and_update_arr(iden, index, val)
        else:
            raise NameError(f"Variable '{iden}' not found!")
        
    def find_and_update(self, iden, val, new_category=None):
        if iden in self.table:
            category = self.table[iden][1]
            if category == SymbolCategory.FIXED:
                raise ValueError(f"Error: Cannot reassign to a fixed variable '{iden}'")
            category_to_use = new_category if new_category is not None else category
            self.table[iden] = (val, category_to_use)
        elif self.parent:
            self.parent.find_and_update(iden, val)
        else:
            raise NameError(f"Variable '{iden}' not found!")

    def copy_scope(self):
        new_scope = SymbolTable(parent=self.parent)
        new_scope.table = self.table.copy()
        return new_scope