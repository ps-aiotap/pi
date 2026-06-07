This guide walks you through how to book **Return of Capital
(ROC)** transactions for bonds in Asset Vantage, both manually and via
automated Corporate Actions. ROC transactions are essential for properly
accounting for principal amortization in bonds, and ensuring accurate
cost basis and face value tracking over time.

Return of Capital is used when a bond gradually repays part of its
principal during its lifetime. While the quantity of the bond remains
unchanged, the **purchase cost** and **face value** reduce
proportionally. This has downstream effects on **interest
payout**, **accrued interest**, and other financial analytics---making
timely recording of ROC crucial for accurate reporting.

**1. Booking ROC Manually in the AV System**

You can manually record ROC transactions for any bond through the
Transactions module. Follow the steps below:

**Step 1: Navigate to Add a New Transaction**

- Go to **Transactions \> Fixed Income \> Bonds/Debentures**

- Click on the **\"+\" Add** button to record a new transaction.

**Step 2: Select Transaction Type**

- From the dropdown, choose the **Transaction Type: Return of Capital
  (ROC)**\
  This new type functions similarly to Amortization and includes the
  same key fields:

  - Entity

  - Account

  - Security Name

  - Transaction Date

  - Payee/Payor

  - Amortization Amount (editable)

  - Amortization on Face Value (editable)

![](media/image1.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**Step 3: Enter ROC Details**

- You may enter either:

  - **Amortization Amount** (in negative)I

  - OR **Amortization on Face Value (%)**

- The system auto-calculates:

  - **Adjusted Cost**

  - **Adjusted Face Value**

 **Note:**

- Use a negative sign for amortization to reduce cost and face value.

- Positive values will increase them (though uncommon).

- The \"Open Lot Date\" shows the most recent purchase date for that
  holding.

![](media/image2.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**Step 4: Save and View Voucher**

After saving the transaction, the system generates the appropriate
accounting voucher:

- Debit: **Bank Account** (amount received as ROC)

- Credit: **Custodian Account** (reduction in value of holding)

 

**3. Booking ROC via Corporate Actions (Auto Mode)**

For recurring ROC events (common with amortizing bonds), Asset Vantage
allows you to automate the process through the **Bond Master** setup.
This significantly reduces manual work and ensures consistency.

 

**Step 1: Add ROC Frequency in Bond Master**

Navigate to:\
**Menu \> Masters \> Fixed Income\
\
 **Search for the desired fixed income security.

- If the security is **listed**, the frequency table is automatically
  populated from market feeds and cannot be edited.

- If the security is **unlisted** (i.e., created manually in the AV
  system), you can set up your own ROC frequency table.

Click the **Edit** icon for the selected unlisted security.

Scroll down to the section below the existing **Interest Payout
Frequency** table. You will now see a new table titled:\
**"Return of Capital (ROC) Payout Frequency."**

Enter the ROC frequency details as required to automate ROC postings for
the selected security.

![](media/image3.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**Step 2: Define ROC Schedule**

Click on **\"+\" Add** to create a payout schedule. You can configure:

- **Month / Day / Year**

- **Amount**

- **OR Percentage (%)** of face value

 **Auto-Calculation Logic:**

- If you enter **Amount**, system calculates Percentage.

- If you enter **Percentage**, system calculates Amount.

![](media/image4.jpeg){width="6.263888888888889in"
height="3.0694444444444446in"}

**Step 3: ROC Auto-Posting via Corporate Actions**

Once the schedule is saved in the Bond Master:

- The system will auto-generate **Return of Capital** transactions as
  per your frequency table(monthly, quarterly, yearly, etc.).

- These entries will be ready to **process under Transactions \>
  Corporate Actions \> Fixed Income**.

 **Just like Interest Payouts**, you can apply filters by:

- Entity

- Holding

- Date Range

- Transaction Type = ROC

![](media/image5.png){width="6.263888888888889in" height="2.8125in"}

**4. ROC via Upload**

If you prefer bulk uploads, ROC can be handled via the existing Fixed
Income upload template.

**Key Points:**

- No change in template structure.

- In the **Transaction Type** column, select \"Return of Capital
  (ROC)\".

- Use **Net Amount** column to enter the amortization amount.

- ROC transactions will reflect the calculated face value adjustment
  based on this amount.

- Historic-dated ROC transactions will be flagged as **Out-of-Turn**,
  similar to other FI types.

 
