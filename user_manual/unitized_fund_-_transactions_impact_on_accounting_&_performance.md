**Path:** **Menu **\> **Transactions **\> **Unitized** **Funds**.

Types of UF transactions and impact:

**Contribution**

**Use : **To enter the contribution of fund along with any
expenses/charges paid.

**Reports Impact : **

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I) : **Total
  Amount is used as Cashflow.

- **General Ledger Impact : **Custodian account is debited with
  \"Amount\". \"Expenses & Fees\" amounts impact respective expense
  ledgers.

**Negative Amount Support :** No

 

**Withdrawal**

**Use :** To enter the withdrawal of fund along with any gain/loss and
income/expense incurred.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  : **Total Amount is used as Cashflow.

- **General Ledger Impact : **Custodian account is credited with
  \"Amount\". \"Income\" and \"Expenses & Fees\" amounts impact
  respective income/expense ledgers.

**Negative Amount Support :**

- Amount - No.

- Income - Yes.

- Expenses & Fees - No.

**Comments :** It should not be entered as a first transaction for the
position. There should be always a Contribution entered before
Withdrawal.

**Income**

**Use :** To capture Income received from the fund.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  : **Total Amount is used as Cashflow.

- **General Ledger Impact : **\"Income\" and \"TDS\" amounts impact
  respective income/expense ledgers 

**Negative Amount Support :**

- Income - Yes.

-  TDS - No.

 

**Expense**

**Use :** To capture Expense related to the fund.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  : **Total Amount is used as Cashflow.

- **General Ledger Impact : **\"Expenses & Fees\" amounts impact
  respective income/expense ledgers. 

**Negative Amount Support : **No.

 

**Valuation**

**Use :** To capture a valuation of the fund as of a date.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  : **Used as End Market Value (EMV) on cashflow dates and report
  generation date.

- **General Ledger Impact : **No Impact on accounting entries; Balance
  sheet with Valuation will consider Last Valuation.

**Negative Amount Support : **No.\
*\*
**Comments : **It should not be entered as a first transaction for the
position.

 

**Quick Notes**

- *System will consider position completely sold off when ledger balance
  is zero and valuation is zero if either of the two are not zero then
  it will be considered as open position on Analytics and GL Reports.*

- *Valuation transactions to be entered at regular intervals for system
  to compute expected unrealized gain/loss and capture correct
  performance numbers.*

- *If Valuation not available on report date, system will consider the
  price from the latest available valuation before report date*

- *If no valuation entered for the fund, system will consider Valuation
  as the running ledger balance of the fund on report date*

**We hope you are now familiar with UF types and its impact. Still have
questions? Reach out to AV\'s Customer Success Team.**
