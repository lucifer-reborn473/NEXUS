# Schema Type Documentation

## Table of Contents

1. [Syntax Definition](#syntax-definition)
2. [Core Concepts](#core-concepts)
3. [Initialization Rules](#initialization-rules)
4. [Method Types](#method-types)
5. [Complete Examples](#complete-examples)
6. [Test Cases](#test-cases)
7. [Compatibility Matrix](#compatibility-matrix)
8. [Edge Cases](#edge-cases)

---

## Syntax Definition

### Base Structure

```prog
schema <TypeName>([arguments]) {
    [initialize(|set_default)]
    [methods]
}
```

### Formal Grammar

```prog
SchemaDecl = "schema" ID [Params] "{" SchemaBody "}"
Params = "(" [ArgList] ")" | ε
ArgList = ID ["," ArgList]
SchemaBody = (InitBlock | DefaultBlock | MethodDecl)*
InitBlock = "initialize" "(" [ArgList] ")" Block
DefaultBlock = "set_default" "(" [ArgList] ")" Block
MethodDecl = "fn" ID "(" [ArgList] ")" Block
```

---

## Core Concepts

### Declaration Styles

**Style 1: Header Parameters**

```prog
schema Vector3(x, y, z) {
    fn sqrt(val){
        val^0.5;
    }
    fn magnitude() {
        sqrt(x^2 + y^2 + z^2);
    }
};
```

**Style 2: Explicit Initialize**

```prog
schema Animal {
    initialize(name, sound);
    fn call_name() {
        name;
    }
}
```


Without initialize the code will throw error.

---

## Initialization Rules

### Mandatory Components

- Every schema requires initialization via either:
  - Header parameters
  - Explicit `initialize()` method

### Optional Defaults

```prog
schema AppConfig(
    timeout,
    retries
) {
    set_default(timeout=60) /> Overrides header default
};
```

---

## Method Types

### Instance Methods

```prog
schema Counter {
    initialize(value);
    set_default(value=0);

    fn increment() {
        value += 1
    }
};

c = Counter();
c.increment();
```

### Direct Schema Calls

```prog
schema MathUtils {
    fn factorial(n) {
        if n <= 1 then {
            1;
        }
        else{
            n * factorial(n-1);
        }
        end;
    }
};

MathUtils.factorial(5) /> 120
```

---

## Complete Examples

### Complex Schema

```prog
schema HTTPClient(
    base_url,
    timeout
) {
    set_default(timeout=15)

    initialize() {
        headers = {"Content-Type": "application/json"}
    }

    fn get(endpoint) {
        return fetch(base_url + endpoint)
    }

    fn post(endpoint, data) {
        return send("POST", endpoint, data)
    }
};
```

---

## Test Cases

### Validation Suite

```prog
/> TEST 1: Basic Instantiation
schema Box(w, h) {
    fn area() { return w * h }
}
b = Box(3, 4)
displayl b.area();

// TEST 2: Default Overrides
schema TestDefault(
    a=1,
    b=2
) {
    set_default(a=5)
}
t = TestDefault()
displayl t.a == 5 // Header default overridden

/> TEST 3: Error Conditions
schema ErrorSchema {
    initialize(req_arg)
}
/> Should throw: Missing required argument 'req_arg'
e = ErrorSchema()
```

---

## Compatibility Matrix

| Feature               | Support | Notes                            |
| --------------------- | ------- | -------------------------------- |
| Optional Parameters   | ✔️    | In header and methods            |
| Method Chaining       | ❌      | No implicit `return this`      |
| Schema Composition    | ✔️    | Via nested initialization        |
| Operator Overloading  | ❌      |                                  |
| Runtime Modifications | ✔️    | Add/remove methods post-creation |

---

## Edge Cases

### Empty Schema

```prog
schema Ghost {}
g = Ghost() // Valid zero-property object
```

### Schema in Collections	

```prog
schema Node(id) {};
var nodes = [
    Node(1),
    Node(2),
    Node(3)
];

displayl nodes;
```

### Self-Referential (To be implemented)

```prog
schema TreeNode {
    initialize(value)

    fn add_child(child) {
        value.PushBack(child)
        child.parent = this
    }
};
```

---

Add in docs:
initialize overrides vars declared in brackets i.e.
if anything declared before initialize is considered invalid
