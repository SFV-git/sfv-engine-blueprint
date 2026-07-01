# **Bloom Filters: Fast, Memory-Efficient Membership Testing**

> **Concept chosen:** Bloom filters — probabilistic data structures that can quickly answer  
> “Have I probably seen this item before?” while using remarkably little memory.

---

## **Table of Contents**

1. [The Problem Bloom Filters Solve](#1-the-problem-bloom-filters-solve)
2. [The Core Idea](#2-the-core-idea)
3. [How Insertion and Lookup Work](#3-how-insertion-and-lookup-work)
4. [A Python Implementation](#4-a-python-implementation)
5. [False Positives and the Mathematics](#5-false-positives-and-the-mathematics)
6. [Choosing Good Parameters](#6-choosing-good-parameters)
7. [Practical Example: Filtering Duplicate URLs](#7-practical-example-filtering-duplicate-urls)
8. [Common Mistakes and Limitations](#8-common-mistakes-and-limitations)
9. [Variants and Extensions](#9-variants-and-extensions)
10. [Exercises](#10-exercises)
11. [Summary](#11-summary)

---

## **1. The Problem Bloom Filters Solve**

Imagine that a web crawler has already visited 100 million URLs. Before fetching another
URL, it needs to ask:

> **“Has this URL already been visited?”**

A normal set gives an exact answer:

```python
visited = {
    "https://example.com/",
    "https://example.com/about",
}

if "https://example.com/contact" not in visited:
    print("Fetch this page")
```

This is simple and usually fast, but retaining every complete URL can consume a large
amount of memory. A Bloom filter provides a different tradeoff:

- It uses a compact array of bits instead of storing complete values.
- It never reports an inserted value as absent.
- It may occasionally report an unseen value as present.

These outcomes can be summarized as follows:

| Bloom filter answer | Actual condition | Meaning |
|---|---|---|
| **Definitely absent** | Absent | The item was not inserted |
| **Probably present** | Present | Correct membership result |
| **Probably present** | Absent | False positive |
| **Definitely absent** | Present | Impossible in a standard Bloom filter |

The phrase **“probably present, definitely absent”** is the essential Bloom-filter
contract.

### **When is that tradeoff useful?**

A Bloom filter is useful when:

- the collection is large;
- exact storage is expensive;
- membership checks are frequent;
- false positives are acceptable or can be checked elsewhere; and
- false negatives are unacceptable.

Common applications include caches, database engines, distributed storage systems,
web crawlers, spell-checking pipelines, and network services.

---

## **2. The Core Idea**

A Bloom filter consists of:

1. a bit array containing `m` bits, initially all zero;
2. `k` independent hash functions; and
3. operations for insertion and membership testing.

Suppose the filter has 12 bits:

```text
index:  0 1 2 3 4 5 6 7 8 9 10 11
bits:   0 0 0 0 0 0 0 0 0 0  0  0
```

To insert `"pear"`, three hash functions might produce indices `2`, `7`, and `10`.
Those bits are set to one:

```text
index:  0 1 2 3 4 5 6 7 8 9 10 11
bits:   0 0 1 0 0 0 0 1 0 0  1  0
```

Inserting `"plum"` might produce `1`, `7`, and `9`:

```text
index:  0 1 2 3 4 5 6 7 8 9 10 11
bits:   0 1 1 0 0 0 0 1 0 1  1  0
```

Notice that both values may set bit `7`. This overlap is expected. Bloom filters do
not preserve enough information to reconstruct their inserted values.

### **Why multiple hashes?**

One hash would set too little information and cause collisions quickly. Multiple hashes
create a compact fingerprint spread across the bit array. However, using too many
hashes fills the array rapidly, so more is not always better.

### **A useful mental model**

Think of each inserted value as switching on several lamps. To test a value, calculate
which lamps it would have switched on:

- if any required lamp is off, the value was **definitely not inserted**;
- if every required lamp is on, the value was **probably inserted**.

All required lamps might have been switched on by several other values. That is the
source of false positives.

---

## **3. How Insertion and Lookup Work**

### **Insertion**

To add a value `x`:

1. Compute `k` hashes of `x`.
2. Map each hash into the range `0` through `m - 1`.
3. Set every corresponding bit to `1`.

Pseudocode:

```text
function add(x):
    for each hash_function h:
        index = h(x) mod m
        bits[index] = 1
```

### **Membership lookup**

To test a value `x`:

1. Compute the same `k` indices.
2. Inspect the corresponding bits.
3. Return false if at least one bit is zero.
4. Otherwise, return true.

```text
function might_contain(x):
    for each hash_function h:
        index = h(x) mod m
        if bits[index] == 0:
            return false
    return true
```

### **Why false negatives do not occur**

Insertion sets all of an item's bits. A standard Bloom filter never clears individual
bits, so a later lookup will find those bits still set. Therefore, an inserted item
cannot test as absent.

This guarantee assumes:

- the filter was not reset;
- identical bytes are hashed during insertion and lookup;
- the hash configuration has not changed; and
- there is no data corruption or concurrent-update bug.

---

## **4. A Python Implementation**

The following implementation uses Python's standard library. It derives multiple
indices from SHA-256 using **double hashing**, a practical technique described later.

```python
from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable


class BloomFilter:
    """A fixed-capacity probabilistic membership filter."""

    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be between 0 and 1")

        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate

        # Optimal bit count:
        # m = -n ln(p) / (ln(2)^2)
        self.bit_count = math.ceil(
            -expected_items * math.log(false_positive_rate)
            / (math.log(2) ** 2)
        )

        # Optimal number of hashes:
        # k = (m / n) ln(2)
        self.hash_count = max(
            1,
            round((self.bit_count / expected_items) * math.log(2)),
        )

        # Eight bits fit in each byte.
        self._bytes = bytearray((self.bit_count + 7) // 8)
        self.items_added = 0

    def _indices(self, value: str) -> Iterable[int]:
        encoded = value.encode("utf-8")
        digest = hashlib.sha256(encoded).digest()

        # Interpret two digest segments as large unsigned integers.
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big")

        # Generate k positions without computing k separate cryptographic hashes.
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.bit_count

    def _set_bit(self, index: int) -> None:
        byte_index, bit_offset = divmod(index, 8)
        self._bytes[byte_index] |= 1 << bit_offset

    def _get_bit(self, index: int) -> bool:
        byte_index, bit_offset = divmod(index, 8)
        return bool(self._bytes[byte_index] & (1 << bit_offset))

    def add(self, value: str) -> None:
        for index in self._indices(value):
            self._set_bit(index)
        self.items_added += 1

    def might_contain(self, value: str) -> bool:
        return all(self._get_bit(index) for index in self._indices(value))

    def __contains__(self, value: str) -> bool:
        return self.might_contain(value)

    @property
    def size_bytes(self) -> int:
        return len(self._bytes)
```

Example usage:

```python
filter_ = BloomFilter(expected_items=100_000, false_positive_rate=0.01)

filter_.add("alpha@example.com")
filter_.add("beta@example.com")

print("alpha@example.com" in filter_)  # True: probably present
print("gamma@example.com" in filter_)  # Usually False: definitely absent

print(filter_.bit_count)   # Approximately 958,506 bits
print(filter_.hash_count)  # Approximately 7 hashes
print(filter_.size_bytes)  # Approximately 119,814 bytes
```

### **Understanding the bit operations**

A `bytearray` stores eight filter bits per byte. Given a bit index:

```python
byte_index, bit_offset = divmod(index, 8)
```

For index `19`, the result is:

```text
byte_index = 2
bit_offset = 3
```

The mask `1 << 3` is binary `00001000`. Setting the bit uses bitwise OR:

```python
data[2] |= 1 << 3
```

Testing the bit uses bitwise AND:

```python
is_set = bool(data[2] & (1 << 3))
```

### **Why not use Python's built-in `hash()`?**

Python intentionally randomizes many built-in hash values between interpreter
processes. A persisted Bloom filter created in one process could become invalid when
loaded by another. A stable hashing algorithm avoids that problem.

SHA-256 is portable and convenient for a tutorial, though a faster non-cryptographic
hash is often preferable in performance-sensitive production systems.

---

## **5. False Positives and the Mathematics**

Let:

- `m` be the number of bits;
- `n` be the number of inserted items; and
- `k` be the number of hash indices per item.

After inserting `n` items, the approximate false-positive probability is:

```text
p ≈ (1 - e^(-kn/m))^k
```

This expression captures two competing effects:

- too few hashes produce weak fingerprints;
- too many hashes fill the bit array too quickly.

For fixed `m` and `n`, the approximately optimal number of hashes is:

```text
k ≈ (m / n) ln(2)
```

If the desired false-positive probability `p` and expected item count `n` are known,
the required bit count is:

```text
m ≈ -n ln(p) / (ln(2))²
```

### **Example calculation**

Suppose a service expects one million identifiers and accepts a 1% false-positive
rate:

```python
import math

n = 1_000_000
p = 0.01

m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
k = round((m / n) * math.log(2))

print(f"Bits: {m:,}")
print(f"MiB:  {m / 8 / 1024 / 1024:.2f}")
print(f"Hashes: {k}")
```

Approximate result:

```text
Bits: 9,585,059
MiB:  1.14
Hashes: 7
```

The filter needs roughly **9.6 bits per expected item**, or about **1.14 MiB** total,
not counting object overhead.

### **Capacity matters**

The target false-positive probability is valid only near the planned capacity.
Continuing to insert items increases the probability:

| Inserted items relative to design capacity | Approximate effect |
|---:|---|
| 25% | Very low false-positive rate |
| 50% | Below the design target |
| 100% | Near the design target |
| 150% | Significantly above target |
| 200% | Potentially much worse |

The filter does not suddenly fail when overloaded. Its answers simply become less
useful as more bits turn on.

### **Empirically measuring the rate**

```python
filter_ = BloomFilter(expected_items=50_000, false_positive_rate=0.01)

for i in range(50_000):
    filter_.add(f"inserted:{i}")

trials = 100_000
false_positives = sum(
    f"never-inserted:{i}" in filter_
    for i in range(trials)
)

print(f"Observed rate: {false_positives / trials:.3%}")
```

The observed result will vary, but it should be reasonably close to the configured
rate when the hash indices are well distributed.

---

## **6. Choosing Good Parameters**

Parameter selection should start from requirements, not guesses.

### **Step 1: Estimate `n`**

Choose the maximum number of distinct items expected during the filter's useful
lifetime. If traffic varies, use a credible high-water mark and include a safety
margin.

### **Step 2: Choose an acceptable `p`**

Ask what a false positive costs:

- If it causes one inexpensive database lookup, 1% may be acceptable.
- If it incorrectly suppresses important work, even 0.01% may be too high.
- If any false positive is unacceptable, a Bloom filter alone is the wrong tool.

### **Step 3: Compute `m` and `k`**

| Expected items | Target false-positive rate | Approx. bits/item | Approx. hashes |
|---:|---:|---:|---:|
| 100,000 | 10% | 4.79 | 3 |
| 100,000 | 1% | 9.59 | 7 |
| 100,000 | 0.1% | 14.38 | 10 |
| 1,000,000 | 1% | 9.59 | 7 |

The bits required **per item** depend primarily on the target error rate, not the
absolute number of items.

### **Step 4: Define lifecycle behavior**

Decide what happens when capacity is reached:

- rotate to a new filter;
- rebuild a larger filter from an authoritative data source;
- use a scalable Bloom filter;
- accept a rising false-positive rate; or
- partition filters by day, tenant, region, or another stable key.

Operational lifecycle is part of the data structure's design.

---

## **7. Practical Example: Filtering Duplicate URLs**

Consider a crawler that uses a Bloom filter as a fast front gate and a database as the
authoritative source.

```python
class CrawlFrontier:
    def __init__(self, database, expected_urls: int):
        self.database = database
        self.seen = BloomFilter(
            expected_items=expected_urls,
            false_positive_rate=0.005,
        )

    def should_fetch(self, url: str) -> bool:
        normalized = normalize_url(url)

        # A negative answer is definitive.
        if normalized not in self.seen:
            return True

        # A positive answer might be false, so verify it.
        return not self.database.contains_url(normalized)

    def mark_fetched(self, url: str) -> None:
        normalized = normalize_url(url)
        self.database.insert_url(normalized)
        self.seen.add(normalized)
```

A minimal URL normalizer might look like this:

```python
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    scheme, netloc, path, query, _fragment = urlsplit(url)

    scheme = scheme.lower()
    netloc = netloc.lower()
    path = path or "/"

    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    return urlunsplit((scheme, netloc, path, query, ""))
```

The request flow is:

```text
Candidate URL
     |
     v
Bloom filter says absent? ---- yes ----> Fetch candidate
     |
     no
     v
Check authoritative database
     |
     +---- present ----> Skip duplicate
     |
     +---- absent  ----> False positive; fetch candidate
```

This pattern is powerful because Bloom-filter negatives avoid expensive database
queries, while positive answers are safely verified.

### **Insertion ordering**

In real systems, consistency matters. If the Bloom filter is updated before the
database write succeeds, another worker may see “probably present” while the database
still has no record. Whether this is acceptable depends on the workflow.

A safer default is:

1. complete the authoritative write;
2. update the Bloom filter; and
3. make retries idempotent.

---

## **8. Common Mistakes and Limitations**

### **Mistake 1: Treating “probably present” as certain**

Incorrect:

```python
if user_id in bloom:
    reject_registration()
```

Safer:

```python
if user_id in bloom and database.user_exists(user_id):
    reject_registration()
```

If a false positive causes data loss, denial of service, or an incorrect business
decision, verify positive answers against authoritative state.

### **Mistake 2: Expecting deletion**

Clearing an item's bits is unsafe because those bits may also represent other items:

```text
"pear" uses bits 2, 7, 10
"plum" uses bits 1, 7, 9
```

Clearing bit `7` while deleting `"pear"` could cause `"plum"` to become a false
negative. Standard Bloom filters therefore do not support deletion.

### **Mistake 3: Ignoring normalization**

These strings may refer to equivalent resources but hash differently:

```text
https://EXAMPLE.com
https://example.com/
https://example.com:443/
```

Canonicalize values before both insertion and lookup. The exact normalization rules
must match the application's semantics.

### **Mistake 4: Changing hash behavior**

Persisted filters need a versioned format that records:

- bit count;
- hash count;
- hash algorithm and seed;
- value encoding and normalization version; and
- byte order or bit layout.

Without this metadata, a software upgrade can silently invalidate the filter.

### **Mistake 5: Forgetting concurrency**

Concurrent bit-setting operations must not lose updates. In a distributed system,
workers also need a defined ownership or synchronization model. Possible approaches
include:

- one filter per worker;
- atomic operations on shared memory;
- partitioned filters;
- a dedicated filter service; or
- periodic merging by bitwise OR.

Two compatible Bloom filters can be unioned:

```python
combined = bytearray(a | b for a, b in zip(filter_a, filter_b))
```

This requires identical size and hash configuration.

### **Important limitations**

A Bloom filter:

- cannot enumerate its contents;
- cannot recover inserted values;
- cannot report exact item counts;
- does not support normal deletion;
- has false positives;
- degrades when overloaded; and
- requires stable hashing and serialization rules.

---

## **9. Variants and Extensions**

### **Counting Bloom filter**

A counting Bloom filter replaces each bit with a small counter:

- insertion increments counters;
- deletion decrements counters; and
- lookup checks whether all counters are nonzero.

It supports deletion but consumes more memory and requires care to prevent counter
overflow or accidental deletion of an item that was never inserted.

### **Scalable Bloom filter**

A scalable Bloom filter adds new filters as capacity grows. Queries check each
component filter. This avoids requiring an exact capacity estimate in advance, though
it introduces additional lookups and more complex error budgeting.

### **Partitioned Bloom filter**

The bit array is divided into `k` regions, and each hash selects one bit from its own
region. This layout can improve memory-access behavior and simplify some
implementations.

### **Cuckoo filter**

A Cuckoo filter stores compact fingerprints in hash-table buckets. Depending on the
configuration, it can offer deletion, competitive space efficiency, and good lookup
performance. Insertions are more complex and can fail when the structure is too full.

### **Related structures**

| Structure | False positives | False negatives | Deletion | Enumerates values |
|---|---:|---:|---:|---:|
| Hash set | No | No | Yes | Yes |
| Bloom filter | Yes | No | No | No |
| Counting Bloom filter | Yes | No* | Yes | No |
| Cuckoo filter | Yes | No* | Yes | No |

`*` Assumes correct use and no implementation, overflow, or concurrency errors.

The right structure depends on required operations—not merely lookup speed.

---

## **10. Exercises**

### **Exercise 1: Inspect bit density**

Add this property to `BloomFilter`:

```python
@property
def bit_density(self) -> float:
    set_bits = sum(byte.bit_count() for byte in self._bytes)
    return set_bits / self.bit_count
```

Then measure density at 25%, 50%, 100%, and 200% of design capacity. Explain how the
density relates to false positives.

### **Exercise 2: Support bytes**

Modify the class so it accepts `bytes` as well as `str`. Make the conversion explicit
and ensure two distinct representations cannot accidentally be treated as identical.

```python
def encode_value(value: str | bytes) -> bytes:
    if isinstance(value, str):
        return b"s:" + value.encode("utf-8")
    return b"b:" + value
```

### **Exercise 3: Add persistence**

Design a file format with:

```text
magic bytes
format version
bit count
hash count
hash identifier
normalization version
raw bit-array bytes
checksum
```

Reject incompatible or corrupted files rather than loading them silently.

### **Exercise 4: Compare with a set**

Insert one million short strings into both a Python `set` and a Bloom filter. Measure:

- construction time;
- lookup time;
- approximate memory usage; and
- observed false-positive rate.

Remember that Python object overhead makes a simple `len()` comparison insufficient.

### **Exercise 5: Test the guarantee**

Write a test proving that inserted values never return false:

```python
def test_no_false_negatives():
    bloom = BloomFilter(10_000, 0.01)
    values = [f"item:{i}" for i in range(10_000)]

    for value in values:
        bloom.add(value)

    assert all(value in bloom for value in values)
```

Then write a statistical test for false positives. Avoid asserting an exact count;
use a generous range so random variation does not make the test flaky.

---

## **11. Summary**

A Bloom filter exchanges exactness for exceptional space efficiency:

- insertion sets several hash-selected bits;
- lookup checks those same bits;
- a zero bit proves an item is absent;
- all-one bits mean the item is only probably present;
- false negatives are excluded by the standard algorithm;
- false positives are controlled through capacity, bit count, and hash count; and
- positive answers can be verified against authoritative storage when correctness
  demands it.

The key design question is not simply **“Is a Bloom filter fast?”** It is:

> **“Can this system safely exploit definitive negative answers while tolerating—or
> verifying—probabilistic positive answers?”**

When the answer is yes, Bloom filters can eliminate large numbers of expensive
lookups with a surprisingly small memory footprint.

