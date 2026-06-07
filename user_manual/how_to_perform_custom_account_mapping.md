Learn to auto assign feed transactions to vendors and income/expense
accounts. 

**For data feeds (Electra/PCR/By All)**

Custom Account Mapping feature is a powerful feature that allows you to
set a default Payee/ Payor/ Vendor, Position, and Ledger/ Income Account
based on a combination of fields including the 'Feed Security Type',
'Feed Transaction Type', \'Position\' and 'Description String'.

It will allow you to change the investment vehicle and transaction type
based on the description.

You can copy an existing mapping and then create a new for any
additional positions that need to be added.

**Mapping the Electra/PCR/By All account **

To use the 'Custom Account Mapping' feature, you'll first have to map
the Electra/PCR account.* *

**Step 1**

Go to 'Masters', then 'Accounts'.  

![](media/image1.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

 

**Step 2** 

Click the '+' to add/edit your accounts. Select your desired account,
add your details, then the desired account can be mapped
by selecting Electra or PCR account from the 'Sync Accounts' dropdown. 

![](media/image2.png){width="6.268055555555556in"
height="3.452777777777778in"}

**Custom Mapping**\
**Step 3** 

Now perform your Custom Account Mapping by clicking the fire icon (also
known as 'Feed Account Details'), available on the 'Account Master' list
view, 'Custodian Reconciliation' report screen, or the 'Transaction
Sync' process tab. 

![](media/image3.png){width="6.268055555555556in"
height="2.495833333333333in"}

**Step 4** 

Select 'Custom Account Mapping' from the filter.

![](media/image4.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 5** 

- You can map your desired \'AV Security Type\', \'AV Transaction
  Type\', 'Payee / Payor / Vendor' and 'Ledger / Income Account' based
  on a combination of 'Feed Security Type', 'Feed Transaction Type', and
  'Description String'.

- If the feed's description matches the Custom Account
  Mapping's 'Description String', AV will use the
  mapped details in 'Transaction Sync' if 'Security Type' and
  'Transaction Type' match.

 ![](media/image5.png){width="6.268055555555556in"
height="2.7354166666666666in"}

**Auto-mapping in Transaction Sync** 

AV automatically maps the tagged 'Payee / Payor / Vendor' and 'Ledger /
Income Account' in the 'Transaction Sync'. 

**Step 6** 

Go to 'Transactions', then to 'Transaction Sync'. 

![](media/image6.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 7** 

Select your 'Entity', 'Account', then click 'Start
Sync'. ![](media/image7.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 8** 

Go to the 'Process' tab. The system will auto map the tagged accounts
and transactions will be in green. You can directly process
these transactions. 

In the above image, AV auto mapped 'Feed Security Type Cash', 'Feed
Transaction Type Interest', and 'Description String Interest' (done in
Step 2).  

However, the system did not map the first transaction even
when the 'Feed Transaction Type' and 'Security Type' were
matched, because the description did not have "INTEREST" text as
provided in the Custom Account mapping (Step 2). 

*Note: The 'Transaction Edit' field shows the auto
selected ledger account, mapped in Custom Account Mapping.* 

![](media/image8.png){width="6.268055555555556in"
height="3.452777777777778in"}

*Note**:** You can map 'Payee / Payor / Vendor' and 'Ledger / Income
Account' for all Bank Cash-related transactions. You will be able to map
'Ledger / Income Account for Dividend Payout', 'Interest
Payout', and 'Dividend Reinvestment (Direct Equity, Bonds and
Debentures, Fixed Deposit, Mutual Fund)'. 'Payee / Payor / Vendor' will
be greyed out for these transactions.* 

![](media/image9.png){width="6.268055555555556in"
height="3.452777777777778in"}

![](media/image10.png){width="6.268055555555556in"
height="3.452777777777778in"}

![](media/image11.png){width="6.268055555555556in"
height="3.452777777777778in"}

![](media/image12.png){width="6.268055555555556in"
height="3.452777777777778in"}

![](media/image13.png){width="6.268055555555556in"
height="2.734722222222222in"}

**We hope you are now able to efficiently use the custom account mapping
feature. Still have questions? Feel free to reach out to AV\'s Customer
Success Team.**
