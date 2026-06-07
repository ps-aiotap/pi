This guide will walk you through the steps to automate the often
time-consuming process of handling corporate actions such as **Interest
Payout** and **Maturity** transactions for Fixed Income instruments
(Bonds, OFCDs, CPs, and CODs). Automating transaction posting will mean
less manual work and minimizes the risk of errors for entities with
fixed income holdings. 

 

**How to find Corporate Actions in the AV System**

In the main menu, click on Transactions, then select Corporate Actions. 

 

**How to use the Filter Options for Corporate Actions:** 

- You can process Fixed Income Corporate Actions for single or multiple
  holdings simultaneously for all Entities & Groups. 

<!-- -->

- Utilize the filter options on the Corporate Actions screen to refine
  your data by Account, Holding Name, and Date Range. 

<!-- -->

- Set the TDS percentage to automatically compute TDS on Interest
  Payout. 

 

**How to run Corporate Actions for Single or Multiple Entities/Groups** 

1.  Select the entity or group for which you want to run the corporate
    actions.  

2.  The second module filter is set by default to "equity". You can
    change it to "Fixed Income" by clicking on it, as shown below. \
    \
    ![A screenshot of a
    computer](media/image1.png){width="6.268055555555556in"
    height="2.1131944444444444in"} 

The Type filter lets you select between two types of corporate actions:
Interest Payout and Maturity. You can select one or multiple options
from the dropdown list, as shown below. \
\
![A screenshot of a computer Description automatically
generated](media/image2.png){width="6.268055555555556in"
height="1.3034722222222221in"} 

**   4. Filter by Account and Holding Name:** 

- Select the required account and fixed income holding name. 

- The account filter dropdown will display a list of accounts as per the
  selected entity or group. You can choose one or multiple accounts. 

- The Holding Name filter dropdown allows you to select all holdings or
  specific ones based on the selected Account.

**5. Date Range Filters\**
You can either choose from the predefined options in the Date Range
dropdown list or manually select the dates using the "Date From" and
"Date To" fields\
\
**a. Predefined Date Range Options:** 

The Date Range filter offers several predefined options to simplify your
selection: 

- **MTD (Month to Date):** Automatically selects the start of the
  current month to today\'s date. 

<!-- -->

- **Previous Month:** Selects the entire previous month, from the first
  to the last day. 

<!-- -->

- **QTD (Quarter to Date):** Chooses the start of the current quarter to
  today\'s date. 

<!-- -->

- **Previous Quarter:** Covers the entire previous quarter, from the
  first to the last day. 

<!-- -->

- **Custom:** Allows you to manually choose any specific date range. 

**An example to understand how the Predefined Date Range Options
work:** 

When you select a predefined date range (e.g., Previous Month), the
system will automatically populate the "Date From" and "Date To" fields
with the relevant dates. For instance, if you select "Previous Month" in
September, the system will set "Date From" to August 1st and "Date
To" to August 31st. 

**b. Manual Date Selection:** 

- If none of the predefined options fit your needs, select "Custom" from
  the Date Range dropdown. You can then manually set your desired start
  and end dates using the "Date From" and "Date To" fields. 

 

**Important Note:** 

- **90-Day Restriction for All Entities/Groups:** If you are processing
  fixed income corporate actions for all entities or a group, the system
  restricts the custom date range to a maximum of 90 days. This means
  you cannot select a date range longer than 90 days for these
  categories. However, this restriction does not apply when processing
  actions for individual entities. 

    **6. Filter by Status:** 

- The Status filter defaults to \"All,\" but you can filter by
  "Processed" or "Unprocessed" interest payout and maturity
  transactions. 

<!-- -->

- The system will display data according to the selected Status filter. 

 

**    7. Set the TDS Percentage:** 

- Select the TDS value (0% or 10%) from the dropdown list. 

<!-- -->

- The TDS amount will be computed based on the selected percentage for
  the interest payout transaction type, as depicted below.  

![](media/image3.png){width="6.268055555555556in" height="2.61875in"} \
\
**Important Note:** You can overwrite the TDS value for unprocessed
Interest Payouts but ensure to click Process to save your changes. \
 

8.  **8. Configure Payee/Payor/Bank Accounts:** 

- If you select **Yes** in the "Process Payouts to Receivable
  A/Cs" filter then your interest payout transactions are posted
  to **Interest Receivable - Fixed Income** ledger. 

<!-- -->

- Select **No** to post interest payout in the default Payee/Payor/Bank
  ledger tagged to the custodian account.  

<!-- -->

- For Maturity transactions its set to default Payee/Payor/Bank ledger
  tagged to the custodian account.  

 

9.  **9. Processing Corporate Actions:** 

- Once you\'ve finished setting up all the filters and configurations,
  go ahead and process the fixed income transactions you\'ve selected by
  clicking the "Process button" on the top right corner of the screen,
  as shown below. 

![](media/image4.png){width="6.268055555555556in"
height="2.551388888888889in"} \
 

- You\'ll then see the status of each corporate action change
  to **\"Processed\".** 

 

**This automates posting interest payments and maturity transactions
based on holding positions and interest frequency.** 

 \
To enable automatic posting through the Corporate Action window
for fixed income, make sure the frequency table is set up correctly. You
can find this table in the fixed income masters.
(The picture below provides a visual example.) \
 \
 \
![](media/image5.png){width="6.268055555555556in"
height="2.8986111111111112in"} \
 \
 \
 \
 
