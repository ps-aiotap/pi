**About Bill.Com**

Bill.com brings smart Accounts Payables and Accounts Receivables
automation and new bill payment capabilities to your business. Harness
intelligent technology to help streamline your payments. We will get all
client's paid bills via API feed into AV system. These transactions
shall be posted as Withdrawals (bank Cash) in AV system. The workflow
for user is similar like existing feeds (PCR, Electra, etc).

To enable Bill.com for your system, get in touch with AV support.

As an initial set up, you will have to export Expense Ledgers (COA) and
Vendors created in AV system and import (upload) the same in Bill.com
system. These uploaded Ledgers and Vendors shall be used in Bill.com
system to pay the bills.

**Export Ledgers and Vendors**

**Ledger Account**

**Export existing Expense Ledger accounts (COA) from AV and upload in
Bill.com**

You can export your available expense ledger accounts from AV system in
bill.com upload format and upload the same in bill.com system. The same
can be exported from the account master screen. Below are the steps for
the same.

**Step 1 **

Go to Masters \> Accounts

![](media/image1.jpeg){width="6.268055555555556in"
height="2.386111111111111in"}

**Step 2 **

Click on CSV icon, Accounts. The system will export the list of
available ledgers in Bill.com format.

![](media/image2.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 3 **

Upload the CSV in bill.com system:  Login to your Bill.com console \>
Settings \> Import / Export \> Import
(Accounts)![](media/image3.jpeg){width="6.268055555555556in"
height="3.5256944444444445in"}

**Vendors**

**Export existing Vendors from AV and upload in Bill.com:**

You can export your available Vendors from AV system in bill.com upload
format and upload the same in bill.com system. The same can be exported
from the account master and vendor master screen (depending on how
Vendors are created). Below are the steps for the same.

**Vendors from Account master**

**Step 1 **

Go to Masters \> Accounts

![](media/image1.jpeg){width="6.268055555555556in"
height="2.386111111111111in"}

**Step 2 **

Click on CSV icon, Vendor. The system will export a list of available
Vendors in Bill.com
format.![](media/image4.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 3 **

Upload the CSV in bill.com system:  Login to your Bill.com console \>
Settings \> Import / Export \> Import (Vendors)

![](media/image5.jpeg){width="6.268055555555556in"
height="3.5256944444444445in"}

**Vendors from Vendor Master**

**Step 1 **

Go to Masters \> Vendors

![](media/image6.jpeg){width="6.268055555555556in" height="2.4375in"}

**Step 2**

Click on CSV icon. The system will export a list of available Vendors in
Bill.com format

![](media/image7.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 3**

Upload the CSV in bill.com system:  Login to your Bill.com console \>
Settings \> Import / Export \> Import (Vendors). Refer to the snip
attached point 3 of account master.

**Note :**

- Name and Number for Ledger and Vendors created will be used for
  mapping the transactions.

- It is advised that Name and Number created in Bill.com should be in
  sync with the ones available in AV.

- You should not Edit Name or Number in only Bill.com or AV system
  (should be updated in both systems). It will hamper the auto-mapping
  of ledger and Vendors while posting the transactions.

**Sync and Post Bill.com transactions**

**Sync feed**

Go to Master\> Connect Bank/Credit Card/ Investment Account\> Active
sync feeds--- Select Account type as "Unmapped", feed type as "Bill.com"
and click on the process button. You will be able to see all the newly
synced accounts on the screen.

![](media/image8.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Sync Account**

Go to Master\> Account master\> Sync Accounts (desired account to be
selected from the drop-down).

![](media/image9.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

- **Auto-create Ledgers and Vendors:**

  - ** **You can check this checkbox; if you want the system to
    auto-create ledger and Vendors if not found in the system (while
    fetching the transactions from feed).

    - **Default vendor : **Value in this field decides exactly where to
      create Vendor (Account master or Vendor master), while
      auto-creating Vendors in the system. Below will be the working for
      each record selection:

      - **Liability: Payee**---the system will create Liability: Payee
        accounts if not found in the system.

      - **Vendor**---the system will create Vendor master if not found
        in the system.

    - 

  - 

  - You can keep it unchecked; if you don't want the system to
    auto-create ledger and Vendors if not found in the system (while
    fetching the transactions from
    feed).![](media/image10.jpeg){width="6.268055555555556in"
    height="3.5256944444444445in"}

- 

**Sync Transactions**

Sync transactions (step to be performed only for historical
transactions). The system will auto-sync transactions on a daily basis
once the account is synced/mapped in Account master.

![](media/image11.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Process Transactions**

Process the transactions via the "Process" tab.

If Auto-create is enabled in the account master, the system will
auto-create the ledger and Vendors if not found in the system.

![](media/image12.jpeg){width="6.268055555555556in"
height="3.0277777777777777in"}

If Auto-create is not enabled in the account master, the system will
highlight the transactions in red if the ledger and Vendors are not
found in the system.

![](media/image13.jpeg){width="6.268055555555556in"
height="3.0277777777777777in"}

**View Auto-Created Accounts**

You can view the list of expense ledger accounts and Vendors created by
the system by clicking on the icon available after Fire icon on
Transaction sync\> Process tab

![](media/image14.jpeg){width="6.268055555555556in"
height="3.5256944444444445in"}

User can view all the auto-created Ledgers and Vendors. 

![](media/image15.jpeg){width="6.268055555555556in"
height="3.5256944444444445in"}

**Custom Account Mapping**

Custom Account Mapping is also available for Bill.com feeds. It helps
users map ledgers based on the description updated by the feed provider.
Refer to the below link for help using the Custom Account Mapping
feature : [**Custom Account
Mapping**](https://support.assetvantage.com/hc/en-us/articles/360018469977-Custom-Account-Mapping-Auto-assign-feed-transactions-to-payee-payor-vendors-and-income-or-expense-accounts%C2%A0)

**Bank Reconciliation**

You can use the bank reconciliation feature to reconcile the
transactions posted. Since we don't receive balances from feed, you will
have to manually punch in the balance as per the bank.

Need help with bank reconciliation? Click here : [**Bank
Reconciliation**](https://support.assetvantage.com/hc/en-us/articles/5758508421393-Bank-Reconciliation)

 

**FAQs**

**Can documents be sent out with my check payment?**

Yes -- BILL will include the first page of the invoice/document uploaded
to the transaction with the check.

**Can payments be made on weekends?**

Yes, a payment can be initiated at any time; however, the bank will
process the payment the next business day.

**Does BILL sync directly with AV on daily basis? **

Yes, all "Paid" transactions in BILL will sync into AV on a daily basis
These transactions will appear automatically in the "process" tab at the
next sync interval.

**Does BILL sync directly with AV for historical data?**

No, all "Paid" historical transactions in BILL will have to be manually
synced and processed by the user. 

**How often does AV pull data from BILL? **

AV pulls data from BILL 4 times a day -- at 7am, 12pm, 4pm     and 9pm
(Eastern Time). Any transaction to be captured at that interval should
be paid at least 10 minutes before the sync time.

 

**We hope you are now ready to successfully use BILL\'s feed. Still have
questions? Reach out to AV\'s Customer Success Team.**

 

 

 

 

 

 
