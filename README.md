# Chinook Customer Concentration & Growth Pipeline

A modular Python data pipeline that loads, cleans, analyzes, and
visualizes sales data from the **Chinook** SQLite database (a
digital music store). The four questions form one connected
business story: how concentrated is this business's revenue among
its customers, how fast is it growing, and how often do customers
come back?

## Problem

A generic "top genres" report is easy. What a business actually
needs to know is riskier and more actionable: Do we depend on a
small set of VIP customers, or is revenue spread evenly? Is the
business growing month to month? How often does a typical customer
return? And exactly how many customers would we need to lose before
losing most of our revenue? These four questions -- customer
tiering, growth trend, purchase cadence, and revenue concentration
-- are the kind of analysis a real business analyst is asked to
deliver.

## Data

`data/Chinook_Sqlite.sqlite` — the standard Chinook sample database
(11 tables). This project uses `Invoice`, `InvoiceLine`, `Track`,
`Genre`, and `Customer`.

During cleaning:
- `InvoiceDate` strings are parsed to real `datetime` values.
- Tracks with no genre are labeled `"Unknown"` instead of `NaN`.
- Rows with a non-positive line total or unparsable date are dropped.
- Exact duplicate invoice lines are removed.

## Project structure

```
pipeline_project/
├── data/                       # Chinook_Sqlite.sqlite
├── pipeline/
│   ├── __init__.py
│   ├── load.py                  # get_connection, load_raw, load_table
│   ├── clean.py                  # clean()
│   ├── analyze.py                # 4 analytical questions (SQL)
│   └── visualize.py              # 1 chart function per question
├── tests/
│   ├── test_load.py
│   ├── test_clean.py
│   └── test_analyze.py           # hand-checkable results, not just "runs"
├── outputs/                      # generated .png charts land here
├── main.py                       # end-to-end entrypoint
├── requirements.txt
├── .gitignore
├── README.md
└── .github/workflows/ci.yml      # runs pytest on every push
```

## Analytical questions

| # | Business question | Analytics concept | SQL feature required | Function |
|---|--------------------|---------------------|------------------------|----------|
| 1 | How many customers are VIPs, and how much revenue do they really drive? | Customer spend-tier mapping | JOIN, GROUP BY, aggregate functions (via a derived table for 2-level aggregation) | `analyze_customer_tiers` |
| 2 | Is the business growing month over month? | Revenue trend + growth rate | Date/time functions (`strftime`) | `analyze_monthly_growth` |
| 3 | How often does a typical customer come back to buy again? | Purchase cadence distribution | CTE + correlated subquery before GROUP BY | `analyze_purchase_cadence` |
| 4 | Exactly what share of customers generates what share of revenue? | Revenue concentration (Pareto curve) | Window functions (`ROW_NUMBER()`, `SUM() OVER (...)`) | `analyze_revenue_pareto` |

Each question has a matching chart in `visualize.py` and a `.png`
saved to `outputs/` when you run `main.py`.

## Running it

```bash
pip install -r requirements.txt
python main.py          # runs the full pipeline end-to-end
pytest tests/             # runs the unit tests (13 total)
```

## Findings (example run)

- **Customer tiers (Q1):** VIP customers ($45+ lifetime spend) are
  only 8.5% of the customer base but generate 10.1% of revenue --
  almost exactly proportional. Standard customers (<$38) are 52.5%
  of customers and 50.0% of revenue. **There is no small VIP segment
  quietly carrying the business** -- every tier's revenue share
  tracks its customer share closely.
- **Growth (Q2):** revenue is a flat ~$37.62 baseline in most months,
  punctuated by occasional swings as large as +58.3% or -36.8% in a
  single month -- consistent with a small, evenly-spaced customer
  base rather than a business riding a genuine growth or decline
  trend.
- **Purchase cadence (Q3):** 36 of 59 repeat customers buy again
  within roughly 220 days on average ("Frequent"), while 7 customers
  average 280+ days between purchases ("Infrequent") -- a
  re-engagement target list, in order of priority, falls directly
  out of this segmentation.
- **Revenue concentration (Q4) -- the headline finding:** it takes
  **78% of customers to generate 80% of revenue**. This directly
  contradicts the textbook 80/20 "Pareto" assumption -- confirming
  Q1's tier finding with a second, independent technique (a
  cumulative window-function curve instead of static tier buckets).
  For this business, retention strategy should treat customers as
  roughly equally valuable rather than chasing a handful of whales.

## Challenges

- **Symptom:** the obvious "repeat purchase frequency" metric
  (orders per customer) turned out to be nearly useless -- every
  customer in Chinook has almost exactly 6-7 orders (std dev
  0.13), so a distribution built on it collapsed into a single
  bucket. **Fix:** switched Q3 to *average days between purchases*
  (purchase cadence) instead of order count, which has real spread
  (207-298 days) and produces a genuinely informative distribution.
- **Symptom:** a naive "top 20% of customers" cutoff for Q1 would
  have been arbitrary and hard to defend to a stakeholder.
  **Fix:** used fixed, interpretable dollar-based tiers (VIP/High/
  Mid/Standard) instead, then let Q4's Pareto curve verify the
  same conclusion with an entirely different, more rigorous
  technique -- two independent methods agreeing is far more
  convincing than either alone.