Customers currently use various online cash transfer and payment service
providers like bill.com to track, approve and transfer money for
expenses.  These records then need to be booked into Asset Vantage for
record keeping.

 

**Setting up & Sync Flow**

There are seven primary sync mappings that need to be made between AV
and bill.com during setup.

+----------------------------+-------------------------+-------------------------------------+
| **Asset Vantage /          | **sync**                | **  Bill.com / Mapping**            |
| Mapping**                  |                         |                                     |
+============================+=========================+=====================================+
| Entity                     | \<=                     |   Organization                      |
+----------------------------+-------------------------+-------------------------------------+
| User                       | \<=                     |   Users of bill.com (can map to     |
|                            |                         | multiple\                           |
|                            |                         |   organizations)                    |
+----------------------------+-------------------------+-------------------------------------+
| Asset : Bank               | \<=                     |   Bank Accounts under an            |
|                            |                         | Organization                        |
+----------------------------+-------------------------+-------------------------------------+
| Liability : Bank \>        | \<=                     |   All Payment transactions flow     |
| Bill.com as a \"Credit     |                         | into this\                          |
| Card\" account in AV       |                         |   Bill.com Liability : Bank account |
|                            |                         | in AV                               |
+----------------------------+-------------------------+-------------------------------------+
|                                                                                            |
|                                                                                            |
| **The following are created in either AV and synced to bill.com with a click or vice       |
| versa.**                                                                                   |
+----------------------------+-------------------------+-------------------------------------+
| Chart of Accounts :        | \<=\>                   |   Chart of Accounts : Expense       |
| Expense                    |                         |                                     |
|                            |                         |   Electricity - xx88                |
| Expense : Electricity -    |                         |                                     |
| xx88                       |                         |                                     |
+----------------------------+-------------------------+-------------------------------------+
| Chart of Accounts : Income | \<=\>                   |   Chart of Accounts : Income        |
+----------------------------+-------------------------+-------------------------------------+
| Vendor Master              | \<=\>                   |   Vendor Master                     |
|                            |                         |                                     |
| eg: Vendor : PG&E          |                         |   eg: PG&E                          |
+----------------------------+-------------------------+-------------------------------------+

 

When making payments in bill.com or setting up bill.com for a new
entity, bill.com tags each payment to a particular expense account and
tags this to a particular vendor.  It is imperative that the expense
accounts in bill.com and in Asset Vantage remain in sync. Whenever a new
expense account is added in bill.com, then it should also get added to
AV.

** **

**Operational Flow : Bill.com**

All approvals are managed through bill.com.   When payments are
completed in bill.com See below : **(Click on Review & Pay)**, these set
of completed transactions needs to be sync'd in AV's mapped account as a
corresponding transaction from the bank to the appropriate expense head
marked via a payee / payor.

![](media/image1.png){width="6.268055555555556in"
height="2.8881944444444443in"}

 

 

**Operational Flow : AV**

AV transaction sync (screenshot 1 below) will bring over all the payment
transactions and the bank to bill.com single transfer transaction and
post it (screenshot 2 below) in the mapped accounts against the already
synced Vendors and Expense accounts.

 

![](media/image2.png){width="6.268055555555556in"
height="1.7479166666666666in"}

![](media/image3.png){width="6.268055555555556in"
height="3.063888888888889in"}

 

**Cash Vs Accrual Accounting**

**Scenario 1: Cash Accounting: Where all transactions are booked in
bill.com and post payment there is a sync to AV.**

** **

**Scenario 2: Accrual Accounting: Where transactions are booked in AV to
recognize accrued income/expense.  Payment is made in bill.com on a
later date.**

While syncing with Bill.com transaction after the actual, the system
should be able to identify duplicate transactions which are already
updated in AV system. This can be identified with Bill.com ID. When such
cases are identified, the system should replace all fields with actual
Bill.com data.

**We hope you are now clear with the Bill.com concept. Still have
questions? Reach out to AV\'s Customer Success Team .**

 
