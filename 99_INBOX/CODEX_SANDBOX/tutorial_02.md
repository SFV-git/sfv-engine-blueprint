# **Memoization: Trading Memory for Speed**

> A practical guide to eliminating repeated work with caches, recursion, and dynamic programming.

---

## **Table of Contents**

1. [The Core Idea](#1-the-core-idea)
2. [Why Repeated Work Becomes Expensive](#2-why-repeated-work-becomes-expensive)
3. [Building Memoization by Hand](#3-building-memoization-by-hand)
4. [Using Language-Level Cache Tools](#4-using-language-level-cache-tools)
5. [Memoization and Dynamic Programming](#5-memoization-and-dynamic-programming)
6. [Cache Design and Correctness](#6-cache-design-and-correctness)
7. [Performance Analysis](#7-performance-analysis)
8. [Practical Examples](#8-practical-examples)
9. [Common Mistakes](#9-common-mistakes)
10. [When Memoization Is the Wrong Tool](#10-when-memoization-is-the-wrong-tool)
11. [Exercises](#11-exercises)
12. [Summary and Reference](#12-summary-and-reference)

---

## **1. The Core Idea**

**Memoization** is an optimization technique in which a program stores the result of an expensive function call and reuses that result when the same inputs appear again.

The basic process is:

1. Convert the function's inputs into a stable **cache key**.
2. Check whether that key already has a stored result.
3. Return the stored result if it exists.
4. Otherwise, compute the result, store it, and return it.

In pseudocode:

```text
function memoized_operation(input):
    if input exists in cache:
        return cache[input]

    result = expensive_operation(input)
    cache[input] = result
    return result
```

Memoization is useful when all three of the following are true:

- A function is called repeatedly with identical inputs.
- Computing its result is expensive.
- The same inputs always produce the same reusable result.

The final condition is crucial. A function that reads the current time, queries changing external data, or modifies hidden state cannot be cached safely without additional rules.

### **Memoization in one sentence**

> **Do the work once per distinct input, then remember the answer.**

---

## **2. Why Repeated Work Becomes Expensive**

Consider the mathematical Fibonacci sequence:

```text
F(0) = 0
F(1) = 1
F(n) = F(n - 1) + F(n - 2)
```

A direct recursive translation is easy to read:

```python
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Unfortunately, this implementation repeatedly solves the same subproblems. Calculating `fibonacci(5)` produces a call tree resembling this:

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

Notice that `fib(3)` and `fib(2)` appear more than once. For larger values, that duplication grows dramatically.

| Implementation | Time complexity | Extra space | Work performed |
|---|---:|---:|---|
| Naive recursion | `O(2^n)` | `O(n)` call stack | Repeats overlapping subproblems |
| Memoized recursion | `O(n)` | `O(n)` cache + stack | Solves each value once |
| Iterative solution | `O(n)` | `O(1)` | Solves each value once |

Memoization changes the recursive solution from exponential time to linear time because only `n + 1` distinct Fibonacci inputs exist between `0` and `n`.

### **Overlapping subproblems**

A problem has **overlapping subproblems** when its solution repeatedly depends on the same smaller problems. Fibonacci is the classic teaching example, but the pattern also appears in:

- Pathfinding and graph traversal
- Parsing and pattern matching
- Sequence alignment
- Combinatorial counting
- Game-tree evaluation
- Pricing and configuration rules
- Recursive document or dependency analysis

---

## **3. Building Memoization by Hand**

Writing the cache explicitly makes every part of the technique visible.

```python
def fibonacci(n: int, cache: dict[int, int] | None = None) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")

    if cache is None:
        cache = {}

    if n in cache:
        return cache[n]

    if n < 2:
        result = n
    else:
        result = fibonacci(n - 1, cache) + fibonacci(n - 2, cache)

    cache[n] = result
    return result
```

This implementation has four important parts:

1. **Validation** prevents unsupported inputs.
2. **Lookup** avoids repeated computation.
3. **Computation** occurs only after a cache miss.
4. **Storage** makes the result available to later calls.

### **Why use `cache is None`?**

The following version looks shorter but is usually a mistake:

```python
# Avoid this unless a shared, persistent cache is explicitly intended.
def fibonacci(n: int, cache: dict[int, int] = {}) -> int:
    ...
```

Python creates default argument objects once, when the function is defined. Every later call would share the same dictionary. Shared caching can be useful, but hiding it inside a mutable default makes lifetime, tests, and memory usage harder to reason about.

### **A reusable memoization decorator**

Python functions are values, so a decorator can add caching to many functions:

```python
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

R = TypeVar("R")


def memoize(function: Callable[..., R]) -> Callable[..., R]:
    cache: dict[tuple[Any, ...], R] = {}

    @wraps(function)
    def wrapper(*args: Any) -> R:
        if args not in cache:
            cache[args] = function(*args)
        return cache[args]

    return wrapper


@memoize
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

This simplified decorator has limitations:

- Every argument must be hashable.
- Keyword arguments are unsupported.
- The cache grows without a size limit.
- It provides no invalidation mechanism.
- Concurrent access has not been considered.

Those limitations illustrate an important engineering principle: **the algorithm is simple, but production cache policy is not**.

---

## **4. Using Language-Level Cache Tools**

Python's standard library provides robust memoization decorators in `functools`.

### **Unbounded caching with `@cache`**

```python
from functools import cache


@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(100))
print(fibonacci.cache_info())
```

`cache_info()` exposes:

- **hits**: requests served from the cache
- **misses**: inputs that required computation
- **maxsize**: the configured cache capacity
- **currsize**: the current number of cached entries

The cache can be cleared explicitly:

```python
fibonacci.cache_clear()
```

### **Bounded caching with `@lru_cache`**

An unbounded cache may retain objects indefinitely. A **least recently used** cache limits memory by evicting older entries:

```python
from functools import lru_cache


@lru_cache(maxsize=256)
def render_template(template_name: str, theme: str) -> str:
    print("Rendering from scratch...")
    return f"<article class='{theme}'>{template_name}</article>"
```

When the cache is full, `lru_cache` discards the entry that has gone unused for the longest time.

| Tool | Capacity | Best fit |
|---|---:|---|
| `@cache` | Unbounded | Small, known input spaces |
| `@lru_cache(maxsize=N)` | Bounded | Repeated requests with uncertain input variety |
| Manual dictionary | Custom | Specialized keys, expiration, metrics, or invalidation |

### **Arguments form the cache key**

Calls that appear equivalent to a human may produce distinct keys:

```python
calculate(10, 20)
calculate(first=10, second=20)
```

Likewise, mutable values such as lists and dictionaries cannot be used directly with `@cache` because they are not hashable:

```python
from functools import cache


@cache
def total(values: tuple[int, ...]) -> int:
    return sum(values)


numbers = [3, 5, 8]
print(total(tuple(numbers)))
```

Converting a list to a tuple creates an immutable, hashable representation. That conversion is safe only if order is semantically meaningful. If order does not matter, a sorted tuple or `frozenset` may be a more accurate key.

---

## **5. Memoization and Dynamic Programming**

Memoization is one of two common dynamic-programming strategies.

### **Top-down: memoization**

Start with the original problem and recursively request smaller answers:

```python
from functools import cache


@cache
def ways_to_climb(steps: int) -> int:
    """Count ways to climb using moves of one or two steps."""
    if steps < 0:
        return 0
    if steps == 0:
        return 1
    return ways_to_climb(steps - 1) + ways_to_climb(steps - 2)
```

### **Bottom-up: tabulation**

Start with known base cases and iteratively build larger answers:

```python
def ways_to_climb(steps: int) -> int:
    if steps < 0:
        return 0

    previous, current = 0, 1

    for _ in range(steps):
        previous, current = current, previous + current

    return current
```

| Characteristic | Top-down memoization | Bottom-up tabulation |
|---|---|---|
| Control flow | Recursive | Iterative |
| Evaluates | Only requested states | Usually all states up to the target |
| Stack usage | May be significant | Usually constant |
| Relation to recurrence | Often direct and readable | May require reordering |
| Constant overhead | Function calls and key lookup | Often lower |

Neither is universally superior. Memoization is attractive when only a small fraction of possible states is reached. Tabulation is often better when all states are needed and their dependency order is straightforward.

---

## **6. Cache Design and Correctness**

Caching introduces state. Once state exists, correctness depends on more than the underlying function.

### **6.1 Referential transparency**

The safest memoized function behaves like a mathematical function:

```text
same input → same output
```

This property is often called **referential transparency**. Pure computations such as parsing a fixed string or calculating a mathematical value are strong candidates.

A changing exchange-rate lookup is not:

```python
# Unsafe if the rate can change while the process runs.
@cache
def get_exchange_rate(currency: str) -> float:
    return request_live_rate(currency)
```

The first response could remain cached long after it becomes stale. A time-to-live cache or deliberate invalidation policy would be required.

### **6.2 Key completeness**

Every input that can affect the output must be represented in the key.

```python
tax_rates = {"standard": 0.20}


@cache
def calculate_tax(amount: float) -> float:
    return amount * tax_rates["standard"]
```

The result depends on both `amount` and hidden global state. If the rate changes, old results become incorrect.

A safer interface makes the dependency explicit:

```python
from decimal import Decimal
from functools import cache


@cache
def calculate_tax(amount: Decimal, rate: Decimal) -> Decimal:
    return amount * rate
```

### **6.3 Cached mutable results**

Returning a cached mutable object lets callers alter the value stored in the cache:

```python
@cache
def default_permissions(role: str) -> list[str]:
    return ["read"] if role == "viewer" else ["read", "write"]


permissions = default_permissions("viewer")
permissions.append("delete")

# The cached value now contains "delete".
print(default_permissions("viewer"))
```

Prefer immutable return values:

```python
@cache
def default_permissions(role: str) -> tuple[str, ...]:
    return ("read",) if role == "viewer" else ("read", "write")
```

Alternatively, return a defensive copy, although copying reduces the performance benefit.

### **6.4 Cache lifetime**

Ask these questions before adding a cache:

- Is the cache scoped to one request, one object, one process, or many machines?
- When does cached data become stale?
- Who invalidates it?
- Is the cache bounded by entry count, bytes, or time?
- Does it store sensitive information?
- What happens after a deployment or schema change?

Cache invalidation is often difficult because the program must know exactly when a stored assumption stops being true.

---

## **7. Performance Analysis**

Memoization does not make every operation free. It changes the cost model.

Let:

- `U` be the number of unique inputs.
- `C` be the cost of computing one result.
- `L` be the average cache lookup cost.
- `R` be the total number of requests.

Without memoization, approximate work is:

```text
R × C
```

With memoization, approximate work is:

```text
U × C + R × L
```

Memoization helps when `U` is much smaller than `R` and `C` is meaningfully larger than `L`.

### **Measure instead of assuming**

A small benchmark can reveal whether caching matters:

```python
from functools import cache
from time import perf_counter


def slow_square(n: int) -> int:
    return n * n


@cache
def cached_square(n: int) -> int:
    return n * n


inputs = [number % 100 for number in range(1_000_000)]

start = perf_counter()
for value in inputs:
    slow_square(value)
plain_duration = perf_counter() - start

start = perf_counter()
for value in inputs:
    cached_square(value)
cached_duration = perf_counter() - start

print(f"Plain:  {plain_duration:.4f}s")
print(f"Cached: {cached_duration:.4f}s")
```

This example may show little benefit—or even a slowdown—because multiplication is cheaper than cache key construction and lookup. Cache **expensive work**, not merely repeated work.

Useful measurements include:

- Cache hit ratio: `hits / (hits + misses)`
- Average hit and miss latency
- Entry count and memory consumption
- Eviction rate
- Stale-result rate
- Time spent creating keys

---

## **8. Practical Examples**

### **8.1 Parsing repeated configuration strings**

```python
import json
from functools import lru_cache
from typing import Any


@lru_cache(maxsize=128)
def parse_configuration(raw: str) -> dict[str, Any]:
    # Return a new dictionary to protect the cached representation.
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Configuration must be a JSON object")
    return parsed
```

Because dictionaries are mutable, a production version could cache an immutable model or copy the result before returning it.

### **8.2 Counting paths through a blocked grid**

Suppose a robot can move only right or down:

```python
from functools import cache


def count_paths(
    rows: int,
    columns: int,
    blocked: set[tuple[int, int]],
) -> int:
    frozen_blocked = frozenset(blocked)

    @cache
    def visit(row: int, column: int) -> int:
        if row >= rows or column >= columns:
            return 0
        if (row, column) in frozen_blocked:
            return 0
        if (row, column) == (rows - 1, columns - 1):
            return 1

        return visit(row + 1, column) + visit(row, column + 1)

    return visit(0, 0)


obstacles = {(1, 1), (2, 1)}
print(count_paths(4, 4, obstacles))
```

The nested function is useful here: its cache lives only for one `count_paths` call, while `rows`, `columns`, and `frozen_blocked` remain fixed in the closure.

### **8.3 Avoiding cycles in recursive structures**

Memoization alone does not prevent infinite recursion if a graph contains cycles. A node must be marked as **in progress** before visiting its neighbors:

```python
def depends_on(
    graph: dict[str, list[str]],
    start: str,
    target: str,
) -> bool:
    memo: dict[str, bool] = {}
    visiting: set[str] = set()

    def search(node: str) -> bool:
        if node == target:
            return True
        if node in memo:
            return memo[node]
        if node in visiting:
            return False

        visiting.add(node)
        result = any(search(neighbor) for neighbor in graph.get(node, []))
        visiting.remove(node)

        memo[node] = result
        return result

    return search(start)
```

Here the two data structures have separate responsibilities:

- `memo` records completed answers.
- `visiting` detects cycles along the current path.

### **8.4 TypeScript implementation**

Memoization is a general technique, not a Python feature:

```typescript
function memoize<A extends readonly unknown[], R>(
  fn: (...args: A) => R,
  makeKey: (...args: A) => string,
): (...args: A) => R {
  const cache = new Map<string, R>();

  return (...args: A): R => {
    const key = makeKey(...args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const distance = memoize(
  (x: number, y: number) => Math.sqrt(x * x + y * y),
  (x, y) => `${x}:${y}`,
);
```

String key construction is convenient but must be unambiguous. For complex values, naive `JSON.stringify` may be sensitive to property order and unable to represent some JavaScript values correctly.

---

## **9. Common Mistakes**

### **Mistake 1: Caching side effects**

```python
@cache
def send_email(address: str) -> bool:
    ...
```

The cache changes behavior: repeated calls no longer send repeated emails. Memoize computations, not commands whose purpose is to perform an effect.

### **Mistake 2: Ignoring memory growth**

An unbounded cache exposed to user-controlled inputs can grow for the life of the process. Use a bounded cache, expiration, request scope, or explicit cleanup.

### **Mistake 3: Omitting dependencies from the key**

Locale, user permissions, feature flags, application version, and configuration may all affect results. If they matter, include them or invalidate affected entries.

### **Mistake 4: Caching trivial work**

A dictionary lookup can cost more than a tiny calculation. Benchmark with realistic input distributions.

### **Mistake 5: Confusing “cached” with “persistent”**

An in-memory memoization cache disappears when the process exits. It is not a database and is not automatically shared by other workers.

### **Mistake 6: Assuming thread safety solves duplicate work**

A cache may protect its internal dictionary while still allowing two concurrent misses to compute the same result. If duplicate work is unacceptable, use per-key locking or a “single-flight” mechanism.

### **Mistake 7: Caching failures forever**

If exceptions or failure values are cached, a temporary outage can become a permanent local failure. Decide explicitly whether failures should be cached and for how long.

---

## **10. When Memoization Is the Wrong Tool**

Do not reach for memoization automatically. It is a poor fit when:

- Calls rarely repeat the same inputs.
- The calculation is already cheap.
- Results change frequently or unpredictably.
- The input space is enormous and memory is limited.
- Correct invalidation would be more complex than recomputation.
- The function exists primarily for side effects.
- Inputs or outputs contain secrets that should not remain in memory.
- An iterative algorithm offers the same speed with less memory.

A useful decision checklist:

| Question | If “yes” | If “no” |
|---|---|---|
| Are identical inputs common? | Continue evaluating | Skip memoization |
| Is computation expensive? | Potentially valuable | Measure carefully |
| Is the result stable? | Simple caching may work | Define freshness rules |
| Is the key complete and compact? | Proceed | Redesign the interface |
| Can memory be bounded? | Choose a policy | Avoid or scope the cache |
| Can effectiveness be measured? | Add metrics | Establish observability |

---

## **11. Exercises**

### **Exercise 1: Minimum coin count**

Given coin denominations and a target amount, return the minimum number of coins needed. Use memoization to avoid repeatedly solving the same remaining amount.

```python
def minimum_coins(coins: tuple[int, ...], amount: int) -> int | None:
    # Implement this.
    ...
```

Consider:

- What is the memoization key?
- What result represents an impossible amount?
- How does the complexity depend on `amount` and the number of coin types?

<details>
<summary><strong>Possible solution</strong></summary>

```python
from functools import cache


def minimum_coins(coins: tuple[int, ...], amount: int) -> int | None:
    if amount < 0:
        return None
    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive")

    @cache
    def solve(remaining: int) -> int | None:
        if remaining == 0:
            return 0
        if remaining < 0:
            return None

        candidates: list[int] = []

        for coin in coins:
            subproblem = solve(remaining - coin)
            if subproblem is not None:
                candidates.append(subproblem + 1)

        return min(candidates) if candidates else None

    return solve(amount)
```

</details>

### **Exercise 2: Normalize cache keys**

Write a memoized function that accepts tags where order does not matter:

```python
search_by_tags(["python", "cache"])
search_by_tags(["cache", "python"])
```

Both calls should use the same cached entry. Consider duplicates and letter casing when designing the key.

### **Exercise 3: Add cache statistics**

Extend the hand-written `memoize` decorator so it records:

- Hits
- Misses
- Current cache size
- A method that clears both entries and statistics

### **Exercise 4: Choose the right strategy**

For each workload, decide between no cache, unbounded memoization, bounded LRU caching, time-based caching, or persistent storage:

1. Computing factorials from `0` through `100`.
2. Fetching live weather data by city.
3. Parsing the same 20 schema files throughout a compiler run.
4. Rendering personalized pages for millions of users.
5. Calculating `x + 1`.

The important part is not the label; it is the reasoning about cost, repetition, freshness, and memory.

---

## **12. Summary and Reference**

Memoization is a focused optimization:

> Store results by input, then reuse them when the same problem appears again.

### **Key takeaways**

- Memoization is most effective for expensive computations with repeated, stable inputs.
- It can turn recursive algorithms with overlapping subproblems from exponential time into polynomial or linear time.
- A correct key must represent every dependency that affects the result.
- Mutable results, hidden global state, and stale external data require special care.
- Cache lifetime and eviction are part of program correctness, not merely performance tuning.
- Bounded caches control memory but may reduce the hit rate.
- Top-down memoization and bottom-up tabulation solve similar problems with different tradeoffs.
- Realistic benchmarks and cache metrics should justify the optimization.

### **Compact Python reference**

```python
from functools import cache, lru_cache


@cache
def unbounded(value: int) -> int:
    return expensive_calculation(value)


@lru_cache(maxsize=256)
def bounded(value: int) -> int:
    return expensive_calculation(value)


print(unbounded.cache_info())
unbounded.cache_clear()
```

### **Final rule of thumb**

**Memoize when repeated computation is measurably more expensive than storing, locating, and safely maintaining the result.**

---

*End of tutorial.*
