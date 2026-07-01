# **Finite State Machines: Making Stateful Programs Predictable**

> A practical, implementation-focused guide to modeling behavior as a finite set of
> states and explicit transitions.

---

## **Table of Contents**

1. [Why State Machines Matter](#1-why-state-machines-matter)
2. [The Core Model](#2-the-core-model)
3. [Designing a State Machine](#3-designing-a-state-machine)
4. [Implementation Patterns in Python](#4-implementation-patterns-in-python)
5. [A Complete Example: Order Processing](#5-a-complete-example-order-processing)
6. [Testing State Machines](#6-testing-state-machines)
7. [Common Mistakes and Better Designs](#7-common-mistakes-and-better-designs)
8. [Hierarchical and Concurrent State Machines](#8-hierarchical-and-concurrent-state-machines)
9. [When to Use—or Avoid—a State Machine](#9-when-to-useor-avoida-state-machine)
10. [Exercises](#10-exercises)
11. [Summary and Cheat Sheet](#11-summary-and-cheat-sheet)

---

## **1. Why State Machines Matter**

Many programs behave differently depending on what happened earlier:

- A media player can be **playing**, **paused**, or **stopped**.
- An online order can be **created**, **paid**, **shipped**, or **cancelled**.
- A network connection can be **disconnected**, **connecting**, or **connected**.
- A document can be **draft**, **under review**, or **published**.

This history-dependent behavior is called **stateful behavior**. It often begins as a
few Boolean variables:

```python
is_connected = False
is_connecting = False
has_error = False
is_retrying = False
```

That representation looks simple, but four independent Booleans allow
`2⁴ = 16` combinations. Which combinations are valid? Can a connection be both
connected and connecting? Can it be retrying without an error? The data structure
does not answer those questions.

A **finite state machine**, or **FSM**, replaces ambiguous combinations with:

1. A finite set of named states.
2. A finite set of events.
3. Explicit rules describing which event moves the system between which states.

Instead of asking whether several flags happen to agree, the program can say:

```python
connection_state = ConnectionState.CONNECTING
```

The central benefit is not terser code. It is **making valid behavior explicit and
invalid behavior difficult—or impossible—to represent**.

---

## **2. The Core Model**

### **2.1 The five ingredients**

A deterministic finite state machine can be described as a tuple:

```text
(States, Events, Transition Function, Initial State, Final States)
```

| Ingredient | Meaning | Example |
|---|---|---|
| **States** | All modes the system may occupy | `LOCKED`, `UNLOCKED` |
| **Events** | Inputs that may trigger behavior | `COIN`, `PUSH` |
| **Transition function** | Maps a state and event to the next state | `(LOCKED, COIN) → UNLOCKED` |
| **Initial state** | State occupied at startup | `LOCKED` |
| **Final states** | Optional completed or accepting states | `COMPLETED` |

The **transition function** is the heart of the model:

```text
next_state = transition(current_state, event)
```

For a deterministic machine, a given `(state, event)` pair has no more than one
result.

### **2.2 A turnstile example**

Consider a subway turnstile:

| Current state | Event | Next state | Side effect |
|---|---|---|---|
| `LOCKED` | `COIN` | `UNLOCKED` | Unlock gate |
| `LOCKED` | `PUSH` | `LOCKED` | Sound alarm |
| `UNLOCKED` | `PUSH` | `LOCKED` | Lock after passage |
| `UNLOCKED` | `COIN` | `UNLOCKED` | Return coin |

The same event can have different meanings in different states. A `PUSH` is an
invalid attempt when locked but a successful passage when unlocked.

A compact state diagram is:

```text
              COIN
       ┌─────────────────┐
       │                 ▼
   ┌────────┐         ┌──────────┐
   │ LOCKED │         │ UNLOCKED │
   └────────┘         └──────────┘
       ▲                 │
       └─────────────────┘
              PUSH

   LOCKED + PUSH  → LOCKED   (alarm)
   UNLOCKED + COIN → UNLOCKED (refund)
```

### **2.3 States are not events**

A useful naming test is:

- A **state** usually answers, “What condition is the system in?”  
  Examples: `PENDING`, `ACTIVE`, `CLOSED`.
- An **event** usually answers, “What just happened?”  
  Examples: `APPROVE`, `TIMEOUT`, `CANCEL`.

Avoid states named `APPROVE` or events named `APPROVED`. Keeping states and events
grammatically distinct improves diagrams, logs, and code.

### **2.4 Transitions, actions, and guards**

A realistic transition may include more than a next state:

- A **guard** is a condition that must be true.
- An **action** is work performed during the transition.
- A **side effect** changes something outside the state machine, such as sending
  email or charging a card.

For example:

```text
PENDING --[PAY, if inventory_available] / charge_card --> PAID
```

Here, `PAY` is the event, inventory availability is the guard, and charging the
card is the action.

---

## **3. Designing a State Machine**

### **3.1 Start with observable behavior**

Before writing code, list:

1. The stable conditions the system can occupy.
2. The events the system receives.
3. The valid response to each event in each state.
4. The transitions that are forbidden.
5. The external actions each valid transition requires.

Suppose a support ticket may be opened, assigned, resolved, reopened, and closed.
A first model might be:

```text
OPEN → ASSIGNED → RESOLVED → CLOSED
           ▲          │
           └─ REOPEN ─┘
```

The diagram exposes questions early:

- Can an unassigned ticket be resolved?
- Can a closed ticket be reopened?
- Who is permitted to close it?
- Does reopening retain the previous assignee?

These are domain questions. A state machine does not decide the answers, but it
forces the team to state them.

### **3.2 Build a transition table**

Diagrams are intuitive; tables are systematic. For every state-event pair, specify
the outcome:

| State | `ASSIGN` | `RESOLVE` | `REOPEN` | `CLOSE` |
|---|---|---|---|---|
| `OPEN` | `ASSIGNED` | Invalid | Invalid | Invalid |
| `ASSIGNED` | `ASSIGNED` | `RESOLVED` | Invalid | Invalid |
| `RESOLVED` | Invalid | `RESOLVED` | `ASSIGNED` | `CLOSED` |
| `CLOSED` | Invalid | Invalid | Invalid | `CLOSED` |

Two design choices are visible here:

- Repeating `ASSIGN` in `ASSIGNED` is **idempotent**.
- Repeating `CLOSE` in `CLOSED` is also idempotent.

Idempotency is valuable in distributed systems because events may be delivered more
than once.

### **3.3 Decide how invalid events behave**

There is no universal answer. Common policies include:

| Policy | Behavior | Appropriate when |
|---|---|---|
| **Reject** | Raise or return an error | Invalid input indicates a caller bug |
| **Ignore** | Keep the current state | Duplicate/noisy events are expected |
| **Record** | Keep state but emit an audit entry | Attempts matter operationally |
| **Defer** | Queue the event for later | Ordering can legitimately vary |
| **Compensate** | Run corrective behavior | A distributed operation partly succeeded |

Choose the policy deliberately. Silently ignoring everything makes failures hard to
diagnose; raising on every duplicate can make a robust integration brittle.

### **3.4 Keep state meaningful**

Create a state when it changes what events are valid or what behavior occurs. Avoid
states that merely duplicate stored data.

For example, `HAS_EMAIL_ADDRESS` probably should not be a user-account state. It is
a property. In contrast, `EMAIL_VERIFICATION_PENDING` may be a useful state if it
changes which actions the user may perform.

---

## **4. Implementation Patterns in Python**

### **4.1 Pattern one: enums and explicit branching**

For a small machine, direct branching is often the clearest implementation:

```python
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    UNLOCKED = auto()


class Event(Enum):
    COIN = auto()
    PUSH = auto()


def transition(state: State, event: Event) -> State:
    if state is State.LOCKED:
        if event is Event.COIN:
            return State.UNLOCKED
        if event is Event.PUSH:
            print("Alarm!")
            return State.LOCKED

    if state is State.UNLOCKED:
        if event is Event.PUSH:
            return State.LOCKED
        if event is Event.COIN:
            print("Returning coin")
            return State.UNLOCKED

    raise ValueError(f"Unsupported transition: {state=} {event=}")
```

Advantages:

- Easy to read and debug.
- Natural place for state-specific behavior.
- No framework or abstraction overhead.

Disadvantages:

- Large machines produce deeply nested branches.
- It is difficult to inspect the whole transition graph mechanically.

### **4.2 Pattern two: a transition map**

A table-driven implementation makes the graph data:

```python
from enum import Enum, auto


class State(Enum):
    LOCKED = auto()
    UNLOCKED = auto()


class Event(Enum):
    COIN = auto()
    PUSH = auto()


TRANSITIONS: dict[tuple[State, Event], State] = {
    (State.LOCKED, Event.COIN): State.UNLOCKED,
    (State.LOCKED, Event.PUSH): State.LOCKED,
    (State.UNLOCKED, Event.PUSH): State.LOCKED,
    (State.UNLOCKED, Event.COIN): State.UNLOCKED,
}


def transition(state: State, event: Event) -> State:
    try:
        return TRANSITIONS[state, event]
    except KeyError:
        raise ValueError(
            f"Event {event.name} is invalid while in {state.name}"
        ) from None
```

Advantages:

- The transition graph is compact and inspectable.
- Completeness checks and diagram generation are straightforward.
- Transition logic remains separate from effects.

Disadvantages:

- Guards and actions require a richer transition representation.
- A huge literal table can become hard to navigate.

### **4.3 Pattern three: transition objects**

Use a small data class when transitions include actions or guards:

```python
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class State(Enum):
    DRAFT = auto()
    REVIEW = auto()
    PUBLISHED = auto()


class Event(Enum):
    SUBMIT = auto()
    APPROVE = auto()
    REJECT = auto()


Context = dict[str, Any]
Guard = Callable[[Context], bool]
Action = Callable[[Context], None]


@dataclass(frozen=True)
class Transition:
    target: State
    guard: Guard = lambda context: True
    action: Action = lambda context: None


def is_editor(context: Context) -> bool:
    return "editor" in context["roles"]


def record_publication(context: Context) -> None:
    context["audit_log"].append("Document published")


TRANSITIONS = {
    (State.DRAFT, Event.SUBMIT): Transition(State.REVIEW),
    (State.REVIEW, Event.REJECT): Transition(State.DRAFT),
    (State.REVIEW, Event.APPROVE): Transition(
        target=State.PUBLISHED,
        guard=is_editor,
        action=record_publication,
    ),
}
```

The execution function applies a predictable order:

```python
def dispatch(state: State, event: Event, context: Context) -> State:
    rule = TRANSITIONS.get((state, event))
    if rule is None:
        raise ValueError(f"{event.name} is invalid in {state.name}")

    if not rule.guard(context):
        raise PermissionError(
            f"Guard rejected {event.name} in {state.name}"
        )

    rule.action(context)
    return rule.target
```

For real external effects, think carefully about failure. If `action` succeeds but
persisting the new state fails, the machine and the outside world may disagree.
Database transactions, idempotency keys, an outbox, or compensating actions may be
needed.

---

## **5. A Complete Example: Order Processing**

This example models a simplified order:

```text
                  CANCEL
 CREATED ───────────────────────► CANCELLED
    │
    │ PAY
    ▼
  PAID ───────► CANCELLED
    │ CANCEL
    │
    │ SHIP
    ▼
 SHIPPED
    │
    │ DELIVER
    ▼
 DELIVERED
```

### **5.1 Domain definitions**

```python
from dataclasses import dataclass, field
from enum import Enum, auto


class OrderState(Enum):
    CREATED = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


class OrderEvent(Enum):
    PAY = auto()
    SHIP = auto()
    DELIVER = auto()
    CANCEL = auto()


class InvalidTransition(Exception):
    """Raised when an event is not valid for the current order state."""


@dataclass
class Order:
    order_id: str
    total_cents: int
    state: OrderState = OrderState.CREATED
    history: list[str] = field(default_factory=list)
```

### **5.2 Pure transition logic**

The transition function contains domain rules but performs no network or database
I/O:

```python
ORDER_TRANSITIONS: dict[
    tuple[OrderState, OrderEvent],
    OrderState,
] = {
    (OrderState.CREATED, OrderEvent.PAY): OrderState.PAID,
    (OrderState.CREATED, OrderEvent.CANCEL): OrderState.CANCELLED,
    (OrderState.PAID, OrderEvent.SHIP): OrderState.SHIPPED,
    (OrderState.PAID, OrderEvent.CANCEL): OrderState.CANCELLED,
    (OrderState.SHIPPED, OrderEvent.DELIVER): OrderState.DELIVERED,
}


def next_order_state(
    current: OrderState,
    event: OrderEvent,
) -> OrderState:
    try:
        return ORDER_TRANSITIONS[current, event]
    except KeyError:
        raise InvalidTransition(
            f"Cannot {event.name.lower()} an order in "
            f"{current.name.lower()} state"
        ) from None
```

### **5.3 Applying an event**

```python
def apply_event(order: Order, event: OrderEvent) -> None:
    previous = order.state
    target = next_order_state(previous, event)

    order.state = target
    order.history.append(
        f"{previous.name} --{event.name}--> {target.name}"
    )
```

Usage:

```python
order = Order(order_id="ORD-1042", total_cents=7_500)

apply_event(order, OrderEvent.PAY)
apply_event(order, OrderEvent.SHIP)
apply_event(order, OrderEvent.DELIVER)

print(order.state)
# OrderState.DELIVERED

print(*order.history, sep="\n")
# CREATED --PAY--> PAID
# PAID --SHIP--> SHIPPED
# SHIPPED --DELIVER--> DELIVERED
```

An impossible operation fails explicitly:

```python
cancelled = Order(order_id="ORD-1043", total_cents=2_500)
apply_event(cancelled, OrderEvent.CANCEL)
apply_event(cancelled, OrderEvent.SHIP)

# InvalidTransition:
# Cannot ship an order in cancelled state
```

### **5.4 Separating decisions from effects**

Payment and shipping are external operations. One workable architecture is:

```python
def handle_payment(order: Order, payment_gateway) -> None:
    # Validate before triggering the external effect.
    target = next_order_state(order.state, OrderEvent.PAY)

    receipt = payment_gateway.charge(
        amount_cents=order.total_cents,
        idempotency_key=f"payment:{order.order_id}",
    )

    previous = order.state
    order.state = target
    order.history.append(
        f"{previous.name} --PAY--> {target.name}; "
        f"receipt={receipt.id}"
    )
```

The idempotency key lets a payment provider recognize retries. In production, the
remaining consistency gap—payment succeeds, process crashes before state is
stored—still needs a recovery strategy.

### **5.5 Persistence with optimistic concurrency**

Two workers might read `PAID` and both try to ship the same order. A version field
can prevent both updates from succeeding:

```sql
UPDATE orders
SET state = 'SHIPPED',
    version = version + 1
WHERE order_id = 'ORD-1042'
  AND state = 'PAID'
  AND version = 7;
```

The worker must verify that exactly one row changed. A zero-row result means its
copy was stale or the transition was no longer valid.

---

## **6. Testing State Machines**

State machines are unusually testable because their rules form a finite graph.

### **6.1 Test valid transitions**

```python
import pytest


@pytest.mark.parametrize(
    ("current", "event", "expected"),
    [
        (OrderState.CREATED, OrderEvent.PAY, OrderState.PAID),
        (
            OrderState.CREATED,
            OrderEvent.CANCEL,
            OrderState.CANCELLED,
        ),
        (OrderState.PAID, OrderEvent.SHIP, OrderState.SHIPPED),
        (
            OrderState.PAID,
            OrderEvent.CANCEL,
            OrderState.CANCELLED,
        ),
        (
            OrderState.SHIPPED,
            OrderEvent.DELIVER,
            OrderState.DELIVERED,
        ),
    ],
)
def test_valid_transition(current, event, expected):
    assert next_order_state(current, event) is expected
```

### **6.2 Test invalid transitions exhaustively**

Instead of hand-picking a few failures, generate all state-event combinations:

```python
import pytest


ALL_PAIRS = {
    (state, event)
    for state in OrderState
    for event in OrderEvent
}

VALID_PAIRS = set(ORDER_TRANSITIONS)
INVALID_PAIRS = ALL_PAIRS - VALID_PAIRS


@pytest.mark.parametrize(("state", "event"), sorted(
    INVALID_PAIRS,
    key=lambda pair: (pair[0].name, pair[1].name),
))
def test_invalid_transitions_are_rejected(state, event):
    with pytest.raises(InvalidTransition):
        next_order_state(state, event)
```

If a new event or state is added, this test automatically covers its unspecified
combinations.

### **6.3 Test invariants**

An **invariant** must remain true regardless of the valid path taken:

```python
TERMINAL_STATES = {
    OrderState.DELIVERED,
    OrderState.CANCELLED,
}


def test_terminal_states_have_no_outgoing_transitions():
    outgoing_sources = {
        state for state, _event in ORDER_TRANSITIONS
    }

    assert TERMINAL_STATES.isdisjoint(outgoing_sources)
```

Other useful invariants include:

- Every non-initial state is reachable from the initial state.
- Every nonterminal state has at least one outgoing transition.
- Every transition targets a declared state.
- Sensitive transitions always have authorization guards.
- Terminal states cannot return to active states.

### **6.4 Test sequences**

Individual edges can be correct while a complete workflow is wrong:

```python
def test_happy_path_reaches_delivered():
    order = Order(order_id="ORD-2001", total_cents=1_000)

    for event in (
        OrderEvent.PAY,
        OrderEvent.SHIP,
        OrderEvent.DELIVER,
    ):
        apply_event(order, event)

    assert order.state is OrderState.DELIVERED
    assert len(order.history) == 3
```

Property-based testing tools can generate event sequences and verify that invariants
always hold. This becomes especially valuable as the graph grows.

---

## **7. Common Mistakes and Better Designs**

### **7.1 Boolean state explosion**

**Problem:**

```python
is_open = True
is_closed = True
```

**Better:**

```python
status = TicketStatus.CLOSED
```

Use one state value when conditions are mutually exclusive. Keep Booleans for truly
independent properties.

### **7.2 Hidden transitions**

If arbitrary code can directly assign state, the transition rules are advisory:

```python
order.state = OrderState.DELIVERED  # Bypasses payment and shipping.
```

Encapsulate mutation:

```python
class Order:
    def __init__(self) -> None:
        self._state = OrderState.CREATED

    @property
    def state(self) -> OrderState:
        return self._state

    def apply(self, event: OrderEvent) -> None:
        self._state = next_order_state(self._state, event)
```

Persistence code may still need controlled hydration, but application code should
have one obvious transition path.

### **7.3 Mixing state decisions with side effects**

A large handler that validates, charges a card, mutates state, writes a database
row, and emails a customer is hard to test and recover.

Prefer distinct concerns:

```text
Event → Validate transition → Perform coordinated effect
      → Persist transition → Publish follow-up event
```

The exact ordering depends on transaction boundaries. The important point is that
the state decision remains identifiable and testable.

### **7.4 Too many states**

Not every combination of business properties deserves a state:

```text
PAID_WITH_COUPON_AND_EXPRESS_SHIPPING
```

This creates a combinatorial model. Keep orthogonal facts as data:

```python
order.state = OrderState.PAID
order.used_coupon = True
order.shipping_method = ShippingMethod.EXPRESS
```

### **7.5 Too few states**

The opposite failure compresses meaning:

```python
status = "ACTIVE"
```

If “active but awaiting verification” and “active and fully enabled” accept
different events, they may need distinct states.

### **7.6 Persisting display labels**

Do not use human-facing labels as stable database identifiers:

```text
"Awaiting Payment"  # May change for copy or localization.
```

Persist a stable code such as `PAYMENT_PENDING` and map it to a localized label in
the presentation layer.

### **7.7 No observability**

Log transitions as structured records:

```json
{
  "entity_type": "order",
  "entity_id": "ORD-1042",
  "event": "SHIP",
  "from_state": "PAID",
  "to_state": "SHIPPED",
  "actor_id": "warehouse-worker-3",
  "correlation_id": "req-f172",
  "occurred_at": "2026-06-30T14:22:08Z"
}
```

This supports audit trails, debugging, workflow metrics, and incident analysis.
Avoid logging secrets or unnecessary personal data.

---

## **8. Hierarchical and Concurrent State Machines**

Flat FSMs are ideal when the state set is small. More complex domains may benefit
from richer models.

### **8.1 Hierarchical states**

Suppose a connection has these states:

```text
DISCONNECTED
CONNECTED
  ├── IDLE
  └── TRANSFERRING
```

`IDLE` and `TRANSFERRING` inherit behavior from `CONNECTED`. A `DISCONNECT` event
can be defined once on the parent rather than duplicated for both child states.

Hierarchical state machines reduce repeated transitions, but they introduce rules
about event lookup, entry actions, and exit actions. Define those semantics clearly.

### **8.2 Concurrent regions**

A media application might independently track:

- Playback: `PLAYING` or `PAUSED`
- Network: `ONLINE` or `OFFLINE`
- Audio: `MUTED` or `AUDIBLE`

Flattening these gives `2 × 2 × 2 = 8` composite states. Modeling three concurrent
regions keeps each concern smaller.

Concurrency is appropriate when regions are genuinely independent. If transitions
frequently require coordinated changes across every region, a single explicit
aggregate model may be clearer.

### **8.3 Pushdown automata and unbounded memory**

A finite state machine has only finite memory. It cannot naturally match arbitrary
nested structures such as balanced parentheses because nesting depth is unbounded.
A **pushdown automaton** adds a stack and is a better theoretical model for parsers
that handle recursive grammar.

In application code, ordinary data can supplement an FSM:

```python
state = DownloadState.RUNNING
bytes_received = 8_192
retry_count = 2
```

The finite state captures the control mode; associated data captures quantities
that are not finite in practice.

---

## **9. When to Use—or Avoid—a State Machine**

### **9.1 Strong use cases**

Use an FSM when:

- Behavior depends on a small, identifiable set of modes.
- Certain operations are legal only in certain modes.
- The workflow has important forbidden transitions.
- Auditing how an entity changed matters.
- Bugs arise from contradictory flags or scattered conditions.
- Events can arrive asynchronously or out of order.

Common domains include user interfaces, device controllers, games, protocol
implementations, approval workflows, payments, and job orchestration.

### **9.2 Weak use cases**

An FSM may be unnecessary when:

- The operation is stateless.
- The workflow is a simple linear sequence with no branching.
- State names merely mirror independent data properties.
- The state graph changes dynamically per user and is better represented as data.
- The central problem is numeric computation rather than control flow.

Do not introduce a framework merely because a variable changes over time. A plain
enum and one transition function are often enough.

### **9.3 Choosing an implementation**

| Machine characteristics | Suggested implementation |
|---|---|
| Fewer than roughly 10 transitions, little metadata | Explicit branching |
| Moderate graph, mostly uniform transitions | Transition map |
| Guards, actions, audit metadata | Transition objects |
| Reusable workflow designed by non-developers | Data-driven workflow engine |
| Nested states or concurrent regions | Statechart library |
| Long-running distributed process | Durable workflow/orchestration system |

The boundaries are judgment calls. Start with the smallest representation that
makes the rules explicit, and add machinery only when concrete requirements demand
it.

---

## **10. Exercises**

### **Exercise 1: Traffic signal**

Model a signal with `RED`, `GREEN`, and `YELLOW` states and a `TIMER` event.

Questions:

1. What is the initial state?
2. What transitions are valid?
3. Should an emergency event add a state or a separate property?
4. What invariants should tests enforce?

### **Exercise 2: Account lockout**

Model login behavior with these requirements:

- An account begins active.
- Five failed attempts lock it.
- An administrator can unlock it.
- A disabled account cannot be unlocked by a normal password reset.

Hint: attempt count is data, while `ACTIVE`, `LOCKED`, and `DISABLED` are candidate
states. The fifth failure is an event whose guard depends on the attempt count.

### **Exercise 3: Add refunds to the order machine**

Extend the order example:

```text
PAID ──REFUND──► REFUNDED
```

Then decide:

- Can a shipped order be refunded?
- Does refunding mean requested or completed?
- What happens if the payment provider times out?
- Is `REFUND_PENDING` necessary?
- Which events should be idempotent?

### **Exercise 4: Reachability check**

Write a function that discovers states reachable from the initial state:

```python
def reachable_states(
    initial: OrderState,
    transitions: dict[
        tuple[OrderState, OrderEvent],
        OrderState,
    ],
) -> set[OrderState]:
    ...
```

A breadth-first or depth-first graph traversal is sufficient. Compare the result
with `set(OrderState)` to detect orphaned states.

---

## **11. Summary and Cheat Sheet**

### **Core vocabulary**

| Term | Concise definition |
|---|---|
| **State** | A stable mode that affects system behavior |
| **Event** | An input or occurrence presented to the machine |
| **Transition** | A permitted movement from one state to another |
| **Guard** | A condition that permits or rejects a transition |
| **Action** | Work performed when a transition occurs |
| **Initial state** | The state in which the machine begins |
| **Terminal state** | A state with no further transitions |
| **Invariant** | A property that must remain true for all valid paths |

### **Design checklist**

- **Name states as conditions** and events as occurrences or commands.
- **Write the transition table before the implementation.**
- **Specify invalid-event behavior** rather than leaving it accidental.
- **Separate transition decisions from external effects.**
- **Prevent uncontrolled state assignment.**
- **Test all valid and invalid state-event pairs.**
- **Check reachability and terminal-state invariants.**
- **Log transitions with actor and correlation metadata.**
- **Plan for duplicates and concurrency** in distributed systems.
- **Prefer the simplest implementation** that keeps the model explicit.

### **Minimal reusable skeleton**

```python
from enum import Enum, auto


class State(Enum):
    START = auto()
    DONE = auto()


class Event(Enum):
    COMPLETE = auto()


TRANSITIONS = {
    (State.START, Event.COMPLETE): State.DONE,
}


def transition(state: State, event: Event) -> State:
    try:
        return TRANSITIONS[state, event]
    except KeyError:
        raise ValueError(
            f"Invalid transition: {state.name} + {event.name}"
        ) from None
```

Finite state machines turn implicit, scattered control rules into an explicit
graph. That graph can be reviewed, tested, logged, and reasoned about. When stateful
code feels fragile, the first useful question is often:

> **What states actually exist, and which transitions are truly valid?**

