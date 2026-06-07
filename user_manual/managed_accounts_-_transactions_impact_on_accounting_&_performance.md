Path**:** **Menu **\> **Transactions **\> **Managed Accounts**

**Types of MA transactions & impact**

**Contribution**

**Use: **To enter the contribution for a fund along with any expenses/
charges.

**Reports Impact: **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I): **Total Amount is used as Cashflow.

- **General Ledger Impact: **Custodian Account is debited with capital
  \"Amount\" and expenses added will impact respective ledger accounts.

**Negative Amount Support: **

- Amount - Yes.

- Expense & Fees - No.

 

**Withdrawal**

**Use: **To enter the withdrawal for a fund along with any
incomes/expenses/ charges.

**Reports Impact: **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I): **Total Amount is used as Cashflow.

- **General Ledger Impact: **Custodian Account is credited with capital
  \"Amount\" and expenses/incomes added will impact respective ledger
  accounts.

**Negative Amount Support:**

- Amount - Yes.

- Income - Yes.

- Expense & Fees- only supported for Realized Loss.

**Comments: **Withdrawal should be added as first transactions before
adding a contribution.

 

**Income**

**Use: **To capture Income received from the fund.

**Reports Impact:**

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I): **Total Amount is used as Cashflow.

- **General Ledger Impact: **Amounts added under fields will impact
  respective income/expense ledgers.

**Negative Amount Support:**

- Income - Yes. 

- TDS - No.

 

**Expense**

**Use: **To capture Expense related to the fund.

**Reports Impact:**

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I):** Total Amount is used as Cashflow.

- **General Ledger Impact: **Amounts added under fields will impact
  respective income/expense ledgers.

**Negative Amount Support:**

- Only supported for Realized Loss.

- Others - No.

**Cost Basis Adjustment (CBA)**

**Use: **To increase or decrease Tax Basis of the Fund without having an
impact on cash flow.

**Reports Impact:**

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I):** No
  Cash flow Impact while computing IRR/TWR. Cost (Tax basis) will be
  adjusted accordingly.

- **General Ledger Impact: **Cost will be impacted because of the CBA
  transaction.

**Negative Amount Support: **Yes.

 

**Valuation**

**Use: **To capture a valuation of the fund as of a date.

**Reports Impact:**

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I): **Used as End Market Value (EMV) on cashflow dates and as of
  report generation date for Valuations*.*

- **General Ledger Impact: **No voucher impact. Balance Sheet will
  consider the last valuation transaction (when run on \'valuation\'
  basis).

**Negative Amount Support: **Yes.

**Comments:** Valuation cannot be added as first transaction.

 

**Quick Notes**

- *Valuation transactions to be entered at regular intervals for system
  to compute expected unrealized gain/loss and capture correct
  performance (IRR/TWR) numbers.*

- *If Valuation not available on report date, system will consider the
  latest available valuation before report date.*

- *If no valuation entered for the fund, system will consider Valuation
  as the running ledger balance of the fund on report date.*

- *The system captures Automatic Valuation when there is at least one
  valuation transaction present in the system prior to report period.
  This is to facilitate auto incremental valuation propagation for those
  interim reporting dates where there is no specific valuation entered
  following a Contribution / Withdrawal transaction.\*

*If Valuation is not available on report date, System will dynamically
compute Valuation for reports to aid TWR, IRR computation. *

- *Auto Valuation = Last available valuation transaction before report
  period start date.\
  plus sum of all Capital Amount in Contribution transactions.\
  minus sum of Total Amount in Withdrawals transactions.\
  between the valuation transaction date and the report valuation date.\
  Standalone Income / Expense transactions do not contribute to the
  change in Automatic Valuation.\*

- *System will consider position completely sold off when ledger balance
  is zero and valuation is zero if either of the two are not zero then
  it will be considered as open position on Analytics and GL Reports.*

**We hope you are now familiar with MA types and its impact. Still have
questions? Reach out to AV\'s Customer Success Team.**
