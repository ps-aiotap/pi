Path**:** **Menu **\> **Transactions **\> **Fixed Income**.

**Type of transactions and impact**

**Purchase**

**Use : **To enter the Purchase of Bond along with any expenses/taxes
paid.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Net Amount (dirty) is used as Cashflow.

- **General Ledger Impact : **Custodian account is debited with
  \"Amount\". \"Expenses & taxes\" amounts impact respective expense
  ledgers. \"Accrued Interest\" paid during purchase is debited. Bank is
  credited with total cash outflow.

**Negative Amount Support :**

- Quantity - No.

- Clean Price - No.

- Accrued interest - No.

- Taxes and Charges - Yes.

 

**Sell**

**Use : **To enter the Sell of Bond along with any gain/loss and
income/expense incurred.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Net Amount (dirty) is used as Cashflow.

- **General Ledger Impact : **Custodian account is credited with Cost.
  \"Expenses & taxes\" amounts impact respective expense ledgers.
  Gain/loss will be booked. \"Accrued Interest\" received during Sell is
  recognized as \"Income\". Bank is credited with total cash inflow.

**Negative Amount Support :**

- Quantity - No.

- Clean Price - No.

- Accrued interest - No.

- Taxes and Charges - Yes.

**Interest Payout**

**Use : **To enter Coupon payments received.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Gross Amount is used as Cashflow.

- **General Ledger Impact : **\"Income\", \"TDS\" and \"Service Tax\"
  amounts impact respective income/expense ledgers. 

**Negative Amount Support :** Yes.

 

**Transfer-In**

**Use : **To enter transfer-In of Bond along with accrued interest.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Transfer Amount + Accrued interest is used as Cashflow. For
  Performance computation, Transfer Date is considered.

- **General Ledger Impact : **Custodian account is debited with \"Net
  Amount\". \"Accrued Interest\" is debited. Transfer Clearing account
  is credited.

**Negative Amount Support :** No.

 

**Transfer-Out**

**Use : **To enter transfer-Out of Bond holding along with accrued
interest.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Transfer Amount + Accrued interest is used as Cashflow.

- **General Ledger Impact :** Custodian account is credited with Cost.
  \"Accrued Interest\" is credited. Transfer clearing account is
  credited.

**Negative Amount Support :** No.

 

**Amortization**

**Use : **To increase/decrease Cost basis Or To increase/decrease
Quantity held. 

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I) :** No
  Cashflow Impact. Cost will be adjusted accordingly.

- **General Ledger Impact :** Custodian is debited (to increase cost),
  credited (to decrease cost). Income/ expense ledger impacted
  accordingly.

**Negative Amount Support :** Yes.

 

**Valuation **

**Use : **To capture a valuation of the bond as of date.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Used as End Market Value (EMV) on cashflow dates and report
  generation date.

- **General Ledger Impact : **No Impact on accounting entries; Balance
  sheet with Valuation will consider Last Valuation.

**Negative Amount Support :** No.

*Want to enter manual valuation for listed bonds? Click here to know
more : [Bond Manual
Valuation](https://support.assetvantage.com/hc/en-us/articles/8613168827677).*

**Maturity**

**Use : **To enter the Maturity of Bond along with any expenses/taxes
paid.

**Reports Impact : **

- **Other Performance Reports (MPPR, PPR, WR, Cap. flow and CF-I)
  :** Net Amount is used as Cashflow.

- **General Ledger Impact : **Bank is debited. Custodian is credited.
  Gain/loss will be booked. Expenses & fees will impact respective
  ledgers.

**Negative Amount Support :**

- Taxes & Charges - Yes.

- Others - No.

**Quick Notes**

- *For listed, the system will fetch Valuation from Gateway. If not
  available, it will consider the latest transaction price before the
  report date.*

- *For Unlisted, the system will refer to the manual posted Valuation in
  the system. If not available, it will consider the latest transaction
  price before report date.*

- *For Performance computation (IRR & TWR), the system will consider all
  the cashflows with accrued income.*

- *Partial Maturity should not be entered for a bond.*

- *Interest Payout should not be entered after the full sell of a bond.
  It should be entered before or on the full sell date to correctly
  capture performance.*

**We hope you are now familiar with Bond types and its impact. Still
have questions? Reach out to AV\'s Customer Success Team.**

 

 

 

 

 

 

 
