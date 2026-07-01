# **Immutability and Persistent Data Structures**

> A practical guide to representing change without modifying existing values.

## **Table of Contents**

1. [Why Immutability Matters](#1-why-immutability-matters)
2. [Values, References, and Mutation](#2-values-references-and-mutation)
3. [Writing Immutable JavaScript](#3-writing-immutable-javascript)
4. [Persistent Data Structures](#4-persistent-data-structures)
5. [Structural Sharing in Practice](#5-structural-sharing-in-practice)
6. [Immutable State Updates](#6-immutable-state-updates)
7. [Benefits and Trade-offs](#7-benefits-and-trade-offs)
8. [Practical Guidelines](#8-practical-guidelines)
9. [Exercises](#9-exercises)
10. [Summary](#10-summary)

---

## **1. Why Immutability Matters**

**Immutability** means that a value cannot change after it has been created. Instead
of modifying an existing value, a program creates a new value that represents the
desired result.

Consider a shopping cart. A mutable update changes the original cart:

```javascript
const cart = ["book", "pen"];
cart.push("notebook");

console.log(cart); // ["book", "pen", "notebook"]
```

An immutable update leaves the original cart untouched:

```javascript
const cart = ["book", "pen"];
const updatedCart = [...cart, "notebook"];

console.log(cart);        // ["book", "pen"]
console.log(updatedCart); // ["book", "pen", "notebook"]
```

This distinction becomes valuable when state is shared across functions, user
interface components, asynchronous operations, or concurrent tasks. If an existing
value never changes, every consumer can safely reason about the value it received.

### **A useful mental model**

Think of immutable values as snapshots:

```text
cart_v1 = ["book", "pen"]
cart_v2 = ["book", "pen", "notebook"]
cart_v3 = ["book", "notebook"]
```

Each snapshot remains valid. A later version does not silently rewrite history.

---

## **2. Values, References, and Mutation**

Understanding immutability requires distinguishing a value from a reference to that
value.

### **Primitive values**

JavaScript primitives—such as numbers, strings, and booleans—behave immutably:

```javascript
let score = 10;
let previousScore = score;

score = score + 5;

console.log(score);         // 15
console.log(previousScore); // 10
```

The number `10` was not altered. The variable `score` was assigned a different
number.

### **Objects and arrays**

Objects and arrays are accessed through references. Two variables can point to the
same object:

```javascript
const originalUser = {
  name: "Mira",
  preferences: {
    theme: "dark"
  }
};

const alias = originalUser;
alias.preferences.theme = "light";

console.log(originalUser.preferences.theme); // "light"
```

Changing `alias` appears to change `originalUser` because both names refer to the
same underlying object.

### **Shallow copying is not deep copying**

The spread operator creates a new outer object, but nested references remain shared:

```javascript
const originalUser = {
  name: "Mira",
  preferences: {
    theme: "dark"
  }
};

const shallowCopy = { ...originalUser };
shallowCopy.preferences.theme = "light";

console.log(originalUser.preferences.theme); // "light"
```

To update a nested property immutably, copy every object along the path:

```javascript
const updatedUser = {
  ...originalUser,
  preferences: {
    ...originalUser.preferences,
    theme: "solarized"
  }
};
```

Now the objects have the following relationships:

```text
originalUser ──► old preferences { theme: "light" }
updatedUser  ──► new preferences { theme: "solarized" }
```

---

## **3. Writing Immutable JavaScript**

Many common mutations have direct immutable alternatives.

| Goal | Mutable operation | Immutable alternative |
|---|---|---|
| Add an array item | `items.push(x)` | `[...items, x]` |
| Remove an array item | `items.splice(i, 1)` | `items.filter((_, n) => n !== i)` |
| Replace an array item | `items[i] = x` | `items.map((v, n) => n === i ? x : v)` |
| Add an object field | `obj.key = value` | `{ ...obj, key: value }` |
| Remove an object field | `delete obj.key` | object rest syntax |
| Change a nested field | direct assignment | copy each level with spread |
| Sort an array | `items.sort()` | `items.toSorted()` or `[...items].sort()` |
| Reverse an array | `items.reverse()` | `items.toReversed()` or `[...items].reverse()` |

### **Adding and removing array elements**

```javascript
const tasks = [
  { id: 1, title: "Write tests" },
  { id: 2, title: "Review changes" }
];

const withNewTask = [
  ...tasks,
  { id: 3, title: "Deploy release" }
];

const withoutFirstTask = withNewTask.filter(task => task.id !== 1);
```

Neither operation modifies `tasks`.

### **Updating one array element**

```javascript
const completedTasks = tasks.map(task =>
  task.id === 2
    ? { ...task, completed: true }
    : task
);
```

Only the matching item is copied. Every unchanged item keeps its original reference.
That detail is important for both efficiency and change detection.

### **Removing an object property**

```javascript
const account = {
  id: 42,
  name: "Asha",
  temporaryToken: "secret"
};

const { temporaryToken, ...publicAccount } = account;

console.log(publicAccount);
// { id: 42, name: "Asha" }
```

### **`const` does not make objects immutable**

`const` prevents reassignment of the variable; it does not freeze the referenced
object:

```javascript
const settings = { sound: true };
settings.sound = false; // Allowed

// settings = { sound: true }; // TypeError: reassignment is forbidden
```

For runtime enforcement, JavaScript provides `Object.freeze`:

```javascript
const settings = Object.freeze({
  sound: true,
  language: "en"
});

settings.sound = false; // Fails in strict mode; otherwise has no effect
```

However, `Object.freeze` is shallow:

```javascript
const config = Object.freeze({
  database: {
    host: "localhost"
  }
});

config.database.host = "production.example"; // Nested object is still mutable
```

---

## **4. Persistent Data Structures**

Copying an entire large structure for every update would be expensive. A
**persistent data structure** solves this by reusing unchanged parts of previous
versions. This technique is called **structural sharing**.

Suppose a binary tree contains seven nodes:

```text
             8
           /   \
          4     12
         / \    / \
        2   6  10  14
```

To replace `6` with `7`, a persistent tree creates only the nodes on the path from
the root to the changed value:

```text
Old version:                 New version:

       8                            8'
      / \                          /  \
     4   12                       4'   12  ◄── shared
    / \                          / \
   2   6                        2   7
   ▲                            ▲
   └──────── shared ────────────┘
```

The new tree reuses node `2` and the entire subtree rooted at `12`. The old tree
continues to reference node `6`, so both versions remain usable.

### **Persistence does not mean disk storage**

In this context, *persistent* means that previous versions remain available after
an update. It does not necessarily mean that data is saved to a database or file.

### **Common implementations**

Production immutable collections often rely on specialized structures:

- **Linked lists**, where a new head can reuse the existing tail.
- **Hash array mapped tries (HAMTs)**, used for efficient immutable maps and sets.
- **Relaxed radix balanced trees**, used for efficient immutable vectors.
- **Balanced search trees**, used for sorted immutable maps and sets.

These structures usually update only a small path rather than cloning every element.

---

## **5. Structural Sharing in Practice**

A persistent singly linked list is one of the clearest demonstrations of structural
sharing.

```javascript
const empty = null;

function prepend(value, list) {
  return Object.freeze({
    value,
    next: list
  });
}

const listA = prepend(3, empty);
const listB = prepend(2, listA);
const listC = prepend(1, listB);
```

The resulting structure is:

```text
listC ──► [1] ──► [2] ──► [3] ──► null
                   ▲       ▲
listB ─────────────┘       │
listA ─────────────────────┘
```

Every list is a valid version:

```javascript
function toArray(list) {
  const result = [];
  let current = list;

  while (current !== null) {
    result.push(current.value);
    current = current.next;
  }

  return result;
}

console.log(toArray(listA)); // [3]
console.log(toArray(listB)); // [2, 3]
console.log(toArray(listC)); // [1, 2, 3]
```

Prepending takes constant time, **O(1)**, because it creates exactly one new node.
The rest of the list is shared.

### **A persistent binary search tree**

The same idea can be applied recursively:

```javascript
function insert(node, value) {
  if (node === null) {
    return Object.freeze({
      value,
      left: null,
      right: null
    });
  }

  if (value === node.value) {
    return node;
  }

  if (value < node.value) {
    return Object.freeze({
      ...node,
      left: insert(node.left, value)
    });
  }

  return Object.freeze({
    ...node,
    right: insert(node.right, value)
  });
}

let tree = null;
tree = insert(tree, 8);
tree = insert(tree, 4);
tree = insert(tree, 12);

const oldTree = tree;
const newTree = insert(tree, 6);

console.log(oldTree.left.right); // null
console.log(newTree.left.right.value); // 6
console.log(oldTree.right === newTree.right); // true: structurally shared
```

For a balanced tree with `n` nodes, insertion typically creates **O(log n)** new
nodes and shares everything else.

---

## **6. Immutable State Updates**

Immutability is especially useful in applications whose behavior depends on a
sequence of state transitions.

### **Reducer pattern**

A reducer is a pure function that accepts the current state and an action, then
returns the next state:

```javascript
function reducer(state, action) {
  switch (action.type) {
    case "task/added":
      return {
        ...state,
        tasks: [
          ...state.tasks,
          {
            id: action.id,
            title: action.title,
            completed: false
          }
        ]
      };

    case "task/completed":
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.id
            ? { ...task, completed: true }
            : task
        )
      };

    default:
      return state;
  }
}
```

Using it produces an explicit history:

```javascript
const state0 = { tasks: [] };

const state1 = reducer(state0, {
  type: "task/added",
  id: 1,
  title: "Learn persistent structures"
});

const state2 = reducer(state1, {
  type: "task/completed",
  id: 1
});

console.log(state0.tasks.length);           // 0
console.log(state1.tasks[0].completed);     // false
console.log(state2.tasks[0].completed);     // true
```

### **Undo and redo**

Because previous snapshots remain unchanged, implementing undo can be simple:

```javascript
function createHistory(initialState) {
  return {
    past: [],
    present: initialState,
    future: []
  };
}

function applyChange(history, nextState) {
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

No reverse mutation is required. Undo simply selects an earlier snapshot.

### **Reference equality as a change signal**

Immutable updates make reference comparisons meaningful:

```javascript
const before = {
  profile: { name: "Niko" },
  notifications: ["Welcome"]
};

const after = {
  ...before,
  notifications: [...before.notifications, "Build complete"]
};

console.log(before === after);                       // false
console.log(before.profile === after.profile);       // true
console.log(before.notifications === after.notifications); // false
```

A system can quickly determine that `profile` did not change while `notifications`
did. Many user interface frameworks and state libraries use this property to avoid
unnecessary work.

---

## **7. Benefits and Trade-offs**

Immutability is a tool, not a universal rule. Its value depends on the problem.

| Property | Advantage | Cost or limitation |
|---|---|---|
| Predictability | Existing values cannot change unexpectedly | Updates require a different coding style |
| Debugging | Earlier snapshots remain inspectable | Long histories can retain memory |
| Equality checks | Reference equality can reveal changed branches | Correct copying discipline is required |
| Concurrency | Readers can safely share stable values | Some workloads need carefully optimized structures |
| Testing | Pure transformations are easy to isolate | External effects still require separate handling |
| Undo/redo | Previous states are naturally available | History management needs explicit limits |

### **Memory considerations**

Naively deep-cloning a structure on every update can waste substantial memory:

```javascript
// Usually inappropriate for frequent state updates:
const clone = structuredClone(largeState);
clone.user.preferences.theme = "dark";
```

Structural sharing avoids most duplication. However, keeping a reference to an old
root also keeps every node reachable from that root alive. Applications with
unbounded histories should prune or compact old versions.

### **Performance considerations**

Immutability is often efficient when:

- Updates touch a small portion of a large structure.
- Reads greatly outnumber writes.
- Reference equality avoids expensive deep comparisons.
- Specialized persistent collections are used for very large datasets.

Mutation may be appropriate inside a tightly controlled local algorithm:

```javascript
function sum(values) {
  let total = 0;

  for (const value of values) {
    total += value;
  }

  return total;
}
```

The local variable `total` mutates, but that mutation is encapsulated and cannot be
observed by callers. A pragmatic design often combines immutable public state with
carefully contained local mutation.

---

## **8. Practical Guidelines**

### **1. Treat shared state as immutable**

Values passed among components, services, or asynchronous operations are strong
candidates for immutable handling.

### **2. Copy only the changed path**

Preserve references to unchanged branches:

```javascript
function renameProject(state, projectId, newName) {
  return {
    ...state,
    projects: state.projects.map(project =>
      project.id === projectId
        ? { ...project, name: newName }
        : project
    )
  };
}
```

### **3. Keep transformations pure**

A pure function neither mutates its inputs nor performs observable side effects:

```javascript
function applyDiscount(product, percentage) {
  return {
    ...product,
    price: product.price * (1 - percentage / 100)
  };
}
```

Given the same inputs, it returns the same output.

### **4. Enforce the rule where practical**

Useful options include:

- `Object.freeze` during development.
- Read-only types in TypeScript.
- Linters that detect mutation.
- Libraries such as Immer or Immutable.js.
- Encapsulation that prevents direct access to internal mutable data.

TypeScript can express read-only intent:

```typescript
type User = Readonly<{
  id: number;
  name: string;
  roles: readonly string[];
}>;

function addRole(user: User, role: string): User {
  return {
    ...user,
    roles: [...user.roles, role]
  };
}
```

### **5. Avoid accidental mutation through APIs**

Some built-in methods mutate their receiver:

```javascript
const numbers = [3, 1, 2];

const unsafe = numbers.sort();          // Mutates numbers
const safeA = [...numbers].sort();       // Sorts a copy
const safeB = numbers.toSorted();        // Modern immutable alternative
```

Check whether an unfamiliar method returns a new value or changes the existing one.

---

## **9. Exercises**

### **Exercise 1: Toggle a task**

Implement `toggleTask` so that it returns a new array and copies only the matching
task:

```javascript
function toggleTask(tasks, id) {
  // Your implementation
}

const tasks = [
  { id: 1, title: "Read", completed: false },
  { id: 2, title: "Practice", completed: false }
];

const updated = toggleTask(tasks, 2);
```

Expected properties:

```javascript
console.log(updated !== tasks);                  // true
console.log(updated[0] === tasks[0]);            // true
console.log(updated[1] !== tasks[1]);            // true
console.log(updated[1].completed);               // true
```

<details>
<summary><strong>Solution</strong></summary>

```javascript
function toggleTask(tasks, id) {
  return tasks.map(task =>
    task.id === id
      ? { ...task, completed: !task.completed }
      : task
  );
}
```

</details>

### **Exercise 2: Update nested configuration**

Write an immutable update that changes only the port:

```javascript
const config = {
  appName: "Atlas",
  server: {
    host: "localhost",
    connection: {
      port: 3000,
      secure: false
    }
  }
};
```

<details>
<summary><strong>Solution</strong></summary>

```javascript
const updatedConfig = {
  ...config,
  server: {
    ...config.server,
    connection: {
      ...config.server.connection,
      port: 8080
    }
  }
};
```

</details>

### **Exercise 3: Verify structural sharing**

Using the configuration from Exercise 2, predict the results:

```javascript
console.log(config === updatedConfig);
console.log(config.server === updatedConfig.server);
console.log(
  config.server.connection === updatedConfig.server.connection
);
console.log(config.appName === updatedConfig.appName);
```

<details>
<summary><strong>Answer</strong></summary>

```text
false
false
false
true
```

The first three comparisons involve objects along the changed path, so they have new
references. The final comparison involves an unchanged primitive value.

</details>

---

## **10. Summary**

**Immutability** represents change by creating new values instead of altering
existing ones. It improves predictability, supports reliable history, simplifies
testing, and makes reference equality useful for detecting changes.

**Persistent data structures** make immutable updates efficient through
**structural sharing**: new versions copy only the changed path and reuse unchanged
branches from older versions.

The key practices are:

1. Do not mutate shared inputs.
2. Return a new root value when state changes.
3. Copy every object or array along the changed path.
4. Reuse unchanged branches.
5. Keep mutation local and unobservable when it provides a clear performance or
   implementation benefit.

Once these rules become familiar, immutable code stops feeling like defensive
copying and starts functioning as a precise model of state over time.
