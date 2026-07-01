# **Memoization: Trading Memory for Speed**

> A practical guide to caching function results, recognizing suitable problems, and avoiding common implementation mistakes.

---

## **Table of Contents**

1. [What Is Memoization?](#1-what-is-memoization)
2. [Why It Improves Performance](#2-why-it-improves-performance)
3. [Building a Memoized Function](#3-building-a-memoized-function)
4. [Memoization and Dynamic Programming](#4-memoization-and-dynamic-programming)
5. [Design Constraints and Common Pitfalls](#5-design-constraints-and-common-pitfalls)
6. [When to Use Memoization](#6-when-to-use-memoization)
7. [Practice Exercise](#7-practice-exercise)
8. [Summary](#8-summary)

---

## **1. What Is Memoization?**

**Memoization** is an optimization technique that stores the result of an expensive function call and reuses that result when the function is called again with the same input.

The idea is simple:

1. Receive an input.
2. Check whether its result is already cached.
3. Return the cached result if it exists.
4. Otherwise, compute the result, cache it, and return it.

Conceptually, a memoized function behaves like this:

```text
function memoized(input):
    if input exists in cache:
        return cache[input]

    result = expensiveCalculation(input)
    cache[input] = result
    return result
```

Memoization is most reliable when applied to a **pure function**: a function whose output depends only on its arguments and which produces no observable side effects.

```javascript
// Pure: the same input always produces the same output.
function square(number) {
  return number * number;
}
```

By contrast, this function is not a safe memoization candidate:

```javascript
function currentGreeting(name) {
  return `Hello, ${name}. The time is ${new Date().toISOString()}.`;
}
```

Its result depends on the current time, not just `name`. Caching by name would return stale timestamps.

---

## **2. Why It Improves Performance**

Consider the recursive Fibonacci function:

```javascript
function fibonacci(n) {
  if (n <= 1) {
    return n;
  }

  return fibonacci(n - 1) + fibonacci(n - 2);
}
```

This definition closely matches the mathematical recurrence, but it repeatedly solves the same subproblems. Calculating `fibonacci(5)` produces a call tree like this:

```text
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2)
│   │   └── fib(1)
│   └── fib(2)
└── fib(3)
    ├── fib(2)
    └── fib(1)
```

`fib(3)` and `fib(2)` are evaluated multiple times. As `n` grows, this duplication becomes severe.

| Implementation | Approximate Time Complexity | Space Complexity | Main Trade-off |
|---|---:|---:|---|
| Naive recursion | `O(2^n)` | `O(n)` call stack | Simple, but extremely slow |
| Memoized recursion | `O(n)` | `O(n)` | Uses cache memory |
| Iterative solution | `O(n)` | `O(1)` | Fastest storage profile, less recurrence-like |

Memoization reduces the recursive algorithm to approximately `O(n)` time because each distinct Fibonacci value is computed only once.

> **Core principle:** Memoization helps when repeated calls use the same inputs and the saved computation costs more than cache lookup and storage.

---

## **3. Building a Memoized Function**

### **3.1 A direct implementation**

Here is a memoized Fibonacci function in JavaScript:

```javascript
function fibonacci(n, cache = new Map()) {
  if (!Number.isInteger(n) || n < 0) {
    throw new RangeError("n must be a non-negative integer");
  }

  if (n <= 1) {
    return n;
  }

  if (cache.has(n)) {
    return cache.get(n);
  }

  const result =
    fibonacci(n - 1, cache) +
    fibonacci(n - 2, cache);

  cache.set(n, result);
  return result;
}

console.log(fibonacci(40)); // 102334155
```

The order of operations matters:

- Validate the input.
- Handle base cases.
- check the cache.
- Compute only when necessary.
- Store the completed result before returning it.

Using `cache.has(n)` is safer than checking whether `cache.get(n)` is truthy because valid cached values may be `0`, `false`, `""`, or `undefined`.

### **3.2 A reusable memoization wrapper**

Memoization can also be separated from the target function:

```javascript
function memoize(fn) {
  const cache = new Map();

  return function memoized(...args) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const slowMultiply = (a, b) => {
  console.log("Computing...");
  return a * b;
};

const multiply = memoize(slowMultiply);

console.log(multiply(6, 7)); // Logs "Computing...", then 42
console.log(multiply(6, 7)); // Returns cached 42
```

This wrapper demonstrates the general pattern, but `JSON.stringify` is not a universal cache-key strategy. It can mishandle values such as functions, cyclic objects, and objects whose property insertion orders differ.

### **3.3 Memoization in Python**

Python provides a standard decorator for this pattern:

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(40))       # 102334155
print(fibonacci.cache_info())
```

`lru_cache` means **Least Recently Used cache**. When `maxsize` is limited, older entries are removed as new entries are added.

```python
@lru_cache(maxsize=256)
def load_product(product_id: int):
    ...
```

A bounded cache is often safer in a long-running process because it prevents unlimited memory growth.

---

## **4. Memoization and Dynamic Programming**

Memoization is commonly described as the **top-down** form of dynamic programming.

- **Top-down memoization** starts with the full problem and recursively requests smaller solutions.
- **Bottom-up tabulation** starts with known base cases and iteratively builds larger solutions.

For Fibonacci numbers, the two approaches look like this:

```python
# Top-down memoization
from functools import lru_cache


@lru_cache(maxsize=None)
def fib_top_down(n):
    if n <= 1:
        return n
    return fib_top_down(n - 1) + fib_top_down(n - 2)
```

```python
# Bottom-up tabulation
def fib_bottom_up(n):
    if n <= 1:
        return n

    previous, current = 0, 1

    for _ in range(2, n + 1):
        previous, current = current, previous + current

    return current
```

| Property | Top-Down Memoization | Bottom-Up Tabulation |
|---|---|---|
| Control flow | Recursive | Iterative |
| Computes | Only requested states | Usually all preceding states |
| Stack usage | May be significant | Usually constant |
| Natural fit | Recursive problem definitions | Predictable dependency order |
| Debugging | Can involve deep call stacks | Often straightforward |

Memoization is especially useful when only a subset of possible states will actually be visited. Tabulation can be more efficient when every preceding state is required and the dependency order is clear.

---

## **5. Design Constraints and Common Pitfalls**

### **5.1 Unbounded cache growth**

A cache consumes memory. If inputs are effectively unique, memoization may keep accumulating entries without producing many hits.

```javascript
const cache = new Map();

function processUniqueRequest(requestId) {
  // If requestId never repeats, this cache only grows.
}
```

Possible controls include:

- A maximum entry count
- A time-to-live, or **TTL**
- Least-recently-used eviction
- Manual invalidation
- Per-request rather than process-wide cache scope

### **5.2 Stale data**

Caching a database query can return outdated information after the underlying record changes.

```text
read product 42 → cache result
update product 42 in database
read product 42 → stale cached result
```

Cache invalidation must be part of the design:

```javascript
async function updateProduct(id, changes) {
  const updated = await database.products.update(id, changes);
  productCache.delete(id);
  return updated;
}
```

### **5.3 Incorrect cache keys**

For a function with multiple arguments, the cache key must uniquely represent the entire input:

```javascript
function makeKey(userId, locale) {
  return `${userId}:${locale}`;
}
```

Even this can be ambiguous if the values may contain the delimiter. Nested maps or a robust serialization scheme may be safer.

### **5.4 Mutable inputs**

Object identity and object content are different concepts:

```javascript
const settings = { theme: "dark" };
const cache = new Map();

cache.set(settings, "computed result");
settings.theme = "light";

// The Map still sees the same object key,
// although its meaningful content has changed.
console.log(cache.get(settings));
```

Prefer immutable inputs, stable identifiers, or carefully constructed content-based keys.

### **5.5 Caching failures**

When memoizing asynchronous work, decide whether rejected promises should remain cached:

```javascript
function memoizeAsync(fn) {
  const cache = new Map();

  return function (key) {
    if (!cache.has(key)) {
      const promise = fn(key).catch((error) => {
        cache.delete(key); // Permit a later retry.
        throw error;
      });

      cache.set(key, promise);
    }

    return cache.get(key);
  };
}
```

Caching the in-flight promise has an additional benefit: concurrent callers requesting the same key can share one operation instead of triggering duplicate work.

---

## **6. When to Use Memoization**

Memoization is a strong candidate when all or most of these conditions hold:

- The function is deterministic.
- The function is expensive relative to a cache lookup.
- Inputs repeat often.
- Results can be retained within an acceptable memory budget.
- Cached values do not become stale, or invalidation is well defined.

Good use cases include:

- Recursive algorithms with overlapping subproblems
- Parsing or transforming repeatedly used immutable data
- Expensive UI-derived calculations
- Repeated graph searches from the same state
- Deduplicating concurrent network requests

Memoization is usually a poor fit when:

- Inputs rarely repeat.
- The calculation is already cheap.
- Results depend on time, randomness, external state, or side effects.
- Inputs are large and expensive to serialize.
- Correct cache invalidation is more complex than recomputation.

Before adding memoization, measure the workload. A useful metric is the **cache hit rate**:

```text
hit rate = cache hits / total cache lookups
```

A low hit rate combined with a large cache often indicates wasted memory and added complexity.

---

## **7. Practice Exercise**

Suppose a robot can move either one or two steps at a time. Write a function that returns the number of distinct ways it can reach step `n`.

For example:

```text
n = 3

1 + 1 + 1
1 + 2
2 + 1

answer = 3
```

Start with this recursive definition:

```javascript
function countWays(n) {
  if (n < 0) return 0;
  if (n === 0) return 1;

  return countWays(n - 1) + countWays(n - 2);
}
```

Then add memoization:

```javascript
function countWays(n, cache = new Map()) {
  if (n < 0) return 0;
  if (n === 0) return 1;

  if (cache.has(n)) {
    return cache.get(n);
  }

  const result =
    countWays(n - 1, cache) +
    countWays(n - 2, cache);

  cache.set(n, result);
  return result;
}

console.log(countWays(3));  // 3
console.log(countWays(10)); // 89
```

To extend the exercise:

1. Support moves of one, two, or three steps.
2. Implement a bottom-up version.
3. Compare execution times for large inputs.
4. Count cache hits and misses.

---

## **8. Summary**

Memoization stores previously computed results so repeated calls can avoid repeated work. It can transform algorithms with severe redundant computation—such as naive recursive Fibonacci—from exponential time to linear time.

The technique is effective when:

- outputs depend only on inputs,
- the same inputs recur,
- computation is meaningfully expensive, and
- cache lifetime and memory use are controlled.

The implementation pattern is small, but production-quality memoization requires deliberate decisions about **cache keys**, **eviction**, **invalidation**, **mutable values**, and **error handling**. Treat the cache as part of the algorithm's correctness and resource model, not merely as an optional speed boost.

---

> **Key takeaway:** Memoization does not make computation disappear; it performs computation once, stores the answer, and pays with memory to avoid doing the same work again.
