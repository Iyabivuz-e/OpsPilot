import asyncio
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import AsyncSessionLocal
from app.models.models import (
    User,
    Customer,
    Order,
    Payment,
    Refund,
    Return,
)

from app.helpers.id_generator import generate_id_code


# ============================================================
# CONFIGURATION
# ============================================================

NUM_USERS = 20
NUM_CUSTOMERS = 200
NUM_ORDERS = 300
NUM_REFUNDS = 50
NUM_RETURNS = 50


# ============================================================
# COMPANY USERS
# ============================================================

USERS = [
    ("Alice Martin", "alice@cortora.com", "support_agent"),
    ("Marco Rossi", "marco@cortora.com", "support_manager"),
    ("Sarah Chen", "sarah@cortora.com", "operations_admin"),
    ("Thomas Bernard", "thomas@cortora.com", "support_agent"),
    ("Sophie Laurent", "sophie@cortora.com", "support_agent"),
    ("Luca Bianchi", "luca@cortora.com", "operations_admin"),
    ("Emma Wilson", "emma@cortora.com", "support_agent"),
    ("James Anderson", "james@cortora.com", "support_manager"),
    ("Olivia Taylor", "olivia@cortora.com", "support_agent"),
    ("Daniel Martin", "daniel@cortora.com", "operations_admin"),
    ("Chloe Dubois", "chloe@cortora.com", "support_agent"),
    ("Matteo Romano", "matteo@cortora.com", "support_agent"),
    ("Emily Johnson", "emily@cortora.com", "support_agent"),
    ("Lucas Moreau", "lucas@cortora.com", "support_manager"),
    ("Anna Müller", "anna@cortora.com", "operations_admin"),
    ("David Smith", "david@cortora.com", "support_agent"),
    ("Sofia Garcia", "sofia@cortora.com", "support_agent"),
    ("Noah Brown", "noah@cortora.com", "support_manager"),
    ("Claire Martin", "claire@cortora.com", "support_agent"),
    ("Ethan Rossi", "ethan@cortora.com", "operations_admin"),
]


# ============================================================
# CUSTOMER DATA
# ============================================================

FIRST_NAMES = [
    "Jean",
    "Pierre",
    "Marie",
    "Lucas",
    "Thomas",
    "Sophie",
    "Claire",
    "Emma",
    "Oliver",
    "James",
    "Daniel",
    "Sarah",
    "Emily",
    "David",
    "Anna",
    "Sofia",
    "Liam",
    "Noah",
    "Mia",
    "Chloe",
]

LAST_NAMES = [
    "Dupont",
    "Martin",
    "Bernard",
    "Moreau",
    "Laurent",
    "Rossi",
    "Bianchi",
    "Garcia",
    "Smith",
    "Johnson",
    "Brown",
    "Wilson",
    "Taylor",
    "Müller",
    "Anderson",
]

COUNTRIES = [
    "France",
    "Italy",
    "Germany",
    "Spain",
    "United Kingdom",
    "Belgium",
    "Netherlands",
    "Switzerland",
    "Portugal",
]


# ============================================================
# BUSINESS STATES
# ============================================================

ORDER_STATUSES = [
    "PENDING",
    "PROCESSING",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED",
]

PAYMENT_STATUSES = [
    "PENDING",
    "CAPTURED",
    "FAILED",
    "DUPLICATE",
    "PARTIALLY_REFUNDED",
    "REFUNDED",
]

REFUND_STATUSES = [
    "REQUESTED",
    "PROCESSING",
    "COMPLETED",
    "FAILED",
]

RETURN_REASONS = [
    "DAMAGED",
    "WRONG_ITEM",
    "NOT_AS_DESCRIBED",
    "CHANGED_MIND",
    "DEFECTIVE",
]

RETURN_STATUSES = [
    "REQUESTED",
    "APPROVED",
    "RECEIVED",
    "INSPECTING",
    "COMPLETED",
    "REJECTED",
]


# ============================================================
# REALISTIC ORDER AMOUNTS
# ============================================================

COMMON_ORDER_TOTALS = [
    Decimal("39.99"),
    Decimal("49.99"),
    Decimal("59.99"),
    Decimal("79.99"),
    Decimal("99.99"),
    Decimal("119.99"),
    Decimal("149.99"),
    Decimal("199.99"),
    Decimal("249.99"),
    Decimal("299.99"),
    Decimal("399.99"),
    Decimal("499.99"),
    Decimal("599.99"),
    Decimal("749.99"),
    Decimal("899.99"),
    Decimal("999.99"),
    Decimal("1299.99"),
    Decimal("1499.99"),
    Decimal("1899.99"),
    Decimal("2499.99"),
]


# ============================================================
# HELPERS
# ============================================================


def now() -> datetime:
    return datetime.now(timezone.utc)


def random_datetime(days_back: int = 90) -> datetime:
    """
    Generate a realistic timestamp within the last `days_back` days.
    """

    current = now()

    seconds_back = random.randint(
        0,
        days_back * 24 * 60 * 60,
    )

    return current - timedelta(seconds=seconds_back)


def random_order_amount() -> Decimal:
    """
    Pick a realistic e-commerce order total.

    Using predefined values is more realistic than completely
    uniform random values such as €713.42.
    """

    return random.choice(COMMON_ORDER_TOTALS)


def random_customer_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def customer_email(name: str, index: int) -> str:
    safe_name = name.lower().replace(" ", ".").replace("ü", "u")

    return f"{safe_name}.{index + 1}@example.com"


def make_order_id() -> str:
    """
    Business-facing order identifier.

    Example:
        order-8F3A92
    """

    return generate_id_code("order")


def make_payment_id() -> str:
    return generate_id_code("payment")


def make_refund_id() -> str:
    return generate_id_code("refund")


def make_return_id() -> str:
    return generate_id_code("return")


def subtract_minutes(timestamp: datetime, minutes: int) -> datetime:
    return timestamp - timedelta(minutes=minutes)


def add_minutes(timestamp: datetime, minutes: int) -> datetime:
    return timestamp + timedelta(minutes=minutes)


# ============================================================
# USERS
# ============================================================


async def seed_users(
    session: AsyncSession,
) -> list[User]:

    users = []

    for name, email, role in USERS[:NUM_USERS]:
        user = User(
            name=name,
            email=email,
            role=role,
        )

        session.add(user)
        users.append(user)

    await session.flush()

    print(f"Created {len(users)} users")

    return users


# ============================================================
# CUSTOMERS
# ============================================================


async def seed_customers(
    session: AsyncSession,
) -> list[Customer]:

    customers = []

    for i in range(NUM_CUSTOMERS):
        name = random_customer_name()

        customer = Customer(
            name=name,
            email=customer_email(name, i),
            country=random.choice(COUNTRIES),
        )

        session.add(customer)
        customers.append(customer)

    await session.flush()

    print(f"Created {len(customers)} customers")

    return customers


# ============================================================
# ORDER CREATION HELPERS
# ============================================================


async def create_order(
    session: AsyncSession,
    customer: Customer,
    *,
    status: str,
    total: Decimal,
    created_at: datetime,
) -> Order:

    order = Order(
        order_id=make_order_id(),
        customer_id=customer.id,
        total=total,
        status=status,
        created_at=created_at,
        updated_at=created_at,
    )

    session.add(order)

    await session.flush()

    return order


# ============================================================
# PAYMENT CREATION
# ============================================================


async def create_payment(
    session: AsyncSession,
    order: Order,
    *,
    status: str,
    created_at: datetime,
) -> Payment:

    payment = Payment(
        payment_id=make_payment_id(),
        order_id=order.id,
        customer_id=order.customer_id,
        amount=order.total,
        status=status,
        created_at=created_at,
        updated_at=created_at,
    )

    session.add(payment)

    await session.flush()

    return payment


# ============================================================
# REFUND CREATION
# ============================================================


async def create_refund(
    session: AsyncSession,
    order: Order,
    payment: Payment,
    *,
    amount: Decimal,
    status: str,
    created_at: datetime,
) -> Refund:

    refund = Refund(
        refund_id=make_refund_id(),
        order_id=order.id,
        payment_id=payment.id,
        amount=amount,
        status=status,
        created_at=created_at,
        updated_at=created_at,
    )

    session.add(refund)

    await session.flush()

    return refund


# ============================================================
# RETURN CREATION
# ============================================================


async def create_return(
    session: AsyncSession,
    order: Order,
    *,
    reason: str,
    status: str,
    created_at: datetime,
) -> Return:

    return_record = Return(
        return_id=make_return_id(),
        order_id=order.id,
        reason=reason,
        status=status,
        created_at=created_at,
        updated_at=created_at,
    )

    session.add(return_record)

    await session.flush()

    return return_record


# ============================================================
# SCENARIO 1
# NORMAL COMPLETED ORDER
# ============================================================


async def scenario_normal_order(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(60)

    payment_time = add_minutes(created, 5)
    shipped_time = add_minutes(created, 24 * 60)
    delivered_time = add_minutes(created, 3 * 24 * 60)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=random_order_amount(),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=payment_time,
    )

    order.updated_at = delivered_time

    return order


# ============================================================
# SCENARIO 2
# PENDING PAYMENT
# ============================================================


async def scenario_pending_payment(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(7)

    order = await create_order(
        session,
        customer,
        status="PENDING",
        total=random_order_amount(),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="PENDING",
        created_at=add_minutes(created, 3),
    )

    return order


# ============================================================
# SCENARIO 3
# FAILED PAYMENT
# ============================================================


async def scenario_failed_payment(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(30)

    order = await create_order(
        session,
        customer,
        status="PENDING",
        total=random_order_amount(),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="FAILED",
        created_at=add_minutes(created, 2),
    )

    return order


# ============================================================
# SCENARIO 4
# CANCELLED ORDER
# ============================================================


async def scenario_cancelled_order(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(45)

    order = await create_order(
        session,
        customer,
        status="CANCELLED",
        total=random_order_amount(),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    order.updated_at = add_minutes(created, 90)

    return order


# ============================================================
# SCENARIO 5
# DELIVERED + REFUND REQUESTED
# ============================================================


async def scenario_refund_requested(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(40)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("249.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    refund_time = add_minutes(created, 7 * 24 * 60)

    await create_refund(
        session,
        order,
        payment,
        amount=order.total,
        status="REQUESTED",
        created_at=refund_time,
    )

    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 6
# FULL REFUND COMPLETED
# ============================================================


async def scenario_full_refund(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(50)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("399.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    refund_time = add_minutes(
        created,
        10 * 24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=order.total,
        status="COMPLETED",
        created_at=refund_time,
    )

    payment.status = "REFUNDED"

    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 7
# PARTIAL REFUND
# ============================================================


async def scenario_partial_refund(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(50)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("799.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    refund_amount = Decimal("150.00")

    refund_time = add_minutes(
        created,
        12 * 24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=refund_amount,
        status="COMPLETED",
        created_at=refund_time,
    )

    payment.status = "PARTIALLY_REFUNDED"

    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 8
# REFUND PROCESSING
# ============================================================


async def scenario_refund_processing(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(20)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("599.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    refund_time = add_minutes(
        created,
        8 * 24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=order.total,
        status="PROCESSING",
        created_at=refund_time,
    )

    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 9
# FAILED REFUND
# ============================================================


async def scenario_failed_refund(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(30)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("299.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    refund_time = add_minutes(
        created,
        6 * 24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=order.total,
        status="FAILED",
        created_at=refund_time,
    )

    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 10
# RETURN REQUESTED
# ============================================================


async def scenario_return_requested(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(30)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("449.99"),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    return_time = add_minutes(
        created,
        8 * 24 * 60,
    )

    await create_return(
        session,
        order,
        reason="CHANGED_MIND",
        status="REQUESTED",
        created_at=return_time,
    )

    order.updated_at = return_time

    return order


# ============================================================
# SCENARIO 11
# RETURN APPROVED
# ============================================================


async def scenario_return_approved(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(45)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("699.99"),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    return_time = add_minutes(
        created,
        9 * 24 * 60,
    )

    await create_return(
        session,
        order,
        reason="WRONG_ITEM",
        status="APPROVED",
        created_at=return_time,
    )

    order.updated_at = return_time

    return order


# ============================================================
# SCENARIO 12
# RETURN COMPLETED + FULL REFUND
# ============================================================


async def scenario_completed_return(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(60)

    order = await create_order(
        session,
        customer,
        status="RETURNED",
        total=Decimal("899.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    return_time = add_minutes(
        created,
        10 * 24 * 60,
    )

    await create_return(
        session,
        order,
        reason="DEFECTIVE",
        status="COMPLETED",
        created_at=return_time,
    )

    refund_time = add_minutes(
        return_time,
        24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=order.total,
        status="COMPLETED",
        created_at=refund_time,
    )

    payment.status = "REFUNDED"
    order.updated_at = refund_time

    return order


# ============================================================
# SCENARIO 13
# HIGH VALUE ORDER
# ============================================================


async def scenario_high_value_order(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(25)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("2499.99"),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    order.updated_at = add_minutes(
        created,
        5 * 24 * 60,
    )

    return order


# ============================================================
# SCENARIO 14
# MULTIPLE REFUNDS
# ============================================================


async def scenario_multiple_refunds(
    session: AsyncSession,
    customer: Customer,
) -> Order:

    created = random_datetime(60)

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=Decimal("999.99"),
        created_at=created,
    )

    payment = await create_payment(
        session,
        order,
        status="PARTIALLY_REFUNDED",
        created_at=add_minutes(created, 5),
    )

    first_refund_time = add_minutes(
        created,
        7 * 24 * 60,
    )

    second_refund_time = add_minutes(
        created,
        14 * 24 * 60,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=Decimal("100.00"),
        status="COMPLETED",
        created_at=first_refund_time,
    )

    await create_refund(
        session,
        order,
        payment,
        amount=Decimal("200.00"),
        status="COMPLETED",
        created_at=second_refund_time,
    )

    order.updated_at = second_refund_time

    return order


# ============================================================
# BACKGROUND ORDERS
# ============================================================


async def create_background_order(
    session: AsyncSession,
    customer: Customer,
) -> Order:
    """
    Create ordinary e-commerce traffic.

    These records are less important than the deliberate
    scenarios above, but they make the database look like
    a real production dataset.
    """

    created = random_datetime(90)

    scenario = random.random()

    # -----------------------------------------
    # Failed payment
    # -----------------------------------------

    if scenario < 0.05:
        order = await create_order(
            session,
            customer,
            status="PENDING",
            total=random_order_amount(),
            created_at=created,
        )

        await create_payment(
            session,
            order,
            status="FAILED",
            created_at=add_minutes(created, 3),
        )

        return order

    # -----------------------------------------
    # Pending order/payment
    # -----------------------------------------

    if scenario < 0.10:
        order = await create_order(
            session,
            customer,
            status="PENDING",
            total=random_order_amount(),
            created_at=created,
        )

        await create_payment(
            session,
            order,
            status="PENDING",
            created_at=add_minutes(created, 3),
        )

        return order

    # -----------------------------------------
    # Cancelled order
    # -----------------------------------------

    if scenario < 0.15:
        order = await create_order(
            session,
            customer,
            status="CANCELLED",
            total=random_order_amount(),
            created_at=created,
        )

        await create_payment(
            session,
            order,
            status="CAPTURED",
            created_at=add_minutes(created, 5),
        )

        order.updated_at = add_minutes(created, 120)

        return order

    # -----------------------------------------
    # Processing
    # -----------------------------------------

    if scenario < 0.25:
        order = await create_order(
            session,
            customer,
            status="PROCESSING",
            total=random_order_amount(),
            created_at=created,
        )

        await create_payment(
            session,
            order,
            status="CAPTURED",
            created_at=add_minutes(created, 5),
        )

        order.updated_at = add_minutes(created, 24 * 60)

        return order

    # -----------------------------------------
    # Shipped
    # -----------------------------------------

    if scenario < 0.40:
        order = await create_order(
            session,
            customer,
            status="SHIPPED",
            total=random_order_amount(),
            created_at=created,
        )

        await create_payment(
            session,
            order,
            status="CAPTURED",
            created_at=add_minutes(created, 5),
        )

        order.updated_at = add_minutes(
            created,
            random.randint(1, 5) * 24 * 60,
        )

        return order

    # -----------------------------------------
    # Normal delivered order
    # -----------------------------------------

    order = await create_order(
        session,
        customer,
        status="DELIVERED",
        total=random_order_amount(),
        created_at=created,
    )

    await create_payment(
        session,
        order,
        status="CAPTURED",
        created_at=add_minutes(created, 5),
    )

    order.updated_at = add_minutes(
        created,
        random.randint(3, 10) * 24 * 60,
    )

    return order


# ============================================================
# ORDERS
# ============================================================


async def seed_orders(
    session: AsyncSession,
    customers: list[Customer],
) -> list[Order]:

    orders = []

    # --------------------------------------------------------
    # Deliberate customers
    #
    # We reuse some customers for multiple important scenarios.
    # This allows OpsPilot to answer questions such as:
    #
    # "Show me everything about this customer's orders."
    #
    # --------------------------------------------------------

    scenario_customers = customers[:20]

    scenario_functions = [
        scenario_normal_order,
        scenario_pending_payment,
        scenario_failed_payment,
        scenario_cancelled_order,
        scenario_refund_requested,
        scenario_full_refund,
        scenario_partial_refund,
        scenario_refund_processing,
        scenario_failed_refund,
        scenario_return_requested,
        scenario_return_approved,
        scenario_completed_return,
        scenario_high_value_order,
        scenario_multiple_refunds,
    ]

    # --------------------------------------------------------
    # Create deliberate scenarios first.
    # --------------------------------------------------------

    for i, scenario_function in enumerate(scenario_functions):
        customer = scenario_customers[i % len(scenario_customers)]

        order = await scenario_function(
            session,
            customer,
        )

        orders.append(order)

    # --------------------------------------------------------
    # Create realistic background orders.
    # --------------------------------------------------------

    remaining_orders = NUM_ORDERS - len(orders)

    for _ in range(remaining_orders):
        customer = random.choice(customers)

        order = await create_background_order(
            session,
            customer,
        )

        orders.append(order)

    print(f"Created {len(orders)} orders")

    return orders


# ============================================================
# REALISTIC RETURN SCENARIOS
# ============================================================


async def seed_returns(
    session: AsyncSession,
    orders: list[Order],
) -> list[Return]:

    returns = []

    # --------------------------------------------------------
    # Important:
    #
    # We deliberately choose delivered orders for returns.
    # We do NOT randomly attach returns to cancelled/pending
    # orders.
    # --------------------------------------------------------

    eligible_orders = [order for order in orders if order.status == "DELIVERED"]

    random.shuffle(eligible_orders)

    selected_orders = eligible_orders[:NUM_RETURNS]

    for order in selected_orders:
        created_at = order.created_at + timedelta(
            days=random.randint(7, 25),
        )

        # Make sure the return isn't in the future.
        if created_at > now():
            created_at = now() - timedelta(hours=1)

        status_roll = random.random()

        if status_roll < 0.25:
            status = "REQUESTED"

        elif status_roll < 0.45:
            status = "APPROVED"

        elif status_roll < 0.65:
            status = "RECEIVED"

        elif status_roll < 0.80:
            status = "INSPECTING"

        elif status_roll < 0.95:
            status = "COMPLETED"

        else:
            status = "REJECTED"

        return_record = await create_return(
            session,
            order,
            reason=random.choice(RETURN_REASONS),
            status=status,
            created_at=created_at,
        )

        returns.append(return_record)

        if status == "COMPLETED":
            order.status = "RETURNED"

            order.updated_at = created_at

    print(f"Created {len(returns)} returns")

    return returns


# ============================================================
# MAIN SEED
# ============================================================


async def seed_database():

    async with AsyncSessionLocal() as session:
        try:
            print()
            print("=" * 60)
            print("CORTORA DATABASE SEED")
            print("=" * 60)
            print()

            # ------------------------------------------------
            # DELETE EXISTING DATA
            # ------------------------------------------------

            print("Removing existing data...")

            await session.execute(delete(Refund))
            await session.execute(delete(Return))
            await session.execute(delete(Payment))
            await session.execute(delete(Order))
            await session.execute(delete(Customer))
            await session.execute(delete(User))

            await session.flush()

            print("Existing data removed.")
            print()

            # ------------------------------------------------
            # USERS
            # ------------------------------------------------

            users = await seed_users(session)

            # ------------------------------------------------
            # CUSTOMERS
            # ------------------------------------------------

            customers = await seed_customers(session)

            # ------------------------------------------------
            # ORDERS
            # ------------------------------------------------

            orders = await seed_orders(
                session,
                customers,
            )

            # ------------------------------------------------
            # RETURNS
            #
            # Returns are generated AFTER orders so we can
            # deliberately select appropriate orders.
            # ------------------------------------------------

            returns = await seed_returns(
                session,
                orders,
            )

            # ------------------------------------------------
            # COMMIT
            # ------------------------------------------------

            await session.commit()

            print()
            print("=" * 60)
            print("DATABASE SEEDED SUCCESSFULLY")
            print("=" * 60)
            print()
            print(f"Users:     {len(users)}")
            print(f"Customers: {len(customers)}")
            print(f"Orders:    {len(orders)}")
            print(f"Returns:   {len(returns)}")
            print()

            print("Important scenarios included:")
            print("  - Normal delivered orders")
            print("  - Pending payments")
            print("  - Failed payments")
            print("  - Cancelled orders")
            print("  - Requested refunds")
            print("  - Processing refunds")
            print("  - Completed full refunds")
            print("  - Completed partial refunds")
            print("  - Failed refunds")
            print("  - Requested returns")
            print("  - Approved returns")
            print("  - Completed returns")
            print("  - High-value orders")
            print("  - Multiple refunds")
            print()

        except Exception:
            await session.rollback()

            print()
            print("DATABASE SEED FAILED")
            print("Transaction rolled back.")
            print()

            raise


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(seed_database())
