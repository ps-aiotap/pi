Capital Flow Report is a roll forward report of the opening values,
capital contributions (inflows) and withdrawals or distributions
(outflows), security transfers, incomes, expenses, investment returns or
net gains to arrive at the closing values.

![](media/image1.png){width="6.268055555555556in"
height="1.4347222222222222in"}

 

**Important Report Definitions**

**Value on Start Date & Value on End Date**

- **Standalone Bank: **Valuation as of T-1 day of from date of
  Standalone Bank account

- **Standalone Custodian: **Valuation as of T-1 day of report from date
  of Custodian Account summation value 

- **Linked: **Valuation as of T-1 day of report from date of Custodian
  Account summation value + Linked Bank a/c value

**Contributions**

- **Standalone Bank: **Sum of all debit ledger entries of Bank account
  except transactions marked as 'Yes' for 'Consider for return
  computation' or with Tag '\_Is Not Capital'.

- **Standalone Custodian: **Sum of all investment transaction's amount
  which is hitting P/P/B account on credit side need to be considered as
  Contributions for the selected custodian account.

  - Ignore the transaction with \'\_Is Not Capital\' or \'\_Is
    Transfer\' tag

- 

- **Linked: **Sum of all bank/cash transaction's debit ledger entries
  except transactions marked as 'Yes' for 'Consider for return
  computation' or with Tag '\_Is Not Capital'.

  - Sum of all debit ledger entries which are not of a linked custodian
    account. 

- 

**Withdrawals**

- **Standalone Bank:  **Sum of all credit ledger entries of Bank account
  except transactions marked as 'Yes' for 'Consider for return
  computation' or with Tag '\_Is Not Capital'.

- **Standalone Custodian: **Sum of all investment transaction's amount
  which is hitting P/P/B account on debit side need to be considered as
  Withdrawal for the selected custodian account.

  - Ignore the transaction with \'\_Is Not Capital\' or \'\_Is
    Transfer\' tag.

- 

- **Linked:** Sum of all bank/cash transaction's credit ledger entries
  except transactions marked as 'Yes' for 'Consider for return
  computation' or with Tag '\_Is Not Capital'. + Sum of all credit
  ledger entries which are not of a linked custodian account.

**Transfers**

- **Standalone Bank: **Not Applicable

- **Standalone Custodian: **Sum of Transfer Amount for all Transfer-in /
  Transfer-out transactions in the period + any other transaction type
  tagged with \'**\_Is Transfer**\'.

  - The system will ignore TI / TO transactions related to Merger /
    De-merger transactions.

- 

- **Linked:** \'All TI/TO transactions sum of Transfer Amount (Transfer
  date to be considered) + Transactions with \'\_Is Transfer\' tag.

  - Ignore TI/TO due to merger/demerger transactions

- 

**Net Activity**

Net Activity is defined as the summation of Deposits, Withdrawals and
Transfers

**Net Income**

- **Standalone Bank: **Sum of all debit ledger entries of bank account
  which are marked as 'Yes' for 'Consider for return computation' or
  with tag '\_Is Not Capital'.

- **Standalone Custodian: **Net Income will be same logic as for linked
  accounts except bank/cash as bank is not part of Standalone Custodian
  A/C 

- **Linked:** Net amounts of Income transaction + Sum of all debit
  ledger entries of bank account which are marked as 'Yes' for 'Consider
  for return computation' or with tag '\_Is Not Capital\'

**Gross Income**

- **Standalone Bank: **Sum of all debit ledger entries of bank account
  which are marked as 'Yes' for 'Consider for return computation' or
  with tag '\_Is Not Capital'.

- **Standalone Custodian:**Gross Income will be same logic as for linked
  accounts except bank/cash as bank is not part of Standalone Custodian
  A/C

- **Linked:** Gross amounts of Income transactions + Sum of all debit
  ledger entries of bank account which are marked as 'Yes' for 'Consider
  for return computation' or with tag '\_Is Not Capital'.

**Expense**

- **Standalone Bank: **Sum of all credit ledger entries of bank account
  which are marked as 'Yes' for 'Consider for return computation' or
  with tag '\_Is Not Capital'

- **Standalone Custodian: **Expense will be same logic as for linked
  accounts except bank/cash as bank is not part of Standalone Custodian
  A/C 

- **Linked:** Amount of Expense transactions + Sum of all credit ledger
  entries of bank account which are marked as 'Yes' for 'Consider for
  return computation' or with tag '\_Is Not Capital'.

**Change in Value**

= Closing Value -- (Opening value + Net Activity + Income + Expense)

**Net Gain**

= Closing Value -- (Opening value + Net Activity)

**Change in Value**

- **Standalone Bank: **Valuation as of To date of standanlone Bank
  account

- **Standalone Custodian: **Valuation as of To date of report of
  Custodian Account summation value 

- **Linked:** Valuation as of To date of report of Custodian Account
  summation value + Linked Bank a/c value

**Reclassifying Cash Flows**

Using Tags to Re-classify Cash Flows between Capital and Income :**\**

There are three system generated tags '**\_Is Not Capital**', '**\_Is
Transfer**' and \'**\_Is Capital**\' for Capital flow report.

- Use **'\_Is Not Capital' **system tag to mark the Bank/Cash
  transactions like Management fees, Bank Charges, Bank Interest etc.
  which are Income or Expenses and not Capital transactions these will
  be considered as Income/Expense and not Deposit/Withdrawals if tag is
  used.

- Another option is to use Bank/Cash transaction's 'Consider for Return
  Computation' field, mark it as 'Yes' this will consider the
  transaction as Income/Expense and cashflow will be used to compute
  IRR/TWR. If cashflow not to be considered for TWR/IRR then use \_Is
  Not Capital tag.

- Use **'\_Is Transfer**' tag for transfer transactions which are booked
  using non-Transfer In/Out transactions to identify them as transfer
  transactions; transactions with this tag will be considered in
  'Security Transfers' column.

- Use **\'\_Is Capital\'** tag to consider Income/Expense transaction
  amount as part of \'Net Activity\' i.e. to consider them as
  Contributions/Withdrawals.

![](media/image2.png){width="6.268055555555556in" height="2.55in"}

**Finding Capital Flow Report**

Go to Menu \> Analytics \> Capital Flow

![](media/image3.png){width="6.268055555555556in"
height="2.6118055555555557in"}

**Generating Capital Flow Report**

- User need to select the appropriate filters for which they want to
  generate Capital Flow Report.

- Account\'s dropdown has all the Linked, Standalone Custodian and
  Standalone Bank accounts.

- Show Columns has all the columns from which user can select required
  columns to display on report. Net Activity and Net Gain will be
  default selected.

- 2nd Period checkbox will allow user to select 2nd report period in
  case user wants to run the report with another from and to period.

Report Output under Analytics

![](media/image4.png){width="6.268055555555556in"
height="1.8006944444444444in"}

 

Report Output in Report Book Widgets

**Horizontal View**

![](media/image5.png){width="6.268055555555556in"
height="2.689583333333333in"}

**Vertical View**

![](media/image6.png){width="5.6875in" height="4.784722222222222in"}

**Points to Note**

- [Learn more about how to Link Custodian and Bank
  Accounts.](https://support.assetvantage.com/hc/en-us/articles/4403182575377-Linking-Custodian-and-Bank-Accounts-for-Cash-Flow-Reporting) Linked
  Accounts i.e., Custodian and Bank account will be shown as single
  account on capital flow report and in report filter's dropdown values.

- For easy identification Linked accounts is reflected with \* sign in
  dropdown values.

- Check Details checkbox on filter to access debug file and to see
  further calculations.

- For accurate data run the report after **book start date**.

-  If Income is part of a Sell/ Distribution transaction then it will
  not be considered as Income in Income column.

- If Expense is part of a Buy/ Sell/ Drawdown/ Distribution transaction
  then it will not be considered as Expense in Expense column. 

**We hope you are now ready to successfully use the Capital Flow Report.
Still have questions? Reach out to AV\'s Customer Success Team .**
