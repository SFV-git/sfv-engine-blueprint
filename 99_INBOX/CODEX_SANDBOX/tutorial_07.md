# **Dependency Injection: Building Software from Replaceable Parts**

> **Randomly selected concept:** Dependency Injection  
> **Language used in examples:** Python 3.11+  
> **Level:** Intermediate, with a beginner-friendly introduction

Dependency injection—usually shortened to **DI**—is a design technique in which an
object receives the other objects it needs instead of constructing them itself.
That small change in responsibility can make a codebase easier to test, configure,
extend, and understand.

This tutorial develops the idea from first principles. It starts with tightly
coupled code, refactors it one step at a time, discusses several injection styles,
and finishes with a realistic example and practical design guidance.

---

## **Table of Contents**

1. [The Core Idea](#1-the-core-idea)
2. [Why Hidden Construction Causes Problems](#2-why-hidden-construction-causes-problems)
3. [Constructor Injection](#3-constructor-injection)
4. [Programming to a Contract](#4-programming-to-a-contract)
5. [Testing with Fakes](#5-testing-with-fakes)
6. [Other Injection Styles](#6-other-injection-styles)
7. [Composition Roots](#7-composition-roots)
8. [A Complete Example](#8-a-complete-example)
9. [Lifetimes and Resource Management](#9-lifetimes-and-resource-management)
10. [Common Mistakes](#10-common-mistakes)
11. [When Dependency Injection Is Worth Using](#11-when-dependency-injection-is-worth-using)
12. [Exercises](#12-exercises)
13. [Summary](#13-summary)

---

## **1. The Core Idea**

A **dependency** is anything a piece of code relies on to do its work. A service
that sends a receipt might depend on:

- a database;
- an email provider;
- a clock;
- a logger;
- application configuration.

Without dependency injection, the service often creates those collaborators
internally:

```python
class ReceiptService:
    def send_receipt(self, order_id: int) -> None:
        database = PostgreSQLDatabase("postgresql://localhost/shop")
        emailer = SMTPEmailer("smtp.example.com")

        order = database.find_order(order_id)
        emailer.send(
            to=order.customer_email,
            subject="Your receipt",
            body=f"Thank you for order {order.id}.",
        )
```

With dependency injection, the collaborators are supplied from outside:

```python
class ReceiptService:
    def __init__(self, database, emailer) -> None:
        self.database = database
        self.emailer = emailer

    def send_receipt(self, order_id: int) -> None:
        order = self.database.find_order(order_id)
        self.emailer.send(
            to=order.customer_email,
            subject="Your receipt",
            body=f"Thank you for order {order.id}.",
        )
```

The second class does not know how a database connection or an email client is
created. It only knows how to use them. Construction is somebody else's job.

**Dependency injection is therefore an inversion of control:** control over
selecting and constructing collaborators moves out of the class that uses them.

### **A useful mental model**

Think of a wall outlet. A lamp requires electrical power, but it does not contain
its own power station. It accepts power through a standard interface. You can move
the lamp between compatible power sources without redesigning the lamp.

Good dependency boundaries work in much the same way:

```text
application setup ──creates──> database
        │
        ├───────────creates──> emailer
        │
        └──injects both into──> ReceiptService
```

---

## **2. Why Hidden Construction Causes Problems**

Creating dependencies inside a class is not automatically wrong. Constructing a
small, deterministic value object may be entirely reasonable. Trouble appears
when the hidden dependency performs I/O, holds mutable state, is expensive, or
may need to vary between environments.

Consider this price calculator:

```python
import requests


class PriceCalculator:
    def total_in_usd(self, amount: float, currency: str) -> float:
        response = requests.get(
            "https://rates.example/api/latest",
            params={"base": currency},
            timeout=5,
        )
        response.raise_for_status()
        rate = response.json()["rates"]["USD"]
        return round(amount * rate, 2)
```

The arithmetic is simple, but a unit test now depends on:

- a working network;
- a reachable third-party server;
- valid third-party data;
- response time;
- the exchange rate at the instant the test runs.

The code also hard-codes the transport library and API location. A business rule
has become entangled with infrastructure.

### **Coupling in practical terms**

Coupling describes how much one component knows about another. The calculator
above knows:

1. that rates come from HTTP;
2. that `requests` is the chosen HTTP library;
3. the provider's URL;
4. the provider's JSON shape;
5. the provider's error behavior.

Most of that knowledge is unrelated to calculating a total. Extracting it behind
a dependency gives each component a smaller, clearer responsibility.

```python
class PriceCalculator:
    def __init__(self, rate_provider) -> None:
        self.rate_provider = rate_provider

    def total_in_usd(self, amount: float, currency: str) -> float:
        rate = self.rate_provider.usd_rate(currency)
        return round(amount * rate, 2)
```

Now the calculator expresses the business rule directly: obtain a rate, multiply,
and round.

---

## **3. Constructor Injection**

**Constructor injection** passes dependencies to an object when the object is
created. It is usually the best default because it makes required dependencies
explicit and prevents the creation of an unusable object.

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    sku: str
    price: Decimal


class ProductService:
    def __init__(self, repository, audit_log) -> None:
        self._repository = repository
        self._audit_log = audit_log

    def change_price(self, sku: str, new_price: Decimal) -> Product:
        product = self._repository.get(sku)
        updated = Product(sku=product.sku, price=new_price)
        self._repository.save(updated)
        self._audit_log.record(f"{sku}: {product.price} -> {new_price}")
        return updated
```

The signature documents what the service needs:

```python
service = ProductService(repository=repository, audit_log=audit_log)
```

Compare that with an object that can be created without its required dependency:

```python
class FragileProductService:
    def __init__(self) -> None:
        self.repository = None

    def change_price(self, sku, new_price):
        # This fails later and far away from construction.
        product = self.repository.get(sku)
```

Constructor injection offers several properties:

| Property | Practical consequence |
|---|---|
| Dependencies are visible | Readers can understand requirements from the signature |
| Object starts complete | Missing dependencies fail during construction |
| Fields can remain stable | Dependencies need not change halfway through an operation |
| Tests control collaborators | Fakes can be supplied without patching global state |
| Wiring is centralized | Environment-specific choices stay outside business logic |

### **Validate at the boundary when useful**

Python does not enforce type annotations at runtime. For critical boundaries, a
small validation may produce a clearer error:

```python
class ReportService:
    def __init__(self, renderer) -> None:
        if not hasattr(renderer, "render"):
            raise TypeError("renderer must provide a render(report) method")
        self._renderer = renderer
```

Do not duplicate a full static type checker at runtime. Validate only where the
failure would otherwise be obscure or where untrusted plugins enter the system.

---

## **4. Programming to a Contract**

Injection is most useful when the consumer depends on a **capability** rather than
a concrete implementation. In Python, that contract can be informal, expressed
with an abstract base class, or described with a `Protocol`.

### **Using a protocol**

A protocol supports structural typing: an object satisfies the contract if it has
the required methods, even if it does not explicitly inherit from the protocol.

```python
from typing import Protocol


class ExchangeRateProvider(Protocol):
    def usd_rate(self, source_currency: str) -> float:
        """Return the number of USD per unit of source_currency."""
        ...


class PriceCalculator:
    def __init__(self, rates: ExchangeRateProvider) -> None:
        self._rates = rates

    def total_in_usd(self, amount: float, currency: str) -> float:
        return round(amount * self._rates.usd_rate(currency), 2)
```

A production implementation can perform HTTP I/O:

```python
import requests


class HttpExchangeRateProvider:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0) -> None:
        self._base_url = base_url
        self._timeout = timeout_seconds

    def usd_rate(self, source_currency: str) -> float:
        response = requests.get(
            f"{self._base_url}/latest",
            params={"base": source_currency},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return float(response.json()["rates"]["USD"])
```

A local implementation can use fixed values:

```python
class FixedExchangeRateProvider:
    def __init__(self, rates: dict[str, float]) -> None:
        self._rates = rates

    def usd_rate(self, source_currency: str) -> float:
        try:
            return self._rates[source_currency]
        except KeyError:
            raise ValueError(f"Unsupported currency: {source_currency}") from None
```

Both objects satisfy the consumer's contract.

```python
production_calculator = PriceCalculator(
    HttpExchangeRateProvider("https://rates.example/api")
)

demo_calculator = PriceCalculator(
    FixedExchangeRateProvider({"CAD": 0.73, "EUR": 1.08})
)
```

### **Keep contracts consumer-shaped**

A common mistake is injecting a large general-purpose client:

```python
class CheckoutService:
    def __init__(self, giant_cloud_sdk) -> None:
        self._cloud = giant_cloud_sdk
```

The checkout service probably needs one narrow capability, such as charging a
payment. Expressing only that capability reduces accidental coupling:

```python
class PaymentGateway(Protocol):
    def charge(self, account_id: str, cents: int) -> str:
        """Charge an account and return a transaction ID."""
        ...
```

Narrow contracts are easier to understand, implement, and fake.

---

## **5. Testing with Fakes**

Dependency injection makes deterministic unit tests possible without replacing
module globals or intercepting constructors.

```python
def test_converts_cad_to_usd() -> None:
    rates = FixedExchangeRateProvider({"CAD": 0.75})
    calculator = PriceCalculator(rates)

    result = calculator.total_in_usd(20.00, "CAD")

    assert result == 15.00
```

The test has no network access, no delay, and no externally changing data.

### **Fakes, stubs, spies, and mocks**

These terms are sometimes used loosely, but the distinctions help:

| Test double | Purpose | Example |
|---|---|---|
| **Stub** | Returns predetermined answers | A rate provider always returning `0.75` |
| **Fake** | Provides a lightweight working implementation | An in-memory repository |
| **Spy** | Records how it was called | An email sender storing sent messages |
| **Mock** | Verifies predefined interaction expectations | A framework object expecting one call |

Here is a simple spy:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SentEmail:
    recipient: str
    subject: str
    body: str


class RecordingEmailSender:
    def __init__(self) -> None:
        self.sent: list[SentEmail] = []

    def send(self, recipient: str, subject: str, body: str) -> None:
        self.sent.append(SentEmail(recipient, subject, body))
```

The test can assert an observable interaction:

```python
def test_sends_welcome_email() -> None:
    email = RecordingEmailSender()
    service = RegistrationService(email_sender=email)

    service.register("ada@example.com")

    assert email.sent == [
        SentEmail(
            recipient="ada@example.com",
            subject="Welcome",
            body="Your account is ready.",
        )
    ]
```

Prefer small hand-written fakes when they remain clear. Heavy use of framework
mocks can make tests mirror implementation details too closely. Such tests may
break during harmless refactoring even though application behavior is unchanged.

### **Inject nondeterminism**

Time, randomness, and generated identifiers are dependencies too:

```python
from datetime import datetime, timezone
from typing import Callable


class TokenService:
    def __init__(
        self,
        now: Callable[[], datetime],
        generate_token: Callable[[], str],
    ) -> None:
        self._now = now
        self._generate_token = generate_token

    def issue(self) -> dict[str, object]:
        return {
            "token": self._generate_token(),
            "issued_at": self._now(),
        }
```

The test controls both values:

```python
def test_issues_token_with_timestamp() -> None:
    fixed_time = datetime(2026, 1, 10, 12, 0, tzinfo=timezone.utc)
    service = TokenService(
        now=lambda: fixed_time,
        generate_token=lambda: "token-123",
    )

    assert service.issue() == {
        "token": "token-123",
        "issued_at": fixed_time,
    }
```

---

## **6. Other Injection Styles**

Constructor injection is the default, but it is not the only form.

### **Method injection**

Pass a dependency to the particular method that needs it:

```python
class Invoice:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def export(self, formatter) -> bytes:
        return formatter.format(self.lines)
```

Method injection fits when the dependency:

- is needed for only one operation;
- naturally varies on every call;
- is part of the operation's input rather than the object's identity.

### **Property injection**

Assign the dependency after construction:

```python
class ImportJob:
    logger = None

    def run(self) -> None:
        if self.logger is not None:
            self.logger.info("Import started")
```

Property injection can support optional framework hooks, but it has a cost: the
object may temporarily exist in an incomplete state. Required dependencies should
generally not use this style.

### **Parameter injection with plain functions**

Dependency injection does not require classes or a container:

```python
from collections.abc import Callable


def load_json(
    path: str,
    read_text: Callable[[str], str],
    parse_json: Callable[[str], dict],
) -> dict:
    return parse_json(read_text(path))
```

Often a function parameter is the simplest and most honest form of injection.

### **Style comparison**

| Style | Best fit | Main drawback |
|---|---|---|
| Constructor | Required, long-lived collaborators | Constructor may grow if a class does too much |
| Method | Operation-specific collaborator | Repetition if nearly every method needs it |
| Property | Optional integration hook | Object can be incompletely initialized |
| Function parameter | Small functional units | Long signatures if boundaries are poorly chosen |

---

## **7. Composition Roots**

If business objects no longer construct their dependencies, something still must.
The place where the application creates and connects its object graph is called
the **composition root**.

For a command-line application, it might be `main()`:

```python
def main() -> None:
    config = load_config()

    database = PostgreSQLOrderRepository(config.database_url)
    email_sender = SMTPEmailSender(
        hostname=config.smtp_host,
        port=config.smtp_port,
    )
    service = ReceiptService(
        database=database,
        emailer=email_sender,
    )

    command = parse_arguments()
    service.send_receipt(command.order_id)


if __name__ == "__main__":
    main()
```

This is the one area where concrete classes are expected. Its job is to decide:

- which implementations to use;
- what configuration they receive;
- how long instances live;
- how dependencies are connected.

Keeping those decisions near the program's entry point prevents infrastructure
choices from leaking across the codebase.

### **Manual wiring versus a DI container**

A **DI container** can register providers and resolve object graphs automatically.
Containers are common in frameworks and large applications, but they are not the
definition of dependency injection.

Manual wiring:

```python
repository = SqlOrderRepository(connection)
payments = StripePaymentGateway(api_key)
checkout = CheckoutService(repository, payments)
```

Conceptual container wiring:

```python
container.register(OrderRepository, SqlOrderRepository)
container.register(PaymentGateway, StripePaymentGateway)
checkout = container.resolve(CheckoutService)
```

| Manual wiring | Container wiring |
|---|---|
| Explicit and easy to trace | Concise for large object graphs |
| Requires no framework | Can manage scopes and lifecycle |
| More repetitive at scale | May hide where objects come from |
| Errors are usually local | Misconfiguration may fail at runtime |

Start with manual wiring. Introduce a container when the size and repetition of
the composition root justify the additional abstraction.

Avoid using a container as a global service locator:

```python
# Avoid: dependencies are hidden again.
class CheckoutService:
    def checkout(self, cart):
        gateway = global_container.resolve(PaymentGateway)
        gateway.charge(cart.total)
```

Although a container is present, this is not effective constructor injection. The
class still reaches outward to obtain a hidden dependency.

---

## **8. A Complete Example**

The following miniature order workflow separates domain behavior, persistence,
notifications, and setup.

### **Step 1: Define domain data and contracts**

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Order:
    id: str
    customer_email: str
    total_cents: int
    status: str = "pending"


class OrderRepository(Protocol):
    def get(self, order_id: str) -> Order:
        ...

    def save(self, order: Order) -> None:
        ...


class PaymentGateway(Protocol):
    def charge(self, customer_email: str, amount_cents: int) -> str:
        ...


class EmailSender(Protocol):
    def send(self, recipient: str, subject: str, body: str) -> None:
        ...
```

### **Step 2: Write the application service**

```python
class CheckoutService:
    def __init__(
        self,
        orders: OrderRepository,
        payments: PaymentGateway,
        email: EmailSender,
    ) -> None:
        self._orders = orders
        self._payments = payments
        self._email = email

    def checkout(self, order_id: str) -> str:
        order = self._orders.get(order_id)

        if order.status != "pending":
            raise ValueError(f"Order {order_id} is not pending")

        transaction_id = self._payments.charge(
            order.customer_email,
            order.total_cents,
        )

        paid_order = Order(
            id=order.id,
            customer_email=order.customer_email,
            total_cents=order.total_cents,
            status="paid",
        )
        self._orders.save(paid_order)

        self._email.send(
            recipient=order.customer_email,
            subject="Payment received",
            body=f"Transaction: {transaction_id}",
        )
        return transaction_id
```

Notice what this service does **not** know: SQL, HTTP endpoints, API keys, SMTP
ports, or framework globals. It coordinates a use case through narrow contracts.

### **Step 3: Create test implementations**

```python
class InMemoryOrderRepository:
    def __init__(self, orders: list[Order] | None = None) -> None:
        self._orders = {order.id: order for order in orders or []}

    def get(self, order_id: str) -> Order:
        try:
            return self._orders[order_id]
        except KeyError:
            raise LookupError(f"Unknown order: {order_id}") from None

    def save(self, order: Order) -> None:
        self._orders[order.id] = order


class FakePaymentGateway:
    def __init__(self, transaction_id: str = "tx-test") -> None:
        self.transaction_id = transaction_id
        self.charges: list[tuple[str, int]] = []

    def charge(self, customer_email: str, amount_cents: int) -> str:
        self.charges.append((customer_email, amount_cents))
        return self.transaction_id


class RecordingEmailSender:
    def __init__(self) -> None:
        self.messages: list[tuple[str, str, str]] = []

    def send(self, recipient: str, subject: str, body: str) -> None:
        self.messages.append((recipient, subject, body))
```

### **Step 4: Test the use case**

```python
def test_checkout_charges_saves_and_notifies() -> None:
    original = Order(
        id="order-7",
        customer_email="grace@example.com",
        total_cents=2599,
    )
    orders = InMemoryOrderRepository([original])
    payments = FakePaymentGateway("tx-789")
    email = RecordingEmailSender()
    service = CheckoutService(orders, payments, email)

    transaction_id = service.checkout("order-7")

    assert transaction_id == "tx-789"
    assert payments.charges == [("grace@example.com", 2599)]
    assert orders.get("order-7").status == "paid"
    assert email.messages == [
        (
            "grace@example.com",
            "Payment received",
            "Transaction: tx-789",
        )
    ]
```

This test verifies the complete application workflow while remaining fast and
deterministic. Separate integration tests should verify that the real repository,
payment adapter, and email adapter work with their external systems.

---

## **9. Lifetimes and Resource Management**

Dependencies have lifetimes. Choosing the wrong lifetime can cause leaks,
cross-request data contamination, or needless setup cost.

| Lifetime | Meaning | Typical examples |
|---|---|---|
| Transient | New instance for each use | Lightweight formatter |
| Request/scoped | Shared within one operation | Database session, request context |
| Singleton | Shared for the process lifetime | Immutable configuration, connection pool |

Do not interpret “singleton” as “make everything global.” A process-wide object
can still be explicitly created at the composition root and injected.

### **Resources should have clear owners**

For resources such as files and database transactions, context managers make
ownership explicit:

```python
def run_import(session_factory, importer, path: str) -> None:
    with session_factory() as session:
        importer.import_file(path, session)
        session.commit()
```

Here the orchestration layer owns the session lifetime. The importer uses the
session but does not silently open or close it.

### **Factories are dependencies**

Sometimes a service must create several short-lived objects. Inject a factory
instead of injecting one long-lived instance:

```python
from collections.abc import Callable


class BatchProcessor:
    def __init__(self, session_factory: Callable[[], "Session"]) -> None:
        self._session_factory = session_factory

    def process(self, batches: list[list[dict]]) -> None:
        for batch in batches:
            with self._session_factory() as session:
                session.insert_all(batch)
                session.commit()
```

The consumer controls *when* instances are needed; the composition root still
controls *how* they are created.

---

## **10. Common Mistakes**

### **Mistake 1: Injecting every trivial value**

Not every object construction needs abstraction:

```python
# This is usually fine.
full_name = f"{first_name} {last_name}".strip()
result = Money(cents=amount, currency="USD")
```

Inject dependencies that cross meaningful boundaries or create meaningful
variation. Wrapping deterministic language features usually adds noise.

### **Mistake 2: Constructor explosion**

A class with twelve injected dependencies is not proof that DI failed. It is often
evidence that the class owns too many responsibilities.

```python
class EverythingService:
    def __init__(
        self,
        users,
        orders,
        inventory,
        payments,
        email,
        sms,
        analytics,
        audit,
        cache,
        clock,
        ids,
        config,
    ):
        ...
```

Group dependencies only when they form a genuine cohesive abstraction. Otherwise,
split the service around separate use cases.

### **Mistake 3: Interfaces with one method for every implementation detail**

An abstraction is valuable when it establishes a stable boundary. Creating an
interface merely to mirror every concrete class creates ceremony without
decoupling.

Ask: **Does the consumer need a stable capability that could reasonably vary or
that should be isolated during testing?**

### **Mistake 4: Leaking infrastructure types into domain code**

This signature claims to abstract persistence but exposes a database-specific
cursor:

```python
def approve_order(order_id: str, cursor: PsycopgCursor) -> None:
    ...
```

A domain-shaped repository or unit-of-work contract makes the boundary clearer:

```python
def approve_order(order_id: str, orders: OrderRepository) -> None:
    ...
```

### **Mistake 5: Testing only through mocks**

DI improves unit testing, but unit tests do not prove that real adapters match
external systems. Use a balanced test strategy:

- unit tests for business rules with fakes;
- contract tests shared by fake and real implementations;
- integration tests for databases, queues, and APIs;
- a small number of end-to-end tests for critical paths.

### **Mistake 6: Confusing DI with global lookup**

This hides the dependency:

```python
def create_invoice(order):
    logger = services.get("logger")
    database = services.get("database")
```

This exposes it:

```python
def create_invoice(order, logger, database):
    ...
```

Explicit inputs make local reasoning possible.

---

## **11. When Dependency Injection Is Worth Using**

DI is especially useful at boundaries involving:

- databases and repositories;
- remote APIs;
- file systems and object storage;
- queues and event buses;
- clocks and randomness;
- payment, email, and identity providers;
- application configuration;
- observability systems.

It is less compelling for:

- immutable value objects;
- pure calculations;
- private helper objects with no I/O or meaningful variation;
- tiny scripts whose entire lifetime is a few lines.

### **A practical decision checklist**

Consider injection when at least one answer is “yes”:

1. Will tests need to avoid this collaborator?
2. Does the implementation vary by environment?
3. Does it perform I/O or depend on nondeterministic state?
4. Is construction expensive or lifecycle-sensitive?
5. Would the consumer be clearer if infrastructure details moved elsewhere?

The objective is not maximum abstraction. The objective is to place choices and
side effects at boundaries where they can be controlled.

---

## **12. Exercises**

### **Exercise 1: Inject a clock**

Refactor the following class so the test can control the current time:

```python
from datetime import datetime


class Greeting:
    def message(self) -> str:
        hour = datetime.now().hour
        return "Good morning" if hour < 12 else "Good afternoon"
```

<details>
<summary><strong>One possible solution</strong></summary>

```python
from collections.abc import Callable
from datetime import datetime


class Greeting:
    def __init__(self, now: Callable[[], datetime]) -> None:
        self._now = now

    def message(self) -> str:
        return "Good morning" if self._now().hour < 12 else "Good afternoon"


def test_morning_greeting() -> None:
    greeting = Greeting(lambda: datetime(2026, 6, 30, 9, 0))
    assert greeting.message() == "Good morning"
```

</details>

### **Exercise 2: Extract a repository**

Refactor this function so business logic does not contain SQL:

```python
def deactivate_user(connection, user_id: int) -> None:
    row = connection.execute(
        "SELECT status FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if row is None:
        raise LookupError(user_id)
    if row["status"] == "admin":
        raise ValueError("Administrators cannot be deactivated")
    connection.execute(
        "UPDATE users SET status = 'inactive' WHERE id = ?", (user_id,)
    )
```

Aim for a `UserRepository` contract with `get()` and `save()` operations.

### **Exercise 3: Find the composition root**

Take a small application you know and identify:

1. where configuration is loaded;
2. where database and network clients are constructed;
3. where application services are created;
4. whether any service reaches into a global registry.

Sketch a `main()` function that centralizes these decisions.

### **Exercise 4: Detect over-injection**

Review each dependency in one constructor and classify it:

| Question | Keep injected if… |
|---|---|
| Does it perform I/O? | Usually yes |
| Does it vary by environment? | Usually yes |
| Is it nondeterministic? | Usually yes |
| Is it a pure value object? | Usually no |
| Is it used by only one method? | Consider method injection |

---

## **13. Summary**

Dependency injection moves dependency construction out of the code that consumes
those dependencies. Its essential pattern is simple:

```python
# Construct at the boundary.
repository = SqlRepository(database_url)
notifier = EmailNotifier(smtp_config)

# Inject into application behavior.
service = AccountService(repository, notifier)

# Execute the use case.
service.create_account(command)
```

The main lessons are:

- **Prefer constructor injection** for required collaborators.
- **Depend on narrow, consumer-shaped contracts**, not broad infrastructure APIs.
- **Keep concrete wiring in a composition root** near the application entry point.
- **Use fakes to make unit tests fast and deterministic**, while retaining
  integration tests for real adapters.
- **Treat lifecycle as part of the design**, especially for connections, sessions,
  and transactions.
- **Avoid indiscriminate abstraction**; inject boundaries and meaningful sources
  of variation, not every object in the program.

Used carefully, dependency injection does more than make mocking convenient. It
makes a program's assumptions visible, separates policy from infrastructure, and
turns rigid object graphs into components that can evolve independently.

---

> **Final rule of thumb:** If a component chooses *what work should happen*, inject
> the mechanisms that determine *how external work gets done*.
