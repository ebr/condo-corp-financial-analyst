# Condo Financial Analysis — General Reference

This file covers general condominium financial analysis concepts applicable across
jurisdictions. Jurisdiction-specific rules (reserve fund study requirements, legislative
timelines, prescribed forms) are in separate files: `references/ontario.md`, etc.

If no jurisdiction file matches the corporation's location, note the gap in the report
and flag that the board should verify local legislative requirements independently.

---

## How to Read a Condominium Balance Sheet

### Operating Fund
Covers day-to-day expenses paid from common element fees.

| Line | Meaning |
|---|---|
| Bank accounts (operating) | Liquid cash available for operations |
| Accounts receivable | Unpaid common element fees; may include chargebacks separately |
| Prepaid expenses | Insurance premiums, service contracts paid in advance |
| Accounts payable | Amounts owed to vendors and contractors |
| Accrued liabilities — operating | Expenses incurred but not yet invoiced |
| Surplus/(Deficit) | YTD net income from the income statement |

### Reserve Fund
Covers major repairs and replacements of common elements.

| Line | Meaning |
|---|---|
| Bank accounts (reserve) | Liquid cash held for reserve purposes |
| Investments — reserve fund | GICs, bonds, or other held investments |
| Interest receivable — reserve | Accrued interest not yet paid by the bank |
| Accrued liabilities — reserve | Reserve expenditures committed but not yet paid |
| Reserve fund — opening | Balance at fiscal year start |
| Reserve fund — current contribution | Transfers from operating fund YTD |
| Reserve fund — interest | Interest earned YTD |
| Reserve fund expenses (by category) | Capital expenditures drawn YTD |

### Common Reserve Fund Expense Categories
- Structure & Garage / Parking
- Building Envelope (roof, cladding, windows, doors)
- Mechanical HVAC
- Plumbing
- Electrical
- Fire & Life Safety
- Elevators / Lifts
- Amenities / Common Areas
- Site Features (landscaping, paving, fencing)
- Interior Features (corridors, lobbies, finishes)

### Important: Common Elements vs. Unit-Owned Components
Not everything in or about a building unit is a common element. In many condominium
structures, items such as in-suite appliances, interior finishes, balcony doors, and
certain mechanical components serving individual units exclusively are **owned by unit
owners**, not the corporation. Maintenance or replacement programs for such items may be
optional, owner-funded, and not a corporate liability. When a maintenance line item relates
to equipment that could be either a common element or unit-owned, do not assume which it
is — flag the ambiguity and recommend the board clarify with management and legal counsel.

---

## How to Read a Variance Report

Variance reports compare actual spending to budget. Variances in parentheses are over
budget (unfavorable); positive numbers are under budget (favorable).

Only items above a threshold (typically $1,000/month) are usually explained.

**What to watch for:**
- **Recurring over-budget items across multiple reports**: structural problem, not one-time
- **Cleaning or caretaking wages consistently under + relief costs growing**: ongoing vacancy or turnover
- **Utility overruns**: single-month spikes are usually weather events; persistent overruns
  suggest billing issues or consumption changes
- **Unexplained overruns**: if a significant variance has no explanation in the variance
  report, flag it — do not guess the reason
- **"After-hours" service calls**: signal reactive rather than preventive maintenance

---

## How to Compare Actuals to Reserve Fund Study Projections

The RFS contribution table projects opening balance, contributions, expenditures, interest,
and closing balance for each year of the study period.

To compare actual vs. projected for the current year:
1. Find the current fiscal year row in the RFS table
2. Compare projected opening balance to actual (prior year-end FS)
3. Compare projected expenditures to actual YTD capital spend (from trial balance)
4. Calculate projected closing: actual opening + contributions + interest − expenditures
5. Compare to RFS projected closing balance

**Interpretation thresholds:**
- Actual expenditures > 1.5× projected: funding model likely outdated; new study needed
- Actual fund balance < projected by > 15%: flag; check if minimum balance is at risk
- Minimum fund balance at risk: 🔴 High priority

---

## Arrears Analysis

Arrears appear in variance reports. When reviewing:
- Note total outstanding and units in arrears
- Identify chronic accounts (appearing in multiple consecutive reports, balance growing)
- Note any write-off recommendations (require board authorization)
- Calculate arrears as % of monthly common fees: >1 month of total fees outstanding
  is generally worth flagging

---

## Shared Facilities

Some corporations share amenities with adjacent buildings under a Shared Facilities
Agreement. A "Contribution to Shared Facilities" expense line indicates this. Separate
financial statements for the shared entity may exist — review independently.

---

## Bank Statement Cross-Check Protocol

1. Match bank statement period-end to financial statement date
2. Compare closing balance to the corresponding FS line item (by institution and account)
3. Note any discrepancy:
   - $0–$5: likely rounding
   - $5–$500: likely timing (cheques or deposits in transit)
   - >$500: flag for reconciliation
4. If both a bank statement and trial balance are available, the trial balance is
   authoritative for the FS; the bank statement is the independent check

---

## Report Naming Convention

`Reports/YYYY-MM-DD-HHMM[_focus-tag]_Financial-Position-Report.md`

- Always include HH:MM to avoid same-day overwrite collisions
- Add focus tag when user specified a focus area (e.g., `_reserve-focus_`, `_arrears_`)
- Sort by filename = sort by recency (ISO date+time prefix)
- Never overwrite an existing report
