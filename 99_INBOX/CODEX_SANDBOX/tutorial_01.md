# **Immutability and Persistent Data Structures**

> A practical guide to writing programs where values do not change—and where “updates” produce new values without wastefully copying everything.

## **Table of Contents**

1. [What Is Immutability?](#1-what-is-immutability)
2. [Why Immutability Matters](#2-why-immutability-matters)
3. [Values, Bindings, and Mutation](#3-values-bindings-and-mutation)
4. [Updating Immutable Data](#4-updating-immutable-data)
5. [Structural Sharing](#5-structural-sharing)
6. [Persistent Data Structures](#6-persistent-data-structures)
7. [Immutability in JavaScript](#7-immutability-in-javascript)
8. [Immutability in Python](#8-immutability-in-python)
9. [Concurrency and Predictability](#9-concurrency-and-predictability)
10. [Performance Trade-offs](#10-performance-trade-offs)
11. [Practical Design Patterns](#11-practical-design-patterns)
12. [Common Mistakes](#12-common-mistakes)
13. [Exercises](#13-exercises)
14. [Summary](#14-summary)

---

## **1. What Is Immutability?**

**Immutability** means that a value cannot be changed after it has been created.

Consider a coordinate:

```text
(x: 3, y: 5)
```

In a mutable design, moving the coordinate might change `x` directly:

```text
(x: 3, y: 5)  →  (x: 4, y: 5)
     same object, modified in place
```

In an immutable design, moving it creates a new coordinate:

```text
(x: 3, y: 5)  →  (x: 4, y: 5)
 original          new value
```

The original remains `(3, 5)`. Any part of the program that still refers to it continues to see exactly the same value.

This idea sounds restrictive, but it provides a strong guarantee:

> **Once you know the value of immutable data, no distant function, asynchronous callback, or concurrent task can silently change it.**

---

## **2. Why Immutability Matters**

Mutable state is not inherently wrong. Computers are stateful machines, and useful programs eventually change something. The difficulty is that unrestricted mutation makes change harder to track.

Suppose several functions share an object:

```javascript
const settings = {
  theme: "dark",
  notifications: true
};

function disableNotifications(config) {
  config.notifications = false;
}

disableNotifications(settings);
console.log(settings.notifications); // false
```

The function's name suggests an action, but its most important behavior is implicit: it changes an object owned by its caller. If the same object is shared elsewhere, those consumers observe the change too.

An immutable version makes the result explicit:

```javascript
function withNotificationsDisabled(config) {
  return {
    ...config,
    notifications: false
  };
}

const originalSettings = {
  theme: "dark",
  notifications: true
};

const newSettings = withNotificationsDisabled(originalSettings);

console.log(originalSettings.notifications); // true
console.log(newSettings.notifications);      // false
```

### **Key Benefits**

| Benefit | Why it helps |
|---|---|
| Predictability | A value does not change behind your back. |
| Easier debugging | State transitions can be inspected as distinct before-and-after values. |
| Safer concurrency | Readers can share immutable data without coordinating writes. |
| Simpler testing | Pure functions need fewer mocks and less setup. |
| Reliable caching | The same input can safely map to the same cached output. |
| Undo and history | Earlier versions remain available instead of being overwritten. |

---

## **3. Values, Bindings, and Mutation**

Immutability is often confused with constant variables. They are related, but different.

### **A binding is a name**

A variable binds a name to a value:

```javascript
let score = 10;
score = 11;
```

Here, the number `10` was not transformed into `11`. Numbers are immutable. Instead, the name `score` was rebound to a different number.

### **An object has internal state**

Now consider:

```javascript
const player = { score: 10 };
player.score = 11;
```

The `const` keyword prevents `player` from being rebound:

```javascript
// Not allowed:
player = { score: 12 };
```

However, it does **not** make the object immutable. Its internal `score` property can still be changed.

The distinction is:

| Operation | Meaning |
|---|---|
| Rebinding | Make a name refer to a different value. |
| Mutation | Change the internal state of an existing value. |
| Immutable update | Create a new value containing the requested change. |

Understanding this distinction prevents a common misconception: `const` communicates a stable binding, not a deeply immutable object.

---

## **4. Updating Immutable Data**

If immutable values cannot change, how does an application update its state?

It creates a new state derived from the old one.

### **Updating an object**

```javascript
const user = {
  id: 42,
  name: "Mina",
  role: "reader"
};

const promotedUser = {
  ...user,
  role: "editor"
};
```

The spread syntax copies the top-level properties into a new object, after which `role` is replaced.

### **Updating an array**

```javascript
const tasks = ["design", "implement"];

const withReview = [...tasks, "review"];
const completedFirst = tasks.map((task, index) =>
  index === 0 ? `${task} ✓` : task
);
const withoutImplement = tasks.filter(task => task !== "implement");
```

Each expression returns a new array. The original `tasks` array remains unchanged.

### **Updating nested data**

Nested updates require copying each object along the path being changed:

```javascript
const state = {
  account: {
    profile: {
      displayName: "Ari",
      locale: "en-CA"
    }
  }
};

const nextState = {
  ...state,
  account: {
    ...state.account,
    profile: {
      ...state.account.profile,
      locale: "fr-CA"
    }
  }
};
```

Only three objects are newly created:

1. The root state
2. The account
3. The profile

Unchanged values—such as `displayName`—are reused.

---

## **5. Structural Sharing**

A naïve description of immutability is “copy the entire data structure for every update.” Efficient immutable systems usually do something better: **structural sharing**.

Structural sharing means that a new version reuses unchanged parts of an old version.

Imagine a small tree:

```text
Version A
    root
   /    \
 left   right
        /   \
      R1     R2
```

If only `R2` changes, Version B can reuse `left` and `R1`:

```text
Version A                 Version B
    root-A                    root-B
   /      \                  /      \
 left    right-A  <-------- left    right-B
          /   \                       /   \
        R1     R2                   R1    R2'
```

The arrows are conceptual references. The unchanged nodes are not duplicated.

This has two important consequences:

- Creating a new version can be much cheaper than copying everything.
- Comparing old and new versions can be fast because identical references imply identical subtrees.

For example:

```javascript
console.log(state === nextState); // false
console.log(state.account === nextState.account); // false
console.log(
  state.account.profile === nextState.account.profile
); // false
```

If the state also contained an unchanged `permissions` object, that reference could be shared:

```javascript
console.log(
  state.permissions === nextState.permissions
); // true
```

---

## **6. Persistent Data Structures**

A **persistent data structure** preserves access to its previous versions after an update.

“Persistent” here does not necessarily mean saving data to disk. It means that old versions continue to exist and remain valid.

### **A persistent stack**

A stack can be represented as linked nodes:

```text
top → [C] → [B] → [A] → empty
```

Pushing `D` creates one node that points to the existing stack:

```text
old top ─────→ [C] → [B] → [A] → empty
                ↑
new top → [D] ──┘
```

Both stacks are valid:

- Old stack: `C, B, A`
- New stack: `D, C, B, A`

Here is a compact JavaScript implementation:

```javascript
const EMPTY = null;

function push(stack, value) {
  return Object.freeze({
    value,
    next: stack
  });
}

function pop(stack) {
  if (stack === EMPTY) {
    throw new Error("Cannot pop an empty stack");
  }

  return {
    value: stack.value,
    stack: stack.next
  };
}

const stack1 = push(EMPTY, "A");
const stack2 = push(stack1, "B");
const stack3 = push(stack2, "C");

console.log(pop(stack3).value); // C
console.log(pop(stack2).value); // B
```

Creating `stack3` does not modify `stack2`. Both share the node containing `"A"`, and `stack3` also shares the node containing `"B"`.

### **Common persistent structures**

| Structure | Typical strategy |
|---|---|
| Linked list or stack | Share the unchanged tail. |
| Balanced search tree | Copy nodes along the modified path. |
| Hash map | Use a trie organized by chunks of hash bits. |
| Vector | Use a shallow, wide tree with path copying. |
| Queue | Combine persistent lists with controlled reorganization. |

Production implementations often use sophisticated structures such as hash array mapped tries, relaxed radix balanced trees, and finger trees. The underlying principle remains simple: **copy the path that changed and share everything else**.

---

## **7. Immutability in JavaScript**

JavaScript primitives—numbers, strings, booleans, `null`, `undefined`, `bigint`, and symbols—are immutable. Objects and arrays are mutable.

### **Strings are immutable**

```javascript
let greeting = "hello";

// This does not alter the string:
greeting[0] = "H";

// This rebinds the variable to a newly created string:
greeting = "H" + greeting.slice(1);
```

### **`Object.freeze` is shallow**

```javascript
const config = Object.freeze({
  server: {
    port: 8080
  }
});

// The outer object is frozen, but the nested object is not:
config.server.port = 9090;
```

A recursive development-time helper can freeze nested objects:

```javascript
function deepFreeze(value) {
  if (value === null || typeof value !== "object") {
    return value;
  }

  for (const child of Object.values(value)) {
    deepFreeze(child);
  }

  return Object.freeze(value);
}

const settings = deepFreeze({
  database: {
    host: "localhost",
    port: 5432
  }
});
```

Deep freezing can catch accidental mutation, but it has runtime cost. Many applications use it during development and rely on disciplined update functions or specialized libraries in production.

### **Pure reducer functions**

A reducer accepts a state and an action, then returns the next state:

```javascript
function counterReducer(state, action) {
  switch (action.type) {
    case "increment":
      return {
        ...state,
        count: state.count + 1
      };

    case "rename":
      return {
        ...state,
        label: action.label
      };

    default:
      return state;
  }
}
```

Notice the default case returns the original reference. This lets consumers quickly determine that nothing changed:

```javascript
const unchanged = counterReducer(
  { count: 0, label: "Clicks" },
  { type: "unknown" }
);
```

---

## **8. Immutability in Python**

Python includes both mutable and immutable built-in types.

| Usually immutable | Usually mutable |
|---|---|
| `int`, `float`, `bool` | `list` |
| `str`, `bytes` | `dict` |
| `tuple` | `set` |
| `frozenset` | User-defined objects by default |

### **Frozen data classes**

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class User:
    name: str
    role: str


reader = User(name="Mina", role="reader")
editor = replace(reader, role="editor")

print(reader)  # User(name='Mina', role='reader')
print(editor)  # User(name='Mina', role='editor')
```

The generated class rejects normal field assignment:

```python
# Raises dataclasses.FrozenInstanceError:
reader.role = "admin"
```

### **Frozen does not automatically mean deeply frozen**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Report:
    tags: list[str]


report = Report(tags=["weekly"])
report.tags.append("important")  # This still works.
```

The `Report` prevents rebinding `tags`, but the list itself remains mutable. For deeper immutability, use immutable field types:

```python
@dataclass(frozen=True)
class SafeReport:
    tags: tuple[str, ...]


report = SafeReport(tags=("weekly",))
updated = replace(report, tags=report.tags + ("important",))
```

---

## **9. Concurrency and Predictability**

Shared mutable state creates a coordination problem.

Suppose two tasks update the same balance:

```text
Initial balance: 100

Task A reads 100
Task B reads 100
Task A writes 110
Task B writes 80

Final balance: 80
```

Task A's update is lost. Locks, transactions, atomics, or message passing can prevent this, but the problem exists because multiple tasks are trying to mutate shared state.

Immutable data simplifies the read side:

- Any number of tasks can safely read the same immutable snapshot.
- A task performing a computation sees a consistent version.
- New state can be published as a single replacement.
- Old snapshots remain valid for readers already using them.

Immutability does **not** eliminate all concurrency problems. Something must still decide which new state becomes authoritative. However, it reduces the surface area where synchronization is necessary.

A useful architecture is:

```text
events → single state transition boundary → immutable snapshot → many readers
```

The transition boundary coordinates writes. Readers operate without mutating shared data.

---

## **10. Performance Trade-offs**

Immutability is an engineering trade-off, not a universal commandment.

### **Potential costs**

- More allocations may increase garbage-collection work.
- Naïvely copying large arrays or objects can be expensive.
- Deep updates can become syntactically noisy.
- Some numerical and graphical workloads benefit greatly from in-place mutation.
- Poorly chosen persistent structures may have worse cache locality.

### **Potential gains**

- Structural sharing avoids full copies.
- Reference equality can make change detection fast.
- Memoization becomes safer and more effective.
- Lock-free reads can improve concurrent throughput.
- Fewer defensive copies may be needed at subsystem boundaries.

### **Complexity comparison**

Exact costs depend on the implementation, but a simplified comparison is useful:

| Operation | Full immutable copy | Persistent tree | Mutable structure |
|---|---:|---:|---:|
| Read by index/key | Often `O(1)` | Commonly `O(log n)` with a small base | Often `O(1)` |
| Update | `O(n)` | Commonly `O(log n)` | Often `O(1)` |
| Preserve old version | Yes | Yes | No, unless copied |
| Compare versions | Potentially `O(n)` | Often accelerated by reference checks | Requires tracking or scanning |

Many persistent vectors use wide trees, making their practical depth very small. An operation described as `O(log n)` may traverse only a few nodes even for large collections.

### **A pragmatic rule**

Prefer immutable values for:

- Domain models
- Configuration
- Application state
- Messages and events
- Public API inputs and outputs
- Data shared across threads or tasks

Consider controlled local mutation for:

- Tight numerical loops
- Image, audio, or video buffers
- Large matrix operations
- Internal construction of a value before publication
- Performance-critical code proven by profiling

Mutation is safest when it is **local, short-lived, and unobservable outside a well-defined boundary**.

---

## **11. Practical Design Patterns**

### **Pattern 1: Parse, validate, then freeze**

Construct data in a mutable form, validate it, and publish an immutable representation:

```python
def load_ports(raw_values: list[str]) -> tuple[int, ...]:
    ports: list[int] = []

    for raw in raw_values:
        port = int(raw)
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid port: {port}")
        ports.append(port)

    return tuple(ports)
```

The local list is convenient during construction. The returned tuple prevents callers from changing the published result.

### **Pattern 2: Commands return new state**

```javascript
function addItem(cart, item) {
  const existing = cart.items.find(entry => entry.id === item.id);

  if (existing) {
    return {
      ...cart,
      items: cart.items.map(entry =>
        entry.id === item.id
          ? { ...entry, quantity: entry.quantity + 1 }
          : entry
      )
    };
  }

  return {
    ...cart,
    items: [...cart.items, { ...item, quantity: 1 }]
  };
}
```

The caller receives the state transition explicitly:

```javascript
const nextCart = addItem(currentCart, {
  id: "book-7",
  name: "Algorithms"
});
```

### **Pattern 3: Keep a history**

Persistent versions make undo straightforward:

```javascript
function commit(history, nextState) {
  return {
    past: [...history.past, history.present],
    present: nextState,
    future: []
  };
}

function undo(history) {
  if (history.past.length === 0) {
    return history;
  }

  const previous = history.past.at(-1);

  return {
    past: history.past.slice(0, -1),
    present: previous,
    future: [history.present, ...history.future]
  };
}
```

### **Pattern 4: Memoize pure computations**

```javascript
function memoizeOne(fn) {
  let hasValue = false;
  let lastInput;
  let lastOutput;

  return input => {
    if (hasValue && input === lastInput) {
      return lastOutput;
    }

    hasValue = true;
    lastInput = input;
    lastOutput = fn(input);
    return lastOutput;
  };
}

const totalPrice = memoizeOne(cart =>
  cart.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )
);
```

This strategy depends on a clear contract: if the cart reference is unchanged, its contents must also be unchanged. Immutability provides that contract.

---

## **12. Common Mistakes**

### **Mistake 1: Making only the outer object immutable**

```javascript
const state = Object.freeze({
  users: [{ name: "Lee" }]
});

state.users[0].name = "Kai"; // Nested mutation is still possible.
```

Use immutable nested values, deep freezing during development, or a library that enforces safe updates.

### **Mistake 2: Mutating before returning**

```javascript
function rename(user, name) {
  user.name = name;
  return user;
}
```

Returning the object does not make the operation immutable. The input was still changed.

Correct:

```javascript
function rename(user, name) {
  return { ...user, name };
}
```

### **Mistake 3: Copying too little**

```javascript
const next = { ...state };
next.profile.name = "New Name";
```

The root is copied, but `next.profile` and `state.profile` still refer to the same object.

Correct:

```javascript
const next = {
  ...state,
  profile: {
    ...state.profile,
    name: "New Name"
  }
};
```

### **Mistake 4: Copying everything**

Serialization is sometimes used as a crude deep-copy mechanism:

```javascript
const copy = JSON.parse(JSON.stringify(value));
```

This approach:

- Loses unsupported values such as `undefined`
- Converts dates into strings
- Fails on cyclic references
- Discards prototypes and specialized object behavior
- Copies unchanged data unnecessarily

Prefer deliberate updates or a well-tested immutable data library.

### **Mistake 5: Assuming immutability guarantees purity**

A function can avoid mutating its input and still have side effects:

```javascript
function calculateTotal(cart) {
  console.log("Calculating"); // Side effect
  return cart.items.reduce((sum, item) => sum + item.price, 0);
}
```

Immutability is one ingredient of pure functions, not the entire definition. A pure function must also produce the same output for the same input and avoid externally observable side effects.

---

## **13. Exercises**

### **Exercise 1: Immutable array update**

Write a function that marks a task as complete without modifying the original array.

```javascript
const tasks = [
  { id: 1, title: "Read", completed: false },
  { id: 2, title: "Practice", completed: false }
];

function completeTask(tasks, taskId) {
  // Your implementation
}
```

<details>
<summary><strong>Solution</strong></summary>

```javascript
function completeTask(tasks, taskId) {
  return tasks.map(task =>
    task.id === taskId
      ? { ...task, completed: true }
      : task
  );
}
```

</details>

### **Exercise 2: Verify structural sharing**

Given the solution above, predict each result:

```javascript
const updated = completeTask(tasks, 2);

console.log(updated === tasks);
console.log(updated[0] === tasks[0]);
console.log(updated[1] === tasks[1]);
```

<details>
<summary><strong>Solution</strong></summary>

```text
false  — the array is new
true   — the unchanged first task is shared
false  — the updated second task is new
```

</details>

### **Exercise 3: Persistent stack**

Add a `peek` function and a generator that iterates through the persistent stack:

```javascript
function peek(stack) {
  // Your implementation
}

function* values(stack) {
  // Your implementation
}
```

<details>
<summary><strong>Solution</strong></summary>

```javascript
function peek(stack) {
  if (stack === EMPTY) {
    throw new Error("Cannot peek at an empty stack");
  }

  return stack.value;
}

function* values(stack) {
  let current = stack;

  while (current !== EMPTY) {
    yield current.value;
    current = current.next;
  }
}
```

</details>

### **Exercise 4: Reason about boundaries**

For each scenario, decide whether immutable data, controlled mutation, or a combination is most appropriate:

1. A user account record shared across HTTP request handlers
2. A pixel buffer being updated 60 times per second
3. A compiler's abstract syntax tree
4. A local list used only while parsing one CSV row
5. State snapshots for an undoable text editor

There is no single correct answer, but a strong design should explain:

- Who owns the data
- How long it lives
- Whether it is shared
- Whether history is valuable
- Whether profiling shows allocation or copying to be significant

---

## **14. Summary**

Immutability changes the central question of state management.

Instead of asking:

> “Who changed this object?”

an immutable design encourages:

> “Which operation produced this new version?”

The core ideas are:

- **Immutable values do not change after creation.**
- **Rebinding a variable is different from mutating an object.**
- **Updates create new values while preserving old ones.**
- **Structural sharing reuses unchanged data.**
- **Persistent data structures retain earlier versions efficiently.**
- **Immutability improves predictability, testing, caching, and concurrent reading.**
- **Controlled local mutation can still be appropriate when performance or construction ergonomics justify it.**

The most effective systems rarely treat immutability as an absolute ideology. They use it as a boundary-setting tool: mutable implementation details may exist locally, while published state, shared data, and domain values remain stable and trustworthy.

---

### **Further Exploration**

Once these fundamentals are comfortable, useful next topics include:

- Pure functions and referential transparency
- Functional lenses for nested updates
- Hash array mapped tries
- Event sourcing
- Copy-on-write memory
- Ownership and borrowing in Rust
- Actor-based concurrency
- Immutable application architecture

