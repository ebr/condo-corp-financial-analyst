---
name: condo-corp-financial-analyst
description: >
  This skill should be used whenever the user wants to analyze, report on, or check the
  financial position of a condominium corporation. Use it when the user says things like
  "run the financial report", "analyze the financials", "update the financial position report",
  "what's the financial status", "generate a board financial report", "how are we doing
  financially", "check the reserve fund", "what are the flags for the board", or asks any
  question about operating fund health, reserve fund levels, arrears, variance against budget,
  or bank account balances for a condo. Also use it for focused questions like "how is the
  reserve fund doing", "show me arrears trends", or "how are we tracking against budget" —
  these benefit from the document-scanning workflow even if a full report is not requested.
  Works with any condominium corporation's document directory, regardless of jurisdiction.
---

# Condo Corporation Financial Analyst Skill

Produces a structured financial position analysis for a condominium corporation on demand.
All corporation-specific facts (name, fiscal year, unit count, bank accounts, budgets) are
discovered from documents — nothing is assumed. Supports two run modes: **incremental** (update from the prior report using only newer documents) and **full regeneration** (re-read all current-year documents from scratch). The model infers the intended mode from user language; see Step 1d.

---

## Step 1 — Orient Yourself

**1a. Check for existing reports.**
Look for a `Reports/` folder and any `*Financial-Position-Report.md` files inside it.
Sort by filename — the ISO date+time prefix makes the most recent alphabetically last.
If a prior report exists, read it and note:
- The timestamp in its filename (this is your "last report time")
- Which source documents it listed in its `Sources:` header field
- Any ongoing flags or issues already identified
- Key figures already compiled (to avoid re-deriving them)

If no prior report exists, treat all documents as new.

**1b. Check for a project context file.**
Look for `CORP.md` in the working directory root. If found, read it — it contains
corporation-specific facts (fiscal year, unit count, equipment ownership, known issues)
that the board has recorded to avoid re-deriving them from source documents every run.
Also check for `CLAUDE.md` as a fallback, in case the user stored context there.

**1c. Determine the report filename.**
Before constructing the filename, run:

```bash
date +%Y-%m-%d-%H%M
```

Use the output verbatim as the timestamp prefix. Do not guess or estimate the time —
the shell command is the only authoritative source.

Use the format: `Reports/YYYY-MM-DD-HHMM_Financial-Position-Report.md`
If the user specified a focus area, add a short focus tag:
`Reports/YYYY-MM-DD-HHMM_reserve-focus_Financial-Position-Report.md`

Always create a new file. Never overwrite an existing report, even if running multiple
times on the same day — each run is a distinct, timestamped record.

**1d. Classify the run mode.**

Infer the user's intent from their language before reading any source documents:

| Mode | User language signals | Document scope |
|---|---|---|
| **Incremental** *(default when a prior report exists)* | "update", "true-up", "refresh", "what's changed", "what's new", "quick check", no specific instruction | Only files modified after the prior report's timestamp (plus meeting documents not yet in Sources: — see Step 2 scope rule) |
| **Full regeneration** | "regenerate", "from scratch", "complete report", "redo", "full review", "rebuild", "re-read everything" — or no prior report exists | All relevant documents from the current fiscal year |

When a prior report exists and the user's intent is ambiguous, default to **Incremental**.

**Incremental synthesis model:** In incremental mode the prior report is the base. Your job is to apply the new-document diff on top of it — update only the sections where figures or flags changed, and record the delta in Section 8 (Changes Since Last Report). Do not re-derive figures already correctly established in the prior report unless a new document supersedes them.

---

## Step 2 — Discover New Source Documents

Scan `Board Meetings/` (all subdirectories) and `Documents/` for relevant files.

Apply the run mode determined in Step 1d:

**Incremental mode** — read only source documents whose modification time is after the prior report's timestamp. Exception: meeting minutes, manager's reports, and budget documents from the current fiscal year must be read if not listed in any prior report's `Sources:` field (see scope rule below). Treat the prior report as the base; update only sections where new documents change figures or flags.

**Full regeneration mode** — read all relevant source documents from the current fiscal year, plus the prior year-end statement for baseline comparison. Build all report sections from scratch.

**Static documents — read only when triggered:**
The following documents change rarely and must not be re-read on every run:
- Condo Declaration / Master Deed
- Corporation Bylaws and Rules
- Letters Patent / Articles of Incorporation
- Original engineering surveys (not the Reserve Fund Study — that has its own rule above)

Read static documents only when one of these conditions applies:
1. **Cold start or CORP.md missing constants** — read to populate CORP.md, then do not re-read in subsequent incremental runs
2. **Dynamic document cites the static document** — e.g., minutes reference "Declaration Section 4.2" — read only the cited section
3. **User explicitly asks a question about them**

If none of these conditions apply, skip static documents entirely.

**Document priority order:**

| Priority | Type | Purpose |
|---|---|---|
| 1 | Main financial statements (balance sheet + income statement) | Balance sheet figures, revenue/expense vs. budget, net income |
| 2 | Variance reports | Explanations for over/under items; arrears summary |
| 3 | Bank statements | Closing balances; cross-check against financial statement |
| 4 | Reserve Fund Study | Projections, minimum balance, contribution schedule |
| 5 | Meeting minutes, agendas, manager's reports, legal correspondence | Forward-looking exposure: capital projects, contractor quotes, committed costs, board motions — see extraction checklist below |
| 6 | Budget documents | Full-year figures for annualized context |

**Always read the Reserve Fund Study** if one exists in the corpus and it was not listed
in the prior report's sources. Even if the study is old, it is the baseline for all reserve
fund comparisons and should not be skipped.

**Meeting document extraction checklist (Priority 5 documents):**

When reading any meeting minutes, agenda, or manager's report, actively look for and record each of the following:

1. **Capital projects approved or under active consideration** — note project scope and estimated cost
2. **Contractor quotes or tenders received** — vendor category (not necessarily name), scope, and dollar amount
3. **Costs incurred or committed since the last financial statement date** — amounts not yet reflected in any financial statement
4. **Operational issues that explain statement line items** — e.g. equipment failure explaining a maintenance overrun (label the connection as an inference if the document does not state it explicitly)
5. **Board motions related to spending, reserves, or contracts** — and whether the motion was actually passed (versus merely discussed or deferred)
6. **Relevant items from a proposed or approved next-fiscal-year budget** — if the document contains budget-setting discussions or a draft budget

Record findings even when no motion was passed — pending and deferred items are forward-looking obligations the board needs visibility into.

**Worked example — Westfield Condominium Corp. No. 88**

*Fictional scenario: manager's report and board minutes from the October meeting of Westfield Condominium Corp. No. 88, a 96-unit Ontario corporation managed by Greenfield Property Services.*

> **Manager's Report (October 15, 2025):**
> "Three vendors have submitted quotes for the amenities room renovation: Stoneway Interiors ($84,500), Craftline General ($91,200), and Meridian Build Group ($78,800). The board is reviewing the proposals; no motion has been passed. The project is not yet reflected in the reserve fund expenditures."
>
> **Board Minutes (October 15, 2025):**
> "MOTION: To approve an emergency boiler repair at a cost not to exceed $12,400 — PASSED. The repair was completed October 8; invoice expected from Harbor Mechanical Services in November."

Correct extraction:

| Item | Status | Estimated Cost | Source |
|---|---|---|---|
| Amenities room renovation | Under consideration (quotes received, no motion) | $78,800–$91,200 range | Manager's report, Oct 15/25 |
| Boiler emergency repair | Approved (motion passed Oct 15/25); invoice pending | $12,400 (not to exceed) | Board minutes, Oct 15/25 |

Note: the amenities renovation quotes must **not** be described as approved — no motion was passed. The boiler repair is approved and committed, but the cost has not yet appeared in any financial statement.

**Scope rule for meeting documents:**

Meeting minutes, manager's reports, and budget documents from the current fiscal year must always be read, regardless of their modification date, if they are not listed in any prior report's `Sources:` field. These documents may predate the last report's timestamp but contain forward-looking information that was never captured in any previous report.

**While reading, discover and record:**
- Corporation name and number (from letterhead or document titles)
- Fiscal year start/end dates (from financial statement cover page)
- Unit count (from RFS or budget)
- Management company name
- All bank accounts: institution, account number, fund type, current status
- Jurisdiction (province/state/country — from incorporation documents or letterhead)

---

## Step 2b — Update CORP.md with Discovered Constants

As you read source documents, record any **structural constants** you discover into
`CORP.md` — but only if they are not already there. Never overwrite an existing entry;
the user may have manually corrected it.

**What counts as a constant** (true regardless of when the report is run):

| Constant | Example |
|---|---|
| Corporation name and number | `Corporation: Clearview Condominium Corp. No. 412` |
| Fiscal year | `Fiscal year: April 1 – March 31` |
| Unit count | `Units: 112` |
| Management company | `Property manager: Apex Property Management Inc.` |
| Jurisdiction | `Jurisdiction: Ontario, Canada` |
| Corporation address | `Address: 400 Ridgecrest Ave, Laketon, ON` |
| Bank institutions on file | `Banks: Big Reliable Bank (operating + reserve)` |
| Equipment/component ownership (once confirmed) | `Lobby intercom: common element` |

**What does NOT go in CORP.md** — these belong only in dated reports:
- Fund balances, bank balances, investment values
- YTD figures, net income, budget variances
- Accounts payable / receivable
- Flags, issues, or action items
- Anything that will differ between runs

**Mechanics:**
1. If `CORP.md` doesn't exist, create it with a brief header comment
2. For each constant you've discovered, check whether it's already recorded
3. Append only the missing ones — never modify existing lines
4. After writing, note at the end of the inline summary which constants were added,
   so the user is aware of what changed

This means `CORP.md` grows organically: after the first report run it will already
contain the corporation name, fiscal year, unit count, management company, and
jurisdiction — and the user never had to type any of it.

---

## Step 3 — Load Jurisdiction Reference

Once jurisdiction is identified, check `references/` for a matching file
(e.g., `references/ontario.md`, `references/bc.md`).

- **If found**: read it. It contains jurisdiction-specific rules (reserve fund study
  requirements, legislative references, timelines) that inform the flags you'll raise.
- **If not found**: do not invent jurisdiction-specific rules from training data alone.
  Instead, at the end of the report's inline summary, include a contributor prompt:

```
## Jurisdiction Reference Missing — Help Improve This Skill

No reference file was found for **[jurisdiction]** corporations. This means
jurisdiction-specific compliance checks (reserve fund study frequency, required notices,
legislative timelines) could not be performed for this report.

You don't need to write this yourself — just ask:

> "Research condominium reserve fund legislation and compliance requirements for
> [jurisdiction] and generate a jurisdiction reference file for the
> condo-corp-financial-analyst skill, modeled on references/ontario.md."

Claude will research and draft the file. Review it, save it to:
  ~/.claude/skills/condo-corp-financial-analyst/references/[jurisdiction-slug].md

Future reports for [jurisdiction] corporations will then include full compliance
checking automatically.

**Want to help others?** Once you've validated the file against your local legislation,
consider contributing it back — submit a PR to the skill's repository:
  https://github.com/[TBD]
```

---

## Step 4 — Extract Key Figures

For each financial statement, extract and **source-cite** each figure:

```
Operating cash: $412,800 — Big Reliable Bank operating account (balance sheet, FS dated Oct 31/25)
Reserve fund total: $1,953,000 — sum of investments ($1,618,000) + Big Reliable Bank reserve
  ($290,000) + interest receivable ($45,000) — FS dated Oct 31/25
```

Figures to extract from each balance sheet:
- **Operating cash**: sum of all operating bank account balances (all institutions)
- **Reserve fund total**: cash + investments + interest receivable (all reserve assets)
- **Reserve investments**: specific investment portfolio line item
- **Total liabilities**
- **Accounts payable**
- **Accounts receivable** (note: separate from chargeback receivable if both present)
- **YTD surplus/(deficit)**: from fund balances section

From income statement:
- Total revenues actual vs. YTD budget → variance
- Total expenses actual vs. YTD budget → variance
- Net income/(loss) vs. YTD budget

**Bank statement cross-check:**
For any bank account where both a statement and a financial statement line item are available,
compare closing balances. Flag any discrepancy > $100 with the specific amount and possible
explanation (rounding, cheques in transit, timing).

---

## Step 5 — Epistemic Hygiene

Before writing the report, apply this discipline rigorously:

**Documented facts**: things explicitly stated in source documents. Report these directly.
Example: "Elevator preventive maintenance was $3,100 in Q2, $1,400 over the quarterly
budget of $1,700, per the Q2 variance report from Diligent Contracting."

**Inferences**: conclusions drawn by combining information. Label them clearly.
Example: "Waste removal costs increased $2,200 over budget in the same period that the
variance report noted a compactor breakdown — the two are likely connected, though the
report does not explicitly state this."

**Assumptions**: things not stated or inferable from documents. Avoid making them.
If context is genuinely unclear, say so explicitly rather than filling the gap.
Example: "The balcony door hardware maintenance line ($4,200 YTD) is over budget by $3,100.
It is unclear from available documents whether this represents repairs to a common element
assembly or relates to a unit-owner replacement program — the variance report provides no
explanation. The board should request clarification from management."

This discipline protects the board from acting on inaccurate characterizations of projects,
costs, or decisions.

---

## Step 6 — Apply User Focus (if any)

If the user specified a focus, shape the report accordingly:

- **Reserve fund focus**: Expand Sections 2 and 3 with year-by-year RFS comparison table;
  calculate trajectory to minimum balance threshold
- **Arrears focus**: Pull arrears tables from all variance reports; show trend over time;
  note any chronic accounts
- **Operating / budget focus**: Expand variance analysis; flag persistent overruns
- **Year-end projection**: Extrapolate YTD actuals to fiscal year close
- **Specific issue**: Address it first with depth, then provide abbreviated full report

Even for focused questions, still produce and save a full report. The focus shapes emphasis,
not completeness.

Note the focus in both the filename and the report header (see Step 7).

---

## Step 7 — Write the Report

```markdown
# [Corporation Name]
## Financial Position Report
**Date:** [run `date '+%Y-%m-%d %H:%M'` and use the output exactly]
**Focus:** [user-specified focus, or "General — full review"]
**Jurisdiction:** [province/state/country, or "Unknown — verify locally"]
**Period Covered:** [earliest period] – [latest period in documents]
**Sources:** [list each document read, with its date]
**Prepared by:** Board analysis

---

## 1. Operating Fund — Trend Summary

[Table: Period (YTD) | Revenue | Expenses | Net Income/(Loss) | vs. YTD Budget]

[Narrative — with source citations for key figures. Note one-time items separately from
structural trends. Label inferences explicitly.]

**Operating Cash (bank balances):**
[Table: Date | [Bank 1] | [Bank 2 if applicable] | Total]

---

## 2. Reserve Fund — Trend Summary

[Table: Date | Total Reserve Assets | Investments | Cash | Interest Receivable]

[Narrative — source-cited. Note investment liquidations if investment balance decreased.]

**Reserve Capital Expenditures (from trial balance or statement of reserve fund, YTD):**
[Table: Project category | Amount spent YTD]

Net reserve drawdown = total expenditures − (contributions + interest earned)

---

## 3. Reserve Fund Study Context

[Include only if RFS has been read. Show:]
- Study date, preparer, class type
- Key parameters (inflation assumption, interest assumption, unit count)
- **Projected vs. actual table** for current fiscal year
- Minimum projected balance and year it occurs
- Whether a study update is legally due (per jurisdiction reference file)
- Whether actual capital spending pace deviates significantly from RFS projections

---

## 4. Notable Variances

### Positive Variances (Under Budget)
[Table: Item | YTD Variance | Source | Note]

### Negative Variances (Over Budget)
[Table: Item | YTD Variance | Source | Note]

[For any item over budget with no explanation in variance reports, say so explicitly.
Do not infer a reason. Flag it for management follow-up.]

[Flag items that appear over budget in multiple consecutive variance reports — these are
structural, not one-time.]

---

## 5. Summary Scorecard

| Metric | [Period 1] | ... | [Latest period] |
|---|---|---|---|
| Operating cash | | | |
| Reserve fund total | | | |
| Reserve investments | | | |
| Total liabilities | | | |
| Accounts payable | | | |
| Accounts receivable | | | |
| YTD net income/(loss) | | | |

---

## 6. Priority Flags for the Board

[Table: Priority | Issue | Action]

- 🔴 High: Legal/compliance risk, material budget deviation, unresolved personnel issue,
  significant discrepancy requiring immediate action
- 🟡 Medium: Watch items, unexplained variances, minor discrepancies, items to monitor
- 🟢 Positive: Strong performance, resolved issues, favorable trends worth noting

---

## 7. Overall Assessment

[Table: Area | Status (✅ / ⚠️ / ❌) | Trend]

---

## 8. Changes Since Last Report [prior report filename]

[Only if a prior report existed. Show:]
- New flags not in the previous report
- Flags from the previous report that are now resolved
- Metrics that moved materially

If no new documents were found since the prior report, state that explicitly here and
note that the figures and flags are unchanged. This section still serves as a record
that the report was run and the source corpus was verified.

---

## 9. Forward-Looking Context — Approved and Pending Expenditures

*Populated from meeting minutes, manager's reports, and budget documents. Cite the source document for every item. Do not imply board approval where no motion was passed.*

### Capital Projects — Approved or Under Active Consideration

| Project | Status | Estimated Cost | Fund Source | Source Document |
|---|---|---|---|---|
| [project description] | [see status options below] | $X | Operating / Reserve / TBD | [document name, date] |

Status options:
- **Approved** — motion passed (cite meeting date)
- **Under consideration** — quotes received or discussed, no motion passed
- **Tendering in progress** — RFP or tender issued, no award yet
- **Deferred** — considered and explicitly deferred to a future meeting

### Operating Costs — Committed or Pending

| Item | Status | Estimated Cost | Source Document |
|---|---|---|---|
| [description] | Committed (invoice pending) / Approved / Pending decision | $X | [document name, date] |

### Operational Context for Statement Line Items

[Narrative connecting meeting document content to specific line items in the financial statements. Example: "The maintenance line item running $8,200 over YTD budget is consistent with the boiler emergency repair discussed in the October board minutes — *inference, not explicitly stated in the financial statements*."]

Label all inferences explicitly. If no meeting documents were read, state: "No meeting documents were available for this period."

---

*Report generated [output of `date '+%Y-%m-%d %H:%M'`]. Based on unaudited internal financial statements.
Figures are source-cited inline. Inferences are labeled as such.*
```

---

## Step 8 — Save and Summarize

**Save** to: `Reports/YYYY-MM-DD-HHMM[_focus-tag]_Financial-Position-Report.md`
(Use the timestamp captured via `date +%Y-%m-%d-%H%M` in Step 1c — do not re-derive it.)
Create `Reports/` if it doesn't exist. Never overwrite an existing file.

**Output inline to the user:**

```
## Report Summary

[2–3 sentences: overall picture in plain language]

**Top figures (as of [latest period]):**
- Operating cash: $X
- Reserve fund total: $X
- YTD net income/(loss): $X vs. $X YTD budget

**New flags since [prior report date]:** [list, or "None — no new documents"]

**Report saved:** Reports/[filename]

**CORP.md updated:** [list constants added, e.g. "Added fiscal year, unit count, jurisdiction"
— or "No new constants discovered" if nothing was added]
```

**If any ambiguities were flagged during the analysis** (e.g., unclear whether a
maintenance item is a common element or owner responsibility, unresolved variance
explanations, uncertain project scope), append this prompt after the summary:

```
## Improve Future Reports — Add a Context File

This report flagged [N] item(s) that could not be resolved from the available documents:
- [list each ambiguity briefly]

To avoid these flags in future reports, create a file called `CORP.md` in this
working directory and record what you know:

  **CORP.md** — example entries:
  - "Lobby intercom system: common element, maintained by the corporation."
  - "Parking gate motor: reserve fund capital item, not owner responsibility."
  - "Fiscal year: June 1 – May 31."
  - "Unit count: 84 residential + 6 commercial."
  - "Jurisdiction: Ontario, Canada."

The skill reads `CORP.md` automatically at the start of each run (Step 1b), so
resolved facts are never re-questioned. Over time this file becomes the authoritative
single source of truth for your corporation's particulars.
```

---

## Common Patterns to Watch For

Raise these as flags when observed, even if the variance report doesn't mention them:

- **Reserve fund study overdue**: Check jurisdiction reference for required frequency.
  If no jurisdiction file, flag for local verification.
- **Capital spending vs. RFS projections**: If actual > 1.5× projected for the year,
  the funding model may be outdated.
- **Persistent personnel vacancy**: Cleaning or caretaking wages consistently underspent +
  growing relief costs = ongoing vacancy or turnover with operational implications.
- **AR spikes without explanation**: Sudden increase in accounts receivable between periods
  warrants investigation.
- **Bank/FS discrepancies**: Any gap > $100 persisting across periods needs reconciliation.
- **Rising accounts payable**: May indicate cash flow pressure or delayed contractor payments.
- **Unexplained variance report silences**: If a line item is significantly over budget but
  the variance report provides no explanation, flag it — don't fill the gap with inference.
