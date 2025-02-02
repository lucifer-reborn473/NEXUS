from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class VariableInfo:
    value: Any
    dtype: Optional[str]
    redundant: Optional[Any] = None

@dataclass
class Context:
    variables: Dict[str, VariableInfo] = field(default_factory=dict)

    type_map={
        "integer": int,
        "decimal": float,
        "uinteger": int,
        "string": str,
    }
    def add_variable(self, name: str, value: Any, var_type: Optional[str] = None, redundant: Optional[Any] = None):
        if not isinstance(name, str):
            raise TypeError(f"Variable name must be a string, got {type(name)}")
        if var_type:
            if var_type not in self.type_map:
                raise TypeError(f"Invalid variable type: {var_type}")
            try:
                value = self.type_map[var_type](value)
            except ValueError as e:
                raise ValueError(f"Cannot convert {value} to {var_type}: {e}")

        self.variables[name] = VariableInfo(value, var_type, redundant)

    def get_variable(self, name: str) -> Optional[VariableInfo]:
        return self.variables.get(name)

    def has_variable(self, name: str) -> bool:
        return name in self.variables

    def remove_variable(self, name: str) -> bool:
        if name in self.variables:
            del self.variables[name]
            return True
        return False

    def update_variable(self, name: str, value: Any, var_type: Optional[str] = None) -> bool:
        if name not in self.variables:
            return False
            
        current_info = self.variables[name]
        self.variables[name] = VariableInfo(value, var_type or current_info.dtype, current_info.redundant)
        return True

    def list_variables(self) -> Dict[str, str]:
        """Returns a dictionary of variable names and their types"""
        return {name: str(info.dtype) for name, info in self.variables.items()}


# Example usage and testing
if __name__ == "__main__":
    context = Context()

    # Test adding variables
    try:
        context.add_variable("x", 42, "int")
        context.add_variable("y", "hello", "str")
        context.add_variable("z", 3.14, "float")
        
        # Test getting variables
        x_info = context.get_variable("x")
        print(f"x value: {x_info.value}, type: {x_info.dtype}")
        
        # Test variable existence
        print(f"Does x exist? {context.has_variable('x')}")
        print(f"Does w exist? {context.has_variable('w')}")
        
        # Test listing variables
        print("All variables:", context.list_variables())
        
        # Test updating variable
        context.update_variable("x", 100)
        x_info = context.get_variable("x")
        print(f"Updated x value: {x_info.value}")
        
        # Test removing variable
        removed = context.remove_variable("y")
        print(f"Removed y: {removed}")
        print(f"y exists: {context.has_variable('y')}")
        
        # Test type validation
        try:
            context.add_variable("error", "not a number", "int")
        except TypeError as e:
            print(f"Caught expected error: {e}")
            
    except Exception as e:
        print(f"An error occurred: {e}")