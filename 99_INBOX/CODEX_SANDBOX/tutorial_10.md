# **Event Sourcing: Reconstructing State from a History of Facts**

> **Programming concept:** Event sourcing  
> **Examples:** Python 3.11+  
> **Level:** Intermediate  
> **Core idea:** Store the events that changed a system, then derive current state by replaying those events.

---

## **Table of Contents**

1. [Why Event Sourcing Exists](#1-why-event-sourcing-exists)
2. [The Core Mental Model](#2-the-core-mental-model)
3. [Events, State, and the Fold](#3-events-state-and-the-fold)
4. [Building a Small Event-Sourced Bank Account](#4-building-a-small-event-sourced-bank-account)
5. [Separating Decisions from State Changes](#5-separating-decisions-from-state-changes)
6. [Persisting and Reloading Events](#6-persisting-and-reloading-events)
7. [Optimistic Concurrency Control](#7-optimistic-concurrency-control)
8. [Snapshots and Performance](#8-snapshots-and-performance)
9. [Schema Evolution](#9-schema-evolution)
10. [Projections and Read Models](#10-projections-and-read-models)
11. [Testing Event-Sourced Systems](#11-testing-event-sourced-systems)
12. [Common Mistakes and Practical Trade-offs](#12-common-mistakes-and-practical-trade-offs)
13. [When to Use Event Sourcing](#13-when-to-use-event-sourcing)
14. [Complete Example](#14-complete-example)
15. [Further Exercises](#15-further-exercises)

---

## **1. Why Event Sourcing Exists**

Most applications store only their **current state**. A conventional bank-account row might look like this:

| account_id | owner | balance | status |
|---|---|---:|---|
| `A-1042` | Ada | 12500 | open |

This representation answers “What is true now?” efficiently. It does not naturally answer:

- **How did the balance become 12,500?**
- **Which command caused the latest change?**
- **What did the account look like yesterday?**
- **Can a new reporting model be calculated from the historical activity?**
- **Was a disputed withdrawal ever accepted?**

A conventional design can add audit tables, logs, or change-data capture. Event sourcing takes a stronger position: the historical changes are not secondary audit data. They are the **authoritative source of truth**.

Instead of replacing the balance, the application appends facts:

```text
AccountOpened(owner="Ada")
MoneyDeposited(amount=15000)
MoneyWithdrawn(amount=2500)
```

The current balance is calculated by replaying those facts:

```text
0 + 15000 - 2500 = 12500
```

This produces an important shift in design:

> **State is a derived value. Events are durable facts.**

An event-sourced system normally never edits or deletes an event after it has been accepted. Corrections are expressed as additional events. If a deposit was entered twice, the system might append `DepositReversed`, preserving both the mistake and its correction.

---

## **2. The Core Mental Model**

Event sourcing becomes easier when four concepts are kept distinct.

| Concept | Meaning | Example |
|---|---|---|
| **Command** | A request that may be accepted or rejected | `WithdrawMoney(500)` |
| **Event** | An immutable fact that has already happened | `MoneyWithdrawn(500)` |
| **Aggregate** | The consistency boundary that validates commands | One bank account |
| **Projection** | A read-oriented view built from events | Monthly statement |

### **Commands are requests**

A command is written in the imperative mood:

```python
WithdrawMoney(amount=500)
```

It can fail. The account might be closed, the amount might be invalid, or the balance might be insufficient.

### **Events are facts**

An event is written in the past tense:

```python
MoneyWithdrawn(amount=500)
```

Once persisted, the event represents an accepted fact. Replaying it must not repeat validation or consult an external service. Replay says, “This happened; update the derived state accordingly.”

### **The aggregate protects invariants**

An aggregate receives a command, checks business rules against its current state, and emits zero or more events.

For example:

```text
command + current state -> events OR error
```

The emitted events are then applied:

```text
event + current state -> new state
```

These are deliberately separate operations. A command is a proposal. An event is a result.

---

## **3. Events, State, and the Fold**

At its mathematical core, event sourcing is a **fold** (also called a reduction).

Suppose `apply` accepts a state and one event:

```python
def apply(state, event):
    ...
    return new_state
```

Rebuilding the latest state means repeatedly applying every event:

```python
from functools import reduce

current_state = reduce(apply, event_history, initial_state)
```

The same operation written explicitly is often clearer:

```python
state = initial_state

for event in event_history:
    state = apply(state, event)
```

### **A tiny counter example**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Incremented:
    amount: int


@dataclass(frozen=True)
class Decremented:
    amount: int


def apply_counter(value: int, event: Incremented | Decremented) -> int:
    match event:
        case Incremented(amount):
            return value + amount
        case Decremented(amount):
            return value - amount
        case _:
            raise TypeError(f"Unsupported event: {event!r}")


history = [
    Incremented(10),
    Decremented(3),
    Incremented(8),
]

value = 0
for event in history:
    value = apply_counter(value, event)

assert value == 15
```

Two properties are worth noticing:

1. `apply_counter` has no external side effects.
2. Given the same initial state and events, it always produces the same result.

This determinism makes replay and testing reliable.

---

## **4. Building a Small Event-Sourced Bank Account**

We will model an account that can be opened, receive deposits, process withdrawals, and close.

### **4.1 Define immutable events**

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import TypeAlias


@dataclass(frozen=True)
class AccountOpened:
    account_id: str
    owner: str
    occurred_at: datetime


@dataclass(frozen=True)
class MoneyDeposited:
    amount: Decimal
    occurred_at: datetime


@dataclass(frozen=True)
class MoneyWithdrawn:
    amount: Decimal
    occurred_at: datetime


@dataclass(frozen=True)
class AccountClosed:
    occurred_at: datetime


AccountEvent: TypeAlias = (
    AccountOpened | MoneyDeposited | MoneyWithdrawn | AccountClosed
)
```

The classes are frozen because events should be treated as immutable values. `Decimal` is used instead of `float` because binary floating-point is unsuitable for exact monetary arithmetic.

### **4.2 Define the derived state**

```python
@dataclass
class AccountState:
    account_id: str | None = None
    owner: str | None = None
    balance: Decimal = Decimal("0")
    is_open: bool = False
    version: int = 0
```

The `version` records how many events have been applied. It will later support concurrency control.

### **4.3 Apply events**

```python
def apply_event(state: AccountState, event: AccountEvent) -> None:
    match event:
        case AccountOpened(account_id, owner, _):
            state.account_id = account_id
            state.owner = owner
            state.is_open = True

        case MoneyDeposited(amount, _):
            state.balance += amount

        case MoneyWithdrawn(amount, _):
            state.balance -= amount

        case AccountClosed(_):
            state.is_open = False

        case _:
            raise TypeError(f"Unsupported event: {event!r}")

    state.version += 1
```

Applying an event does not ask whether a withdrawal is affordable. If `MoneyWithdrawn` appears in the accepted history, the withdrawal already passed validation when it was originally produced.

### **4.4 Rehydrate an aggregate**

Rehydration is the process of rebuilding an aggregate from its history.

```python
def rehydrate(history: list[AccountEvent]) -> AccountState:
    state = AccountState()
    for event in history:
        apply_event(state, event)
    return state
```

Example:

```python
from datetime import UTC, datetime

now = datetime.now(UTC)

history = [
    AccountOpened("A-1042", "Ada", now),
    MoneyDeposited(Decimal("150.00"), now),
    MoneyWithdrawn(Decimal("25.00"), now),
]

account = rehydrate(history)

assert account.owner == "Ada"
assert account.balance == Decimal("125.00")
assert account.version == 3
```

---

## **5. Separating Decisions from State Changes**

A robust aggregate has two different responsibilities:

- **Decide:** Validate a command and produce events.
- **Evolve:** Apply accepted events to update state.

Mixing the two causes subtle replay bugs. For example, sending an email inside an event-application method would send the email again whenever history is replayed.

### **5.1 Commands**

```python
@dataclass(frozen=True)
class OpenAccount:
    account_id: str
    owner: str


@dataclass(frozen=True)
class DepositMoney:
    amount: Decimal


@dataclass(frozen=True)
class WithdrawMoney:
    amount: Decimal


@dataclass(frozen=True)
class CloseAccount:
    pass
```

### **5.2 Domain errors**

```python
class DomainError(Exception):
    """Base class for rejected business operations."""


class AccountAlreadyOpen(DomainError):
    pass


class AccountNotOpen(DomainError):
    pass


class InvalidAmount(DomainError):
    pass


class InsufficientFunds(DomainError):
    pass
```

### **5.3 Decision logic**

```python
from collections.abc import Callable


Clock = Callable[[], datetime]


def decide(
    state: AccountState,
    command: OpenAccount | DepositMoney | WithdrawMoney | CloseAccount,
    clock: Clock,
) -> list[AccountEvent]:
    match command:
        case OpenAccount(account_id, owner):
            if state.is_open or state.account_id is not None:
                raise AccountAlreadyOpen(account_id)
            if not owner.strip():
                raise DomainError("Owner name must not be empty")
            return [AccountOpened(account_id, owner.strip(), clock())]

        case DepositMoney(amount):
            require_open(state)
            require_positive(amount)
            return [MoneyDeposited(amount, clock())]

        case WithdrawMoney(amount):
            require_open(state)
            require_positive(amount)
            if amount > state.balance:
                raise InsufficientFunds(
                    f"Requested {amount}; available {state.balance}"
                )
            return [MoneyWithdrawn(amount, clock())]

        case CloseAccount():
            require_open(state)
            if state.balance != Decimal("0"):
                raise DomainError("Balance must be zero before closing")
            return [AccountClosed(clock())]

        case _:
            raise TypeError(f"Unsupported command: {command!r}")


def require_open(state: AccountState) -> None:
    if not state.is_open:
        raise AccountNotOpen(state.account_id)


def require_positive(amount: Decimal) -> None:
    if amount <= Decimal("0"):
        raise InvalidAmount("Amount must be positive")
```

The clock is injected instead of calling `datetime.now()` directly. This makes the decision function deterministic under test.

### **5.4 Track uncommitted events**

An aggregate typically tracks newly produced events until the repository persists them:

```python
class BankAccount:
    def __init__(self) -> None:
        self.state = AccountState()
        self.pending_events: list[AccountEvent] = []

    @classmethod
    def from_history(cls, history: list[AccountEvent]) -> "BankAccount":
        account = cls()
        for event in history:
            apply_event(account.state, event)
        return account

    def handle(self, command, clock: Clock) -> None:
        new_events = decide(self.state, command, clock)
        for event in new_events:
            apply_event(self.state, event)
            self.pending_events.append(event)

    def mark_committed(self) -> None:
        self.pending_events.clear()
```

The sequence is:

```text
load history
    ↓
rehydrate aggregate
    ↓
handle command
    ↓
produce and apply new events
    ↓
append new events to storage
```

---

## **6. Persisting and Reloading Events**

An **event store** appends events to named streams. A stream generally contains the history of one aggregate, such as `account-A-1042`.

### **6.1 Minimal in-memory event store**

```python
from collections import defaultdict
from collections.abc import Sequence


class EventStreamNotFound(KeyError):
    pass


class InMemoryEventStore:
    def __init__(self) -> None:
        self._streams: dict[str, list[AccountEvent]] = defaultdict(list)

    def load(self, stream_id: str) -> list[AccountEvent]:
        if stream_id not in self._streams:
            raise EventStreamNotFound(stream_id)
        return list(self._streams[stream_id])

    def append(
        self,
        stream_id: str,
        events: Sequence[AccountEvent],
    ) -> None:
        self._streams[stream_id].extend(events)
```

Returning copies prevents callers from mutating the internal lists accidentally.

### **6.2 Repository**

```python
class AccountRepository:
    def __init__(self, store: InMemoryEventStore, clock: Clock) -> None:
        self.store = store
        self.clock = clock

    def get(self, account_id: str) -> BankAccount:
        stream_id = self._stream_id(account_id)
        history = self.store.load(stream_id)
        return BankAccount.from_history(history)

    def save(self, account: BankAccount) -> None:
        account_id = account.state.account_id
        if account_id is None:
            raise ValueError("Cannot save an unidentified account")

        self.store.append(
            self._stream_id(account_id),
            account.pending_events,
        )
        account.mark_committed()

    @staticmethod
    def _stream_id(account_id: str) -> str:
        return f"account-{account_id}"
```

Real stores also need serialization, transaction guarantees, metadata, and concurrency checks. The simple version exposes the architecture without hiding it behind infrastructure.

### **6.3 Event envelope**

Production events are often wrapped in an envelope:

```python
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class EventEnvelope:
    event_id: UUID
    stream_id: str
    stream_version: int
    event_type: str
    schema_version: int
    occurred_at: datetime
    payload: dict[str, Any]
    metadata: dict[str, Any]


envelope = EventEnvelope(
    event_id=uuid4(),
    stream_id="account-A-1042",
    stream_version=3,
    event_type="MoneyWithdrawn",
    schema_version=1,
    occurred_at=datetime.now(UTC),
    payload={"amount": "25.00"},
    metadata={
        "correlation_id": "request-72d",
        "causation_id": "command-1ab",
        "actor_id": "user-991",
    },
)
```

Metadata is useful for tracing without contaminating domain payloads. A correlation ID links all work caused by one request; a causation ID identifies the specific message that produced the event.

---

## **7. Optimistic Concurrency Control**

Consider two processes loading the same account at version 5:

```text
Process A loads version 5 and withdraws $80
Process B loads version 5 and withdraws $50
```

If the balance is $100, each process independently approves its withdrawal. Blindly appending both events creates a negative balance, violating the aggregate invariant.

The standard solution is **optimistic concurrency control**. Each append includes the version the writer expects:

```python
class ConcurrencyError(RuntimeError):
    pass


class VersionedEventStore:
    def __init__(self) -> None:
        self._streams: dict[str, list[AccountEvent]] = defaultdict(list)

    def load(self, stream_id: str) -> list[AccountEvent]:
        return list(self._streams.get(stream_id, []))

    def append(
        self,
        stream_id: str,
        expected_version: int,
        events: Sequence[AccountEvent],
    ) -> None:
        stream = self._streams[stream_id]
        actual_version = len(stream)

        if actual_version != expected_version:
            raise ConcurrencyError(
                f"{stream_id}: expected version {expected_version}, "
                f"found {actual_version}"
            )

        stream.extend(events)
```

The repository must calculate the version before pending events:

```python
def save_account(store: VersionedEventStore, account: BankAccount) -> None:
    pending_count = len(account.pending_events)
    expected_version = account.state.version - pending_count
    account_id = account.state.account_id

    if account_id is None:
        raise ValueError("Account has no ID")

    store.append(
        stream_id=f"account-{account_id}",
        expected_version=expected_version,
        events=account.pending_events,
    )
    account.mark_committed()
```

If another writer appended first, the second append fails. The application may reload and retry, but only when retrying is semantically safe. A user-facing withdrawal should not be retried indefinitely without considering idempotency and the intended business behavior.

---

## **8. Snapshots and Performance**

Replaying 40 events is cheap. Replaying 40 million events for every command is not.

A **snapshot** stores derived aggregate state at a specific stream version:

```python
@dataclass(frozen=True)
class AccountSnapshot:
    account_id: str
    owner: str
    balance: Decimal
    is_open: bool
    version: int
```

Loading then becomes:

1. Load the latest snapshot.
2. Load only events after the snapshot version.
3. Apply those events.

```python
def restore_from_snapshot(
    snapshot: AccountSnapshot,
    later_events: list[AccountEvent],
) -> AccountState:
    state = AccountState(
        account_id=snapshot.account_id,
        owner=snapshot.owner,
        balance=snapshot.balance,
        is_open=snapshot.is_open,
        version=snapshot.version,
    )

    for event in later_events:
        apply_event(state, event)

    return state
```

Snapshots are a cache, not the source of truth. They should be disposable and rebuildable from events.

| Strategy | Advantage | Cost |
|---|---|---|
| No snapshots | Simplest design | Replay grows with stream length |
| Every *N* events | Predictable replay bound | Extra writes and storage |
| Time-based | Simple operational schedule | Uneven stream sizes |
| Adaptive | Targets expensive aggregates | More complex policy |

Do not add snapshots preemptively. Measure replay latency first. Many well-designed aggregates have short histories because their consistency boundaries are narrow.

---

## **9. Schema Evolution**

Events live longer than application code. A system that stores events must expect old event shapes to remain in the store.

Suppose version 1 used:

```json
{
  "event_type": "MoneyDeposited",
  "schema_version": 1,
  "payload": {
    "amount": "25.00"
  }
}
```

Version 2 adds a currency:

```json
{
  "event_type": "MoneyDeposited",
  "schema_version": 2,
  "payload": {
    "amount": "25.00",
    "currency": "CAD"
  }
}
```

There are three common evolution strategies.

### **9.1 Upcasting**

Transform old serialized data into the current shape during reading:

```python
def upcast_money_deposited(record: dict) -> dict:
    version = record["schema_version"]

    if version == 1:
        record = {
            **record,
            "schema_version": 2,
            "payload": {
                **record["payload"],
                "currency": "CAD",
            },
        }

    return record
```

### **9.2 Multiple readers**

Keep a decoder for each historical version:

```python
def decode_deposit(record: dict) -> MoneyDeposited:
    match record["schema_version"]:
        case 1:
            amount = Decimal(record["payload"]["amount"])
        case 2:
            payload = record["payload"]
            if payload["currency"] != "CAD":
                raise ValueError("Unsupported currency")
            amount = Decimal(payload["amount"])
        case version:
            raise ValueError(f"Unknown schema version: {version}")

    return MoneyDeposited(
        amount=amount,
        occurred_at=datetime.fromisoformat(record["occurred_at"]),
    )
```

### **9.3 Explicit new event types**

When meaning changes—not merely representation—define a new event. Renaming a field can be upcast safely; changing what a field means often cannot.

> **Rule:** Never reinterpret an old fact to mean something it did not mean when written.

Avoid rewriting the entire event store unless there is a compelling operational reason. Permanent migration jobs are risky, difficult to roll back, and can weaken the evidentiary value of the log.

---

## **10. Projections and Read Models**

An aggregate is optimized for enforcing rules, not answering every query. **Projections** consume events and build purpose-specific read models.

For example, a customer dashboard may need:

| Account | Owner | Balance | Status |
|---|---|---:|---|
| A-1042 | Ada | $125.00 | Open |
| A-2081 | Linus | $0.00 | Closed |

A projection can maintain this table:

```python
@dataclass
class AccountSummary:
    account_id: str
    owner: str
    balance: Decimal
    status: str


def project_summary(
    summaries: dict[str, AccountSummary],
    event: AccountEvent,
    account_id: str,
) -> None:
    match event:
        case AccountOpened(_, owner, _):
            summaries[account_id] = AccountSummary(
                account_id=account_id,
                owner=owner,
                balance=Decimal("0"),
                status="Open",
            )
        case MoneyDeposited(amount, _):
            summaries[account_id].balance += amount
        case MoneyWithdrawn(amount, _):
            summaries[account_id].balance -= amount
        case AccountClosed(_):
            summaries[account_id].status = "Closed"
```

Another projection might generate monthly statements. A third might count withdrawals for fraud monitoring. They can all consume the same historical facts.

### **Eventual consistency**

When projections update asynchronously, a command may succeed before a read model reflects the new event:

```text
write accepted → event persisted → projection catches up → query reflects change
```

This delay is called eventual consistency. It must be handled explicitly in the user experience. Common approaches include:

- returning the accepted result directly from the command;
- showing a “processing” state;
- waiting until a projection reaches a known event position;
- using a synchronous projection where latency and coupling are acceptable.

### **Idempotent projections**

Delivery is frequently at least once, so a projection may receive an event more than once. Track processed event IDs or make the update naturally idempotent.

```python
def process_once(
    event_id: str,
    processed_ids: set[str],
    handler,
) -> None:
    if event_id in processed_ids:
        return

    handler()
    processed_ids.add(event_id)
```

In a database, the read-model update and processed-ID insert should occur in one transaction.

---

## **11. Testing Event-Sourced Systems**

Event-sourced domain logic has a natural **Given–When–Then** structure:

- **Given** historical events,
- **When** a command is handled,
- **Then** new events or an error are expected.

### **11.1 Successful command**

```python
from datetime import UTC, datetime


FIXED_TIME = datetime(2026, 1, 15, 12, 0, tzinfo=UTC)


def fixed_clock() -> datetime:
    return FIXED_TIME


def test_withdrawal_emits_event() -> None:
    given = [
        AccountOpened("A-1", "Ada", FIXED_TIME),
        MoneyDeposited(Decimal("100.00"), FIXED_TIME),
    ]
    account = BankAccount.from_history(given)

    account.handle(WithdrawMoney(Decimal("35.00")), fixed_clock)

    assert account.pending_events == [
        MoneyWithdrawn(Decimal("35.00"), FIXED_TIME)
    ]
    assert account.state.balance == Decimal("65.00")
```

### **11.2 Rejected command**

```python
import pytest


def test_withdrawal_rejects_insufficient_funds() -> None:
    given = [
        AccountOpened("A-1", "Ada", FIXED_TIME),
        MoneyDeposited(Decimal("20.00"), FIXED_TIME),
    ]
    account = BankAccount.from_history(given)

    with pytest.raises(InsufficientFunds):
        account.handle(WithdrawMoney(Decimal("35.00")), fixed_clock)

    assert account.pending_events == []
    assert account.state.balance == Decimal("20.00")
```

### **11.3 Replay test**

```python
def test_replay_reconstructs_state() -> None:
    history = [
        AccountOpened("A-1", "Ada", FIXED_TIME),
        MoneyDeposited(Decimal("100.00"), FIXED_TIME),
        MoneyWithdrawn(Decimal("25.00"), FIXED_TIME),
        MoneyDeposited(Decimal("10.00"), FIXED_TIME),
    ]

    account = BankAccount.from_history(history)

    assert account.state.account_id == "A-1"
    assert account.state.balance == Decimal("85.00")
    assert account.state.version == 4
    assert account.pending_events == []
```

Good test suites also verify:

- every supported historical schema version can be decoded;
- snapshots and full replay yield identical state;
- projections are idempotent;
- concurrency conflicts are detected;
- unknown event types fail visibly rather than being silently skipped.

---

## **12. Common Mistakes and Practical Trade-offs**

### **Mistake 1: Treating events as commands**

Bad:

```python
class WithdrawMoney:
    amount: Decimal
```

Persisting `WithdrawMoney` leaves ambiguity: was it requested, approved, rejected, or completed?

Better:

```python
class MoneyWithdrawn:
    amount: Decimal
```

### **Mistake 2: Performing side effects during replay**

Bad:

```python
def apply_account_opened(state, event):
    send_welcome_email(event.owner)  # Repeats on every replay!
    state.is_open = True
```

Side effects should be triggered by newly persisted events through a separate handler, not by the pure state-evolution path.

### **Mistake 3: Using events as generic property changes**

Weak event:

```json
{"type": "FieldChanged", "field": "balance", "value": "125.00"}
```

Domain event:

```json
{"type": "MoneyDeposited", "amount": "25.00"}
```

The domain event preserves intent and remains useful to downstream consumers.

### **Mistake 4: Ignoring event ordering**

Within one aggregate stream, order is part of meaning. A withdrawal before a deposit may be rejected; the same withdrawal after the deposit may be valid. Persist and replay a stable stream position.

### **Mistake 5: Publishing before persistence**

If an event is sent to a message broker before it is durably appended, downstream systems may observe a fact that the authoritative store later loses. Transactional outbox patterns or event-store subscriptions help keep persistence and publication aligned.

### **Mistake 6: Building a distributed transaction in disguise**

An aggregate should protect a small, explicit consistency boundary. If every command requires atomically loading and writing dozens of streams, the boundary is probably wrong.

### **The real costs**

Event sourcing introduces material complexity:

- long-lived event schema management;
- replay-safe code;
- eventual consistency;
- projection operations and monitoring;
- duplicate and out-of-order delivery handling;
- more demanding debugging tools;
- privacy and deletion challenges for immutable data.

These are justified only when historical facts and temporal behavior have real business value.

---

## **13. When to Use Event Sourcing**

Event sourcing is a strong candidate when:

- the full history is itself valuable;
- auditability must be intrinsic rather than bolted on;
- business decisions depend on complex temporal rules;
- multiple read models need the same sequence of facts;
- retroactive analysis or rebuilding views matters;
- disputes require explaining exactly how a state arose.

Typical domains include financial ledgers, inventory movements, workflow engines, booking systems, collaborative editing, and regulated approval processes.

Prefer conventional state persistence when:

- the application is primarily CRUD;
- historical reconstruction has little value;
- the team cannot support schema evolution and projection operations;
- low-complexity consistency is more important than temporal modeling;
- events would merely duplicate database rows without adding business meaning.

### **Decision matrix**

| Question | If “yes” | If “no” |
|---|---|---|
| Must every accepted change be explainable later? | Favors event sourcing | Snapshot state may suffice |
| Are historical facts used by several consumers? | Favors event streams | Direct updates may be simpler |
| Is eventual consistency acceptable for reads? | Projections are viable | Prefer synchronous state |
| Can event schemas be maintained for years? | Long-term model is feasible | Avoid permanent event contracts |
| Does the domain have meaningful transitions? | Events capture intent | CRUD may be the honest model |

Event sourcing can be applied selectively. One bounded context—such as payments—may use it while profile settings remain ordinary relational rows.

---

## **14. Complete Example**

The following compact program ties together commands, events, decisions, replay, and versioned persistence:

```python
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import TypeAlias


# ---------- Events ----------

@dataclass(frozen=True)
class Opened:
    account_id: str
    owner: str
    at: datetime


@dataclass(frozen=True)
class Deposited:
    amount: Decimal
    at: datetime


@dataclass(frozen=True)
class Withdrawn:
    amount: Decimal
    at: datetime


Event: TypeAlias = Opened | Deposited | Withdrawn


# ---------- Commands ----------

@dataclass(frozen=True)
class Open:
    account_id: str
    owner: str


@dataclass(frozen=True)
class Deposit:
    amount: Decimal


@dataclass(frozen=True)
class Withdraw:
    amount: Decimal


Command: TypeAlias = Open | Deposit | Withdraw


# ---------- State and domain logic ----------

@dataclass
class State:
    account_id: str | None = None
    owner: str | None = None
    balance: Decimal = Decimal("0")
    version: int = 0


def evolve(state: State, event: Event) -> None:
    match event:
        case Opened(account_id, owner, _):
            state.account_id = account_id
            state.owner = owner
        case Deposited(amount, _):
            state.balance += amount
        case Withdrawn(amount, _):
            state.balance -= amount
    state.version += 1


def decide(
    state: State,
    command: Command,
    now: Callable[[], datetime],
) -> list[Event]:
    match command:
        case Open(account_id, owner):
            if state.account_id is not None:
                raise ValueError("Account already exists")
            if not owner.strip():
                raise ValueError("Owner is required")
            return [Opened(account_id, owner.strip(), now())]

        case Deposit(amount):
            require_existing(state)
            require_positive(amount)
            return [Deposited(amount, now())]

        case Withdraw(amount):
            require_existing(state)
            require_positive(amount)
            if amount > state.balance:
                raise ValueError("Insufficient funds")
            return [Withdrawn(amount, now())]

    raise TypeError(f"Unknown command: {command!r}")


def require_existing(state: State) -> None:
    if state.account_id is None:
        raise ValueError("Account does not exist")


def require_positive(amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError("Amount must be positive")


# ---------- Aggregate ----------

class Account:
    def __init__(self) -> None:
        self.state = State()
        self.pending: list[Event] = []

    @classmethod
    def load(cls, history: Sequence[Event]) -> Account:
        account = cls()
        for event in history:
            evolve(account.state, event)
        return account

    def execute(self, command: Command) -> None:
        produced = decide(self.state, command, lambda: datetime.now(UTC))
        for event in produced:
            evolve(self.state, event)
            self.pending.append(event)


# ---------- Event store ----------

class Conflict(RuntimeError):
    pass


class Store:
    def __init__(self) -> None:
        self.streams: dict[str, list[Event]] = defaultdict(list)

    def read(self, stream: str) -> list[Event]:
        return list(self.streams[stream])

    def append(
        self,
        stream: str,
        expected_version: int,
        events: Sequence[Event],
    ) -> None:
        history = self.streams[stream]
        if len(history) != expected_version:
            raise Conflict(
                f"Expected version {expected_version}, got {len(history)}"
            )
        history.extend(events)


def save(store: Store, account: Account) -> None:
    assert account.state.account_id is not None
    original_version = account.state.version - len(account.pending)
    stream = f"account-{account.state.account_id}"
    store.append(stream, original_version, account.pending)
    account.pending.clear()


# ---------- Usage ----------

store = Store()

account = Account()
account.execute(Open("A-1042", "Ada"))
account.execute(Deposit(Decimal("150.00")))
account.execute(Withdraw(Decimal("25.00")))
save(store, account)

reloaded = Account.load(store.read("account-A-1042"))

assert reloaded.state.owner == "Ada"
assert reloaded.state.balance == Decimal("125.00")
assert reloaded.state.version == 3
assert reloaded.pending == []

print(reloaded.state)
```

Expected output resembles:

```text
State(account_id='A-1042', owner='Ada', balance=Decimal('125.00'), version=3)
```

The in-memory store is intentionally small. A production implementation must make version checking and appending atomic, use durable storage, serialize explicit schemas, and expose stream positions for subscriptions.

---

## **15. Further Exercises**

1. **Add account closing.** Reject closure when the balance is nonzero.
2. **Add transfer commands.** Consider carefully whether a transfer is one aggregate transaction, a process manager, or a saga.
3. **Serialize events.** Write JSON encoders and decoders with explicit schema versions.
4. **Create a statement projection.** Group deposits and withdrawals by calendar month.
5. **Add snapshots.** Save one every 100 events and prove replay gives identical results.
6. **Simulate concurrency.** Load two copies, save both, and verify the second writer receives a conflict.
7. **Make command handling idempotent.** Store command IDs so a retried request does not create a duplicate deposit.
8. **Introduce an upcaster.** Load a version-1 deposit that lacks a currency and convert it to version 2.

---

## **Summary**

Event sourcing stores an ordered history of **immutable domain facts** instead of treating current state as the only truth. Aggregates rebuild state by folding over those events, validate commands against that state, and append new events using optimistic concurrency control.

The essential separation is:

```text
Command + State  →  Events or Rejection
Event   + State  →  New State
Events           →  Projections
```

That model provides excellent auditability, historical reconstruction, and flexible read models. It also creates permanent event contracts and operational complexity. Use it where the history has real domain value—not merely because an append-only log is technically interesting.

