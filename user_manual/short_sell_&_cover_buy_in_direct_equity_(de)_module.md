This guide will walk you through how to use the **Short
Sell** and **Cover Buy** transaction types in the Direct Equity module.
These features will allow you to record short selling activities and
track their impact seamlessly across your holdings, accounts, and
reports.

Short selling is a trading strategy where you sell borrowed securities,
expecting their price to drop, so you can buy them back later at a lower
price (Cover Buy).

**1. Where to Find the New Transaction Types**

When you navigate to the **Direct Equity module \> Transactions list**,
you will now notice:

- **New values under the \"Transaction Type\" column:** Short Sell and
  Cover Buy.

- You can search transactions by selecting these types in
  the **Transaction Type filter**.

![](media/image1.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**2. Adding a Short Sell or Cover Buy Transaction**

To add a new Short Sell or Cover Buy transaction, follow these steps:

**2.1 Accessing the Add Transaction Pop-Up**

1.  Go to the **Direct Equity module**.

2.  Click on the **\"+\" icon** to add a new transaction.

3.  The **Direct Equity Transaction -- Add** pop-up will appear.

**2.2 Selecting Position Type**

- In the **Position Type **field, you will now see two options:

  1.  Long

  2.  Short

- Select **Short** if you are entering a short selling-related
  transaction.

* **Note:***

- *If you select Short, the **Security Listing Type** will be defaulted
  to Listed and Unlisted will be disabled.*

- *If you select Long, the Security Listing Type dropdown will work as
  before.*

![](media/image2.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**2.3 Transaction Type Field**

Depending on the Position Type:

- If **Short** is selected, the **Transaction Type **dropdown will
  display:

  - Short Sell

  - Cover Buy

  - Dividend Payout (for short positions)

  - Expense

- If **Long** is selected, the existing transaction types remain
  unchanged.

![](media/image3.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**2.4 Entering Transaction Details**

Once you select the Position Type and Transaction Type, proceed to fill
in the details (Security Name, Units, Price, etc.) as usual.

 **Important Validations:**

- You **cannot enter a Cover Buy before a Short Sell** is recorded.

- Cover Buy quantity **cannot exceed the Short Sell quantity**.

- Attempting either will trigger a validation message.

**3. Margin Account & Payee/Payor Handling**

When booking a Short Sell, the system will automatically assign
a **Margin Account (MA)** to handle the liability:

- This account is auto-created when you perform your first Short Sell.

- It appears under **Liabilities \> Bank** in your Chart of Accounts.

- All Short Sell transactions for that position will lock to this
  account as the default **Payee/Payor Bank (PPB)**.

 **For Cover Buy:**

- The PPB dropdown will only show **Asset Bank Accounts**, excluding the
  Margin Account.\
  \
  \
  ![](media/image4.jpeg){width="6.263888888888889in"
  height="3.0694444444444446in"}

**4. Impact on Holdings and Reports**

**Wealth Register & Analytics**

- Short Sell positions will now display as **negative holdings**.

- The **Purchase Value** will be shown as the net amount at which the
  units were shorted.

![](media/image5.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

 

**5. Partial & Full Cover Buys**

- You can close your short position partially or fully by booking Cover
  Buy transactions.

- The system will update the Margin Account and holdings accordingly.

 **Partial Cover Buy:**

- Remaining shorted quantity and Margin Account balances will adjust
  correctly until the position is fully covered.

**6. Other Enhancements**

- **New Transaction Types:**

  - **Dividend Payout (Short):** Used when dividends need to be paid out
    during a short position.

  - **Expense:** To record fees and costs associated with short selling.

- **Upload File Changes:**

  - New column **Position Type (Long/Short)** has been introduced.

  - Transaction Type column now accepts Short Sell, Cover Buy, Expense.

![](media/image6.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**7. Deleting or Editing Transactions**

- You **cannot delete a Short Sell** if it is linked to any Cover Buy
  transactions.

- You must delete associated Cover Buys first.

- Editing Short Sell quantity or date will trigger checks to ensure
  consistency.

**8. Taxation & Reports**

- All gains/losses from Short Sell and Cover Buy are treated
  as **Short-Term Capital Gains (STCG)** regardless of holding period.

- **Schedule D Report:** Short Sell transactions will automatically
  reflect in this tax report, categorized as short-term.
