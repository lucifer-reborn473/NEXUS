# Arrays

Arrays are declared and manipulated using square brackets. They support various operations such as adding, removing, and accessing elements.

### Rules:

- Arrays can contain elements of mixed types.
- Operations like `PushFront`, `PushBack`, `Insert`, and `Remove` modify the array.
- Accessing an invalid index will throw an error.

**Examples:**

```prog
var array arr = [1, 2, 3];
arr.PushBack(4); /> Adds 4 to the end
display arr[2]; /> Displays 3
arr.Remove(1); /> Removes the element at index 1
display arr.Length; /> Displays the length of the array
```


# Hashes

Hashes (dictionaries) are declared and manipulated using curly braces. They allow key-value pairs and support operations like adding and removing keys.

### Rules:

- Keys must be unique.
- Accessing a non-existent key will throw an error.
- Operations like `Add` and `Remove` modify the hash.

**Examples:**

```prog
var hash h = {"key1": 10, "key2": 20};
h.Add("key3", 30); /> Adds a new key-value pair
display h["key1"]; /> Displays 10
h.Remove("key2"); /> Removes the key "key2"
```


## Sample Program

Here is a sample program demonstrating all the features:

```prog
var x = 10;
var arr = [1, 2, 3];
var hash = {"key1": 10, "key2": 20};

arr.PushBack(4);
hash.Add("key3", 30);

fn multiply(a, b) {
    a * b;
}

if x > 5 then {
    displayl "x is greater than 5";
} else {
    displayl "x is 5 or less";
} end;

while (x > 0) {
    displayl x;
    x = x - 1;
}
displayl ("Array run:");
for (var integer i = 0; i < arr.Length; i = i + 1) {
    displayl arr[i];
}

display multiply(hash["key1"], 2);
```

# Schema
### Base Structure

```prog
schema <TypeName>([arguments]) {
    [initialize(|set_default)]
    [methods]
}
```


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
