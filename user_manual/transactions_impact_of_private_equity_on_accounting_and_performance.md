**What\'s in this article?**

Discover the types of private equity transactions and their impact on
accounting and performance. 

**Finding private equity transactions **

**Step 1 **

Access your private equity transactions
from the 'Menu', 'Transactions', and then, 'Private Equity Funds'. 

![Step](media/image1.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Types of private equity transactions and their impact **

![Step](media/image2.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Commitment**

**Use:** To capture and track the Commitment of the fund.

**Impact on reports:**

- **Private equity report**: Impact on the Commitment column, and on
  compute unfunded commitment.

- **Other performance reports (Multi Period Performance Report or MPPR,
  Portfolio Performance Report or PPR, Wealth Register or WR, Capital
  flow, and Capital Flow by Investment or CF-I)**: No impact.

- **General Ledger**: No impact.

**Negative amount support:** Negative commitment amounts are supported
in case the commitment amount is reduced over time.

**Drawdown**

**Use:** To post a capital call or contribution of capital into a fund
along with any expenses included within the drawdown.

**Impact on reports:**

- **Private equity report**: The Amount Called column shows the sum of
  all Drawdowns through report date. The Total Amount of each Drawdown
  transaction is considered, including all expenses.

- **Other performance reports (MPPR, PPR, WR)**: The Total Amount is
  used as cashflow for performance computations for the internal rate of
  return (IRR) and time-weighted rate of return (TWR).

- **General Ledger**: The Custodian Account is debited with the Invested
  Amount.\
  *Note:  Expense & Fees amounts impact respective expense ledgers. *

- **Capital Flow and CF-I**: The net cashflow, i.e., the amount hitting
  the Payee / Payor / Bank account ledger, will be considered as
  Contributions in case of CF-I and the standalone account of Capital
  Flow. In case of negative drawdown, it will be considered as
  Withdrawals.

**Negative amount support: **

- Invested Amount - Yes.

- Expense & Fees - No.

**Distribution**

**Use:** To enter the distribution/withdrawal of fund along with any
gain/loss and income/expense of distribution transaction.

**Impact on reports:**

- **Private equity report**: The Amount Distributed column on the report
  shows the sum of all Distributions + Recallable Distributions; here
  too, the Total Amount is considered.

- **Other Performance Reports (MPPR, PPR, WR)**: Total Amount is used as
  Cashflow.

- **General Ledger**: The Custodian account is credited with Capital
  Distributed. Income and Expense & Fees amounts impact respective
  income/expense ledgers.

- **Capital Flow and CF-I**: The net cashflow, i.e., the amount hitting
  the Payee / Payor / Bank account ledger will be considered as
  Withdrawals for CF-I and the standalone Capital Flow account. In case
  of negative distribution, it will be considered as Contributions.

**Negative amount support: **

- Capital Distributed - Yes.

- Income -- Yes.

- Expense & Fees -- No.

*Note: Distribution should not be entered as a first transaction for the
position; Drawdown must always be entered before Distribution and can be
entered with 'zero' amount if there is no drawdown transaction amount. *

**Recallable Distribution**

**Use:** To enter distributions that are recallable. The transaction has
the same details as Distribution and can be used to track Recallable
Capital.

**Impact on reports:**

- **Private equity report**: Impact is seen on the Recallable
  Distribution column, and is also considered in the Amount Distributed
  column, where the Total Amount is considered.

- **Other Performance Reports (MPPR, PPR, WR)**: Total Amount is used as
  Cashflow.

- **General Ledger:** The Custodian account is credited with Capital
  Distributed. Income and Expense & Fees amounts impact respective
  income/expense ledgers.

- **Capital Flow and CF-I**: The net cashflow, i.e., the amount hitting
  the Payee / Payor / Bank account ledger will be considered as
  Withdrawals for CF-I and the standalone Capital Flow account. In case
  of negative Recallable Distribution, it will be considered as
  Contributions. 

**Negative amount support: **

- Capital Distributed - Yes.

- Income - Yes.

- Expense & Fees - No.

*\*

*Note: Valuation should not be entered as a first transaction for the
position. Drawdown must always be entered*\
*before Distribution or Recallable Distribution.*

**Income**

**Use:** To capture the income received separately and not as a part of
the distribution transaction.

**Impact on reports:**

- **Private equity report:** The Income column shows the sum of all
  income transactions; the Total Amount is considered).

*Note: The Income column is not selected by default and can be selected
from \'Show columns\'.*

- **Other Performance Reports (MPPR, PPR, WR)**: Total Amount is used as
  Cashflow.

- **General Ledger**: Income and Expense & Fees amounts impact
  respective income/expense ledgers.

- **Capital Flow and CF-I**: The sum of Dividends, Interest, and Other
  Income, minus TDS or Tax W/H on Distribution amounts are considered.
  For Gross Income, the sum of Dividends, Interest, and Other Income
  amounts are considered.\
  *Note: If \'Is Capital\' tag is used, then the amount will be
  considered in the Withdrawal column.\*

**\
Negative amount support:**

- Income - Yes.

- Expense & Fees (Tax) - No.

**Expense**

**Use:** To capture expense paid separately and not as a part of
drawdown/distribution transactions.

**Impact on reports:**

- **Private equity report:** The Expense column shows sum of all expense
  transactions (i.e., Total Amount is considered).  *Note: This column
  is not selected by default, but can be selected from \'Show
  columns\'.*

- **Other Performance Reports (MPPR, PPR, WR): **Total Amount is used as
  Cashflow.

- **General Ledger**: Expense & Fees amounts impact respective
  income/expense ledgers.

- **Capital Flow and CF-I**: This is the sum of Operating Expense,
  Partnership Expense, One Time / Set up fee, Management Fees, Carried
  Interest / Profit Share, Tax W/H on Distribution, TDS, Catchup /
  Hurdle Rate, and Other Charges.\
  *Note: If 'Is Capital' tag is used, then the amount will be considered
  in the Contribution column.\*

**Negative amount support: **

- Expense & Fees - No.

**Cost Basis Adjustment (CBA)**

**Use:** To increase or decrease 'Tax Basis' of the private equity fund
without having an impact on cash flow.

**Impact on reports:**

- **Private equity report**: The CBA column shows the sum of all CBA
  transactions.\
  *Note: The Expense column is not selected by default, but can be
  selected from \'Show columns\'.*

- **Other performance reports (MPPR, PPR, WR)**: No cashflow impact; the
  cost will be adjusted accordingly.

- **General Ledger**: The Cost column will be impacted.

**Negative amount support: **

- Cost Basis Adjustment (CBA) - Yes.

**Valuation**

**Use:** To capture a valuation of the fund as of a date.

**Impact on reports: **

- **Private equity report**: The 'Capital Account Value' column shows an
  impact.

- **Other performance reports (MPPR, PPR, WR)**: Valuation is used as
  End Market Value (EMV) on cashflow dates and the report generation
  date.

- **General Ledger**: No impact on accounting entries; balance sheet
  with Valuation will consider the last valuation. 

- **Capital Flow and CF-I**: Opening and Closing values are
  used; refer to the notes below for information
  on \'Automatic Valuation\'.

**Negative amount support:** Yes.

*Note: Valuation should not be entered as a first transaction for the
position.*

**Uploading Transactions:**

How to upload these transactions in bulk using and excel template:

**Step 1** 

Go to **Menu **\> **Transactions **\> **Private Equity Funds**.

**Step 2**

Click on the \"Uploads\" tab on the top right. 

**Step 3**\
\
Download the sample excel template. Quick tip: if you are entering
transactions for already created accounts or investments, you can simply
export a few existing transactions into an excel spreadsheet. That will
save you time to re-enter entity names, account names, bank account
details, etc.

![](media/image3.png){width="6.268055555555556in"
height="1.3902777777777777in"}

**Step 4**

Fill in the relevant information in the spreadsheet before uploading.
Note that a few columns have drop-downs to choose from - e.g.
Transaction Type.

*Note: For Distribution (or Recallable Distribution) transaction types,
the Return of Capital amount should be entered in the \"Amount\" column
(i.e. column K) and the Gains Upon Distribution amount should be entered
in the respective column (i.e. column L).*

![](media/image4.png){width="6.268055555555556in"
height="1.9277777777777778in"}

**Step 5**\
\
Save the excel file, and upload the file by clicking on the \"Up\"
button in the Uploads tab. These transactions then sit into a temporary
table where the system checks if these have all the necessary
information. Green color means that the transactions are ready to be
uploaded. Pink color means they need more mandatory information. Yellow
indicates duplicate transactions.

Once all transactions are Green, you can click the \"Process\" button to
process these transactions.

 

![](media/image5.png){width="6.268055555555556in"
height="2.3222222222222224in"}

 \
***Tip:***

- *If expenses are to be included in Amount Called of the private equity
  report, enter expenses within a Drawdown transaction and not through
  the Expense transaction. The Total Amount, including expenses, will be
  considered here.*

- *If Income/Expenses are part of the fund mandate and to be included in
  Amount Distributed of the private equity report, it should be entered
  within the Distribution transaction and not a separate Income/Expense
  transaction. *

- *The Total Amount, including Income/Expenses, will be considered
  in the private equity report, Standalone Income or Expense
  transactions should not be entered with a date after a position is
  closed out (i.e., Date on which Cost Basis and Valuation = 0) as these
  will give an inconsistent impact on TWR.*

- *Valuation transactions should be entered at regular intervals (end of
  month / end of quarter) for the system to compute expected un-realized
  gain/loss and capture correct performance numbers.*

- *The system captures an Automatic Valuation for those reporting dates
  where there is no specific valuation entered after
  a subsequent Contribution / Withdrawal transaction.*

- *The Automatic Valuation = Last Valuation Transaction (or Automatic
  Valuation Calculation) + Capital amount in the Contribution
  transaction -- Total amount in the Distribution transaction.
  Standalone Income / Expense transactions do not contribute to the
  change in Automatic Valuation.*

- *System will consider the position completely sold off when the ledger
  balance and valuation are zero. If either of the two are
  not zero, then it will be considered as an open position on the
  'Analytics' and 'General Ledger' reports. *

**We hope you are now familiar with the types of private equity and
their impact. Still have questions? Feel free to reach out to AV\'s
Customer Success Team. **
