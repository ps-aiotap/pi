**Overview**

Our system now allows you to override the standard Feed FX rate by
entering the actual transaction rate reflected in your custodian or bank
statement.\
 This new feature, helps you align your system-recorded values with
values in custodian statements, reducing reconciliation mismatches and
improving reporting accuracy.

**Why This Feature Matters?**

The transaction rate entered by users may differ marginally from the
system-provided feed rate, often by a few decimal points. However, even
these minor variations can cumulatively lead to significant value
differences, potentially amounting to tens or thousands over time.
 These variations could cause differences between:

- System-calculated transaction amounts, and

- Actual values in custodian statements or bank advice.

**With this feature, you can now**:

- Enter the actual FX rate used for a transaction, as per your custodian
  or bank statement.

- Ensure your cost and balance reports, accurately reflect real-world
  converted amounts, eliminating discrepancies caused by standard feed
  rates.

 

**Key Benefits**

- Eliminate reconciliation mismatches between system-calculated and
  actual transaction values.

- Enhance transaction accuracy by capturing the exact FX rate applied in
  custodian or bank statements.

- Maintain flexibility with a Reset to System Rate option, allowing you
  to revert to the feed rate anytime.

 

**When Is the Custom FX Rate Applicable?**

The Custom FX Rate section becomes available only when a transaction
involves foreign exchange (Forex) --- that is, when the transactions
involve multiple currencies.

**Applicable Scenarios**:

- **For Direct Equity Transactions**:\
  When the "Account For" currency differs from the "Payee/Payor/Bank"
  currency.

- **For Bank or Cash Transactions**:\
   When the "Ledger Account" currency differs from the "Account For"
  currency.

 

**Where You'll Find It**

 

**[Step-by-Step Guide]{.underline}**

**[Step 1]{.underline} : Navigate to the Transaction Screen**

- Go to **Transactions** \> Bank/Cash or Direct Equity

- Transactions \>Add Transaction (or Edit Transaction).

 ![](media/image1.png){width="6.268055555555556in"
height="3.127083333333333in"}

*Figure 1: Direct Equity Add/Edit screen*

![](media/image2.png){width="6.268055555555556in"
height="2.970833333333333in"}

*Figure 2 : Bank/Cash Module Add/Edit screen*

 

**[Step 2:]{.underline}** **Locate the "Custom FX / Rate Calculation"
Section**

Scroll to the section titled "Custom FX / Rate Calculation".

![](media/image3.png){width="4.847222222222222in"
height="3.2291666666666665in"}

*                       Figure 3:Custom FX/Rate Calculation Screen*

[You'll see the following fields]{.underline}:

  ----------------------------------------------------------------------------------------------------
  **Field**                                            **Description**         **Field Type**
  ---------------------------------------------------- ----------------------- -----------------------
  Gross Amount ("Account for" Currency)                Fetches the amount      Read-Only
                                                       directly from           
                                                       Transaction             

  Fx/Rate (Payee/Payor/Bank: Account For)              Enter the Custom Fx     Numerical Input Type
                                                       rate here               Field

  Final Transaction Amount (Payee/Payor/Bank Currency  Auto-calculated as      Numerical Input Type
                                                       Gross Amount \* Fx Rate Field

  ![](media/image4.png){width="0.3680555555555556in"   Reset Button            On click, resets the Fx
  height="0.3819444444444444in"}                                               rate to default system
                                                                               Fx rate
  ----------------------------------------------------------------------------------------------------

 

**[Pro-tip]{.underline}**:

- If user enters FX rate, the system calculates the Final Transaction
  Amount as per Fx rate and,

- If the user enters Final Transaction Amount, the system back
  calculates the Fx rate as per Gross amount.

- For using the Custom Fx feature, value needs to be inserted in Fx/Rate
  otherwise the default system Fx/Rate is used to provide calculations.

**[Step 3]{.underline}: System Validation**

If your entered rate varies, more than 5% from the Default system rate,
the system shows an alert:

*"FX Rate varies more than 5% from Feed rate. Please correct."*

You can review and still proceed with saving if the rate is correct as
per your statement.

![](media/image5.png){width="6.268055555555556in"
height="4.143055555555556in"}

*Figure 4: Custom Fx/rate Validation Error Screen*

 

**Step 4: Save the Transaction**

Click Save once you've confirmed the FX rate and transaction amount.

The system stores both your Custom FX rate and the Default feed rate for
audit purposes.

![](media/image6.png){width="6.268055555555556in"
height="3.0083333333333333in"}*                                         
                                          Figure 5: Save Transaction*

 

**How It Appears in Ledgers and Reports**

**1. Ledger View**

To improve clarity in how FX data is displayed, two new columns have
been introduced in the **Ledger View**:

  ------------------------------------------------------------------------
  **Column**      **Description**
  --------------- --------------------------------------------------------
  **Currency      Displays the currency conversion pair used in the
  Pair**          transaction (e.g., USD: INR).

  **Transaction   Shows the FX rate applied for the transaction --- either
  FX / Rate**     the user-entered Custom FX Rate or the system-provided
                  feed rate.
  ------------------------------------------------------------------------

** **

**Visual Cue:**\
Custom FX Rates appear in **highlighted format** to clearly distinguish
them from system feed rates.

                ![](media/image7.png){width="6.268055555555556in"
height="3.120138888888889in"}\
*                                                                       
Figure 6: Ledger view of Custom Fx rates*

 

**1. AV Upload Enhancements**

You can now upload or export Custom FX Rate data in bulk through the AV
Upload Format.

**New Fields**:

- Custom FX Rate

- Final Transaction Amount

- Currency Pair

**Upload Rules**:

- These fields are non-mandatory.

- Either Custom FX Rate or Final Transaction Amount must be provided.

- If both fields are provided, the system prioritizes the Final
  Transaction Amount for processing.

- If both fields are left blank, the system automatically applies the
  default feed rate.

- When the Account Currency and Ledger Currency are the same, the
  FX-related fields are mandatorily ignored (not applicable).

 

*        *![](media/image8.png){width="6.268055555555556in"
height="3.2180555555555554in"}

*                                                                     
  Figure 7: Upload section*

**2. Excel and PDF Exports**

All new ledger columns and FX data will also appear in:

- Excel Export of Ledger View

- PDF Export of Ledger View

 

**2. Impact on Reports**

The introduction of the Custom FX Rate impacts how certain report values
are calculated and displayed:

- **Cost Column:** Reflects the Final Transaction Amount, incorporating
  the Custom FX Rate wherever it has been applied.

- **Valuation Column:** Continues to use the default feed rate to
  maintain consistency in portfolio valuation and reporting.

Here's a summary of the reports impacted by the introduction of the
Custom FX Rate feature:\
![](media/image9.png){width="6.268055555555556in"
height="2.629166666666667in"}

*Figure 8: Reports Impacted*

**3. Transparency & Audit Trail**

Every Custom Fx/Rate override is fully auditable, showing:

- **Created by**: Who made the change

- **Created Date/Time**: When it was made

- **Updated by**: Who updated the record

- **Updated Date/Time**: When it was updated

This ensures clear traceability of all adjustments.

 

**Modules Impacted for Custom Fx**

The following table outlines the modules that are impacted by the
implementation of the Custom FX feature and their current rollout
status:

  ---------------------------------------------------------
  **S.No.**   **Module Name **                 **Status**
  ----------- -------------------------------- ------------
  1           Direct Equity                    Live 

  2           Bank / Cash                      Live 

  3           Fixed Income                     Live  

  4           Managed Accounts                 Upcoming

  5           Unitized Funds                   Upcoming

  6           Private Equity Funds             Upcoming

  7           Real Estate                      Live
  ---------------------------------------------------------

 

**We hope you are now familiar with the Custom Fx feature. Still have
questions? Feel free to reach out to AV\'s Customer Success Team.**
