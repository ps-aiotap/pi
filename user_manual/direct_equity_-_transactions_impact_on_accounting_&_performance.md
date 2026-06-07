Path**:** **Menu** \> **Transactions **\> **Direct Equity**

**Buy**

**Use: **To enter the purchase of Direct Equity along with any
expenses/taxes paid.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **Net
  Amount is used as cashflow.

- **General Ledger: **Custodian account is debited with \'Net Amount\'.
  Bank account is credited with \'Gross Amount\'. \'Taxes & Charges\'
  entered impact respective expense ledgers\'. However, expenses (like
  Brokerage, Stamp Duty and other charges) except STT can be capitalized
  through uploads and its impact can be seen on the Net Amount if
  'Capital Expense' is checkbox is checked.

**Negative Amounts supported:**

- Units - No.

- Price - No.

- Taxes & Charges - Yes.

 

**Sell**

**Use: **To enter the sell transactions of Direct Equity along with any
expenses/taxes.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I):** Net
  Amount is used as cashflow.

- **General Ledger:** Custodian account is credited with \'Gross
  Amount\'. Bank account is credited with \'Net Amount\'. \'Taxes &
  Charges\' entered impact respective expense ledgers. However, expenses
  (like Brokerage, Stamp Duty and other charges) except STT can be
  capitalized through uploads and its impact can be seen on the Gross
  Amount if the 'Capital Expense' is checkbox is checked. Gain/Loss
  amount impacts the income account.

**Negative Amounts supported: **

- Units - No.

- Price - No.

- Taxes & Charges - Yes.

**Dividend Payout**

**Use: **To enter the Dividend Payout of Direct Equity along with any
taxes paid.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I) : **Net
  Amount is used as cashflow.

- **General Ledger:** Bank account is debited with \'Net Amount\'.
  \'TDS\' amount impacts respective expense ledger. Income Account is
  credited with \'Net Amount\'.

**Negative Amounts supported:**

- Income - No.

- TDS - Yes.

**Split**

**Use: **To enter the split transactions for Direct Equity.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **No
  Impact.

- **General Ledger: **No Impact.

**Negative Amounts supported: **No.

 

**Consolidation**

**Use: **To enter the consolidation transactions for Direct Equity.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **No
  Impact.

- **General Ledger: **No Impact.

**  Negative Amounts supported: **No.

 

**Bonus**

**Use: **To enter the consolidation transactions for Direct Equity.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **No
  Impact.

- **General Ledger: **No Impact.

**Negative Amounts supported: **No.

 

**Valuation (for unlisted)**

**Use: **To capture valuation of the security as on a specified date.
This transaction type is applicable only for Unlisted securities.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **Used as
  End Market Value (EMV) on cashflow dates and report generation date.

- **General Ledger: **No Impact on accounting entries; Balance sheet
  with Valuation will consider Last Valuation transaction entered.

**Negative Amounts supported:** Yes.

**Comments: **It should not be entered as a first transaction for the
position.

**Merger**

**Use: **To enter corporate action of merger for direct equity.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I):**

1.  Transfer Amount is used as cashflow.

2.  Old security is transferred out at transfer amount.

3.  New security is transferred in at transfer amount.

**General Ledger:**

- **Old Security: **Custodian account is credited with the Cost and
  Transfer Clearing Ledger is debited.

- **New Security: **Custodian account is debited with the Cost Transfer
  Clearing Ledger is credited.

**Negative Amounts supported: **No.

 

**De-Merger**

**Use: **To capture de-merger transaction for direct equity.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I):**

1.  Transfer Amount is used as cashflow.

2.  Old Security is fully transferred out at transfer amount and then
    transferred in at new apportioned cost.

3.  New security is transferred in at transfer amount.

**General Ledger:**\
**    Old Security:**

- Custodian account is credited with original Cost and Transfer Clearing
  Ledger is debited with the               same amount.

- Custodian account is debited with new apportioned Cost and Transfer
  Clearing Ledger is credited with the same amount.

    **New Security:**

- Custodian account is debited with the apportioned Cost and Transfer
  Clearing Ledger is credited.

**Negative Amounts supported: **No.

**Comments: **Total % Cost of Acquisition should be 100%.

 \
**Cost Basis Adjustment (CBA)**

**Use: **To increase or decrease Tax Basis without having an impact on
cash flow.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **No
  Cashflow Impact. Cost will be adjusted accordingly.

- **General Ledger: **Cost will be impacted because of the CBA
  transaction.

**Negative Amounts supported: **Yes.

 

**Return of Capital (ROC)**

**Use: **To capture the return of capital.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and
  CF-I): **\'\'Return of Capital\' amount will be used as cashflow.

- **General Ledger: **Bank Account will be debited with \'Return of
  Capital\' amount and Custodian Account will be credited.

**Negative Amounts supported:** No.

 

**Speculative**

**Use: **To enter speculative transaction entered into for any security.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **No
  Impact.

- **General Ledger: **Bank Account, Speculative income account will be
  impacted

Expenses will impact respective ledgers.

**Negative Amounts supported:**

1.  Units - No.

2.  Price - No.

3.  Taxes & Charges - Yes.

**Transfer-In**

**Use: **To enter the Transfer-In of DE.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I): **Transfer
  Amount is used as cashflow.

- **General Ledger: **Custodian account is debited with \"Net Amount\".\
  Transfer Clearing Ledger is credited with \"Net Amount\".

**Negative Amounts supported:**

1.  Price -No.

2.  Transfer Price -No.

 

**Transfer-Out**

**Use: **To enter the Transfer-Out of DE.

**Reports Impact:**

- **Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I) : **Transfer
  Amount is used as cashflow.

- **General Ledger: **Custodian account is credited with attributable
  cost. Transfer Clearing Ledger is debited.

**Negative Amounts supported: **

1.  Price - No.

2.  Transfer Price -No.

**Quick Notes**

- *For listed, system will fetch Valuation from Gateway. If not
  available, it will consider latest transaction price before report
  date.*

- *For Unlisted, system will refer manual posted Valuation in the
  system. If not available, it will consider the latest transaction
  price before report date.*

- *Dividend Payout should not be entered after full sell of a equity. It
  should be entered before or on the full sell date to correctly capture
  in performance.*

**We hope you are now familiar with DE types and its impact. Still have
questions? Reach out to AV\'s Customer Success Team.**

 
