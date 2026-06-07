**About the Voucher Audit report**

In a double-entry accounting system, every transaction is recorded in at
least two accounts as debit and credit. For every debit entry, there is
a corresponding equal credit entry. Irregularities in such entries
result in discrepancies between credit and debit columns, distorting
your financial picture.

The Voucher Audit report lists all period-specific vouchers and helps
you identify, analyze, and rectify accounting entries (vouchers) with
errors or deviations.

**Finding the Voucher Audit report**

**Step 1 **

Navigate to the Voucher Audit report by going to 'Menu', then 'General
Ledger', and finally, 'Voucher Audit'.

*Can't see it? Check your permission status. For more details, please
refer to the '[User access
permission](https://support.assetvantage.com/hc/en-us/articles/360018470337-Setting-up-users-to-access-the-system-with-their-own-login-credentials-to-assign-user-level-profile-permissions-Admin-Read-View-Edit-Delete-etc-)' article.*

![](media/image1.png){width="6.268055555555556in"
height="2.865972222222222in"}

**Generating the Voucher Audit report**

**Step 2**

To start, you need to select an appropriate filter dataset to be able to
generate the list of transactions with erroneous accounting entries
(represented by vouchers).

![](media/image2.png){width="6.268055555555556in"
height="2.890277777777778in"}

- **Modules:** Select one or more modules out of \'Bank\', \'Credit Card
  & Cash\', \'Mutual Funds\', \'Direct Equity\', \'Fixed Income\',
  \'Managed Accounts\', \'Unitized Funds\', \'Private Equity Funds\',
  \'Real Estate\', etc.

- **Account Type:** Choose the account type based on the module
  selected. For example, if you choose 'Direct Equity', you can only
  select account types from that module.

- **Accounts:** The accounts dropdown will list all accounts with the
  option to select/ deselect any of them.

- **From and To Date:** This report can be run for a custom period as
  defined by you.

- **Show Columns:** This dropdown allows you to select 'Transactions
  ID', 'Position ID', 'Payee/Payor/Vendor', 'Account ID', 'Tags',
  'Notes', 'Memo' and 'All Position Tags'.

Note: 'All Position Tags' can only run in grid view. 

- **Checkboxes:** Depending on the voucher issue you're trying to
  troubleshoot, you can select one or all the below checkboxes
  (explained in detail below):

  1.  Show only mismatched entries

  2.  Show with blank account number

  3.  Show with no vouchers

- 

Note: If none of the above checkboxes are selected, this report will
list all vouchers for the selected period which can be viewed in detail
(including ledger account and amount details) upon clicking the '+'
icon.

![](media/image3.png){width="6.268055555555556in"
height="2.752083333333333in"}

**1. 'Show only mismatched entries' checkbox: **

Selecting this checkbox will generate a list of those accounting
entries/vouchers where either debit or credit has not been passed,
resulting in a mismatched total for that particular transaction.

![](media/image4.png){width="6.268055555555556in"
height="2.347916666666667in"}

**2. 'Show with blank account number' checkbox: **

This option lists transactions where the account has not been tagged
properly causing voucher accounting numbers to not be displayed.

![](media/image5.png){width="6.268055555555556in"
height="2.484027777777778in"}

In the above screenshot, the account number for the account 'Short-Term
Capital Gains - Indirect' is not displayed.

Tip: All you need to do to correct 'Short-Term Capital Gains - Indirect'
from the list of transactions under 'Show with blank account number\'?
Use the \'edit\' icon to tag the correct account. 

**3. Show with no vouchers checkbox:**

This option shows transactions where no voucher was created, i.e., where
no debit or credit entries were passed, possibly because of missing
essential information like a \'sell' transaction without a
'Price/Premium' entry.

Note: Non-monetary transactions like valuation or commitment
transactions (of the private equity fund) will not have any voucher
details and won't appear with the \'Show with no voucher\' option. 

![](media/image6.png){width="6.268055555555556in"
height="2.923611111111111in"}

** Editing the transactions**

**Step 3**

Click the 'edit' icon to manually correct your transactions. Such
corrected/processed transactions will no longer appear in the list when
the report is re-run.

![](media/image7.png){width="6.268055555555556in" height="1.69375in"}

**Viewing detailed transactions**

**Step 4**

For transactions that affect multiple ledger accounts, you can view
detailed multi-distribution by clicking the '+' icon to expand the
voucher and view the detailed transaction.

![](media/image8.png){width="6.268055555555556in" height="1.69375in"}

**Exporting the Voucher Audit report**

**Step 5**

The report can also be viewed in grid view and can be exported in both
XLS and CSV export formats.

![](media/image9.png){width="6.268055555555556in"
height="1.6972222222222222in"}

**We hope you are now ready to successfully generate a Voucher audit
report. Still, have questions? Feel free to reach out to AV\'s Customer
Success Team.**
