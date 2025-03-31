# Scope Management

This document provides an overview of the scope management system implemented in the Our_Compiler project. It details the `SymbolTable` class, its methods for managing variable scopes, and the `SymbolCategory` enumeration used to categorize symbols.

## SymbolTable Class

The `SymbolTable` class is responsible for maintaining a mapping of identifiers (variables, functions, etc.) to their corresponding values and categories. It supports nested scopes, allowing for the definition of variables within functions or blocks without interfering with variables in outer scopes.

### Attributes

- `table`: A dictionary that maps identifiers to a tuple containing the value and its category.
- `parent`: A reference to the parent `SymbolTable`, enabling scope chaining.

### Methods

#### `__init__(self, parent=None)`

Initializes a new `SymbolTable`. If a parent is provided, it allows for nested scopes.

#### `define(self, iden, value, category: SymbolCategory)`

Defines a new identifier in the current scope with its associated value and category.

- **Parameters**:
  - `iden`: The identifier name (string).
  - `value`: The value associated with the identifier.
  - `category`: The category of the symbol (e.g., variable, function).

#### `lookup(self, iden, cat=False)`

Looks up an identifier in the current scope and its parent scopes.

- **Parameters**:
  - `iden`: The identifier name (string).
  - `cat`: If `True`, returns the category instead of the value.
- **Returns**: The value or category of the identifier.
- **Raises**: `NameError` if the identifier is not found.

#### `inScope(self, iden)`

Checks if an identifier is defined in the current scope.

- **Parameters**:
  - `iden`: The identifier name (string).
- **Returns**: `True` if the identifier is in the current scope, `False` otherwise.

#### `find_and_update_arr(self, iden, index, val)`

Updates the value at a specific index in an array.

- **Parameters**:
  - `iden`: The identifier name of the array.
  - `index`: The index to update.
  - `val`: The new value to assign.
- **Raises**: `NameError` if the identifier is not found or is not an array.

#### `find_and_update(self, iden, val)`

Updates the value of an identifier in the current scope.

- **Parameters**:
  - `iden`: The identifier name (string).
  - `val`: The new value to assign.
- **Raises**: `NameError` if the identifier is not found.

#### `copy_scope(self)`

Creates a copy of the current scope, allowing for the creation of a new scope that inherits from the current one.

- **Returns**: A new `SymbolTable` instance that is a copy of the current scope.

## SymbolCategory Enum

The `SymbolCategory` enumeration categorizes symbols managed by the `SymbolTable`. It includes the following categories:

- `VARIABLE`: Represents a variable.
- `FUNCTION`: Represents a function.
- `ARRAY`: Represents an array.
- `CONSTANT`: Represents a constant value.
- `HASH`: Represents a hash (dictionary).
- `SCHEMA`: Represents a class or schema.
