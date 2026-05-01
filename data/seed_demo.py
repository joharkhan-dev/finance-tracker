"""
seed_demo.py — Insert realistic demo transactions into Supabase.

Usage:
    python data/seed_demo.py

Reads Supabase credentials from .streamlit/secrets.toml (same as the app).
Safe to re-run: checks for an existing demo marker row before inserting,
so duplicate data is never created.
"""

import re
import sys
import pathlib
from datetime import date
from supabase import create_client

# ---------------------------------------------------------------------------
# CREDENTIALS — read from .streamlit/secrets.toml
# ---------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECRETS_FILE = ROOT / ".streamlit" / "secrets.toml"

if not SECRETS_FILE.exists():
    sys.exit(f"[error] secrets.toml not found at {SECRETS_FILE}")

# Simple parser for flat key = "value" TOML — no third-party dep needed.
secrets: dict[str, str] = {}
for line in SECRETS_FILE.read_text().splitlines():
    m = re.match(r'^\s*(\w+)\s*=\s*"([^"]*)"\s*$', line)
    if m:
        secrets[m.group(1)] = m.group(2)

supabase = create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])

# ---------------------------------------------------------------------------
# DEMO DATA — 3 months, 28 transactions, realistic UK amounts
# ---------------------------------------------------------------------------

TRANSACTIONS = [
    # ── March 2026 ──────────────────────────────────────────────────────────
    {
        "date": "2026-03-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 3200.00, "user": "Me",
    },
    {
        "date": "2026-03-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 2850.00, "user": "Partner",
    },
    {
        "date": "2026-03-03", "type": "Expense", "category": "Bills",
        "item": "Rent",                          "cost":  975.00, "user": "Joint",
    },
    {
        "date": "2026-03-04", "type": "Expense", "category": "Bills",
        "item": "Gas & Electric",                "cost":   87.50, "user": "Joint",
    },
    {
        "date": "2026-03-06", "type": "Expense", "category": "Food",
        "item": "Tesco Weekly Shop",             "cost":   64.30, "user": "Joint",
    },
    {
        "date": "2026-03-08", "type": "Expense", "category": "Transport",
        "item": "Monthly Rail Pass",             "cost":  148.00, "user": "Me",
    },
    {
        "date": "2026-03-10", "type": "Expense", "category": "Food",
        "item": "Nando's Dinner",                "cost":   32.80, "user": "Me",
    },
    {
        "date": "2026-03-14", "type": "Expense", "category": "Entertainment",
        "item": "Cinema Tickets",                "cost":   22.00, "user": "Joint",
    },
    {
        "date": "2026-03-17", "type": "Expense", "category": "Shopping",
        "item": "New Running Shoes",             "cost":   89.99, "user": "Me",
    },
    {
        "date": "2026-03-19", "type": "Expense", "category": "Food",
        "item": "Sainsbury's Midweek Shop",      "cost":   41.15, "user": "Joint",
    },
    {
        "date": "2026-03-21", "type": "Income",  "category": "Income",
        "item": "Freelance Web Project",         "cost":  750.00, "user": "Me",
    },
    {
        "date": "2026-03-24", "type": "Expense", "category": "Health",
        "item": "Gym Membership",                "cost":   35.00, "user": "Me",
    },
    {
        "date": "2026-03-27", "type": "Expense", "category": "Bills",
        "item": "Broadband & Phone",             "cost":   52.00, "user": "Joint",
    },
    {
        "date": "2026-03-29", "type": "Expense", "category": "Entertainment",
        "item": "Spotify & Netflix",             "cost":   21.98, "user": "Joint",
    },

    # ── April 2026 ──────────────────────────────────────────────────────────
    {
        "date": "2026-04-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 3200.00, "user": "Me",
    },
    {
        "date": "2026-04-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 2850.00, "user": "Partner",
    },
    {
        "date": "2026-04-03", "type": "Expense", "category": "Bills",
        "item": "Rent",                          "cost":  975.00, "user": "Joint",
    },
    {
        "date": "2026-04-05", "type": "Expense", "category": "Food",
        "item": "Tesco Weekly Shop",             "cost":   71.20, "user": "Joint",
    },
    {
        "date": "2026-04-09", "type": "Expense", "category": "Shopping",
        "item": "Spring Clothing Haul",          "cost":  134.50, "user": "Partner",
    },
    {
        "date": "2026-04-12", "type": "Expense", "category": "Transport",
        "item": "Petrol",                        "cost":   58.40, "user": "Me",
    },
    {
        "date": "2026-04-15", "type": "Expense", "category": "Health",
        "item": "Dentist Checkup",               "cost":   60.00, "user": "Partner",
    },
    {
        "date": "2026-04-18", "type": "Expense", "category": "Food",
        "item": "Date Night Restaurant",         "cost":   78.00, "user": "Joint",
    },
    {
        "date": "2026-04-22", "type": "Expense", "category": "Bills",
        "item": "Council Tax",                   "cost":  143.00, "user": "Joint",
    },
    {
        "date": "2026-04-26", "type": "Expense", "category": "Entertainment",
        "item": "Gym Day Pass + Sauna",          "cost":   18.00, "user": "Partner",
    },

    # ── May 2026 ────────────────────────────────────────────────────────────
    {
        "date": "2026-05-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 3200.00, "user": "Me",
    },
    {
        "date": "2026-05-01", "type": "Income",  "category": "Income",
        "item": "Monthly Salary",                "cost": 2850.00, "user": "Partner",
    },
    {
        "date": "2026-05-01", "type": "Expense", "category": "Bills",
        "item": "Rent",                          "cost":  975.00, "user": "Joint",
    },
    {
        "date": "2026-05-03", "type": "Expense", "category": "Food",
        "item": "Tesco Weekly Shop",             "cost":   66.90, "user": "Joint",
    },
]

# A stable anchor row used to detect whether demo data already exists.
# Its item text acts as a sentinel — never used in real transactions.
SENTINEL_ITEM = "__demo_seed_v1__"

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def already_seeded() -> bool:
    result = (
        supabase.table("transactions")
        .select("id")
        .eq("item", SENTINEL_ITEM)
        .limit(1)
        .execute()
    )
    return len(result.data) > 0


def insert_sentinel():
    supabase.table("transactions").insert({
        "date":     str(date.today()),
        "type":     "Expense",
        "category": "Bills",
        "item":     SENTINEL_ITEM,
        "cost":     0.00,
        "user":     "Me",
    }).execute()


def insert_all():
    supabase.table("transactions").insert(TRANSACTIONS).execute()


def print_summary():
    by_month: dict[str, dict] = {}
    for tx in TRANSACTIONS:
        month = tx["date"][:7]  # "YYYY-MM"
        bucket = by_month.setdefault(month, {"income": 0.0, "expenses": 0.0, "count": 0})
        bucket["count"] += 1
        if tx["type"] == "Income":
            bucket["income"] += tx["cost"]
        else:
            bucket["expenses"] += tx["cost"]

    print("\n  Month       Txns   Income      Expenses    Net")
    print("  " + "─" * 54)
    total_in = total_ex = total_n = 0
    for month, b in sorted(by_month.items()):
        net = b["income"] - b["expenses"]
        total_in += b["income"]
        total_ex += b["expenses"]
        total_n  += net
        label = {"2026-03": "Mar 2026", "2026-04": "Apr 2026", "2026-05": "May 2026"}.get(month, month)
        sign  = "+" if net >= 0 else "-"
        print(
            f"  {label:<10}  {b['count']:>4}   "
            f"£{b['income']:>8,.2f}   £{b['expenses']:>8,.2f}   {sign}£{abs(net):,.2f}"
        )
    print("  " + "─" * 54)
    sign = "+" if total_n >= 0 else "-"
    print(
        f"  {'TOTAL':<10}  {len(TRANSACTIONS):>4}   "
        f"£{total_in:>8,.2f}   £{total_ex:>8,.2f}   {sign}£{abs(total_n):,.2f}"
    )
    print()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print(f"\n[seed_demo] Connecting to Supabase...")

    if already_seeded():
        print("[seed_demo] Demo data already present (sentinel row found). Nothing inserted.")
        print("            Delete all rows with item='__demo_seed_v1__' to re-seed.\n")
        return

    print(f"[seed_demo] Inserting {len(TRANSACTIONS)} transactions...")
    insert_all()
    insert_sentinel()

    print(f"[seed_demo] Done. Summary:\n")
    print_summary()
    print(f"[seed_demo] {len(TRANSACTIONS)} transactions inserted across Mar–May 2026.")
    print(f"[seed_demo] Open the app and set the date range to 2026-03-01 → 2026-05-31.\n")


if __name__ == "__main__":
    main()
