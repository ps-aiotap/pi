The main purpose of this enhanced functionality is to accurately value
partnership investments and view such partnership holdings on regular
reports as part of entire holding or net worth as a default.

Also enhanced partnership functionality will allow user to enter the
valuation and commitment transactions through partnership module and
will be able to value their partnership investments through manual or
automatic flowdown entries.

**Disabling this functionality**

There is a checkbox which you can uncheck if you do not want to view
partnership investments by default.

**Key Enhancements**

Newly introduced transaction types:

**Commitment transaction**

Users can now enter \'Commitment\' transaction to capture the
commitments of each partner towards the partnership.

**Step 1**

Simply head to \'Transactions\' from the \'Menu,\' and then to
\'Partnership\'.

**Step 2**

Fill in necessary details like date, type, partner's entity name,
amount, etc.

*Notes: *

- *Users can enter transactions manually or via bulk upload.*

- *Negative amounts can also be added via add/edit screen or upload
  files.*

- *In case of multi-currencies, the commitment amount will be considered
  in the partnership currency.*

![](media/image1.jpeg){width="6.268055555555556in"
height="2.8618055555555557in"}

**Valuation transaction**

Users can now enter valuation transaction for each partner.

**Step 1 **\
\
In the \'Partnership\' tab, users must enter the valuation amount for
the partnership entity (e.g., partnership's net worth), and each
partner\'s values will be automatically allocated by the AV system
using *ownership* percentages as the default. Alternatively, users have
the flexibility to use *profit share* percentages as well.

**Step 2**\
\
Here too, users can add valuation transactions both manually or through
upload files.

*Valuation via manual add*

![](media/image2.jpeg){width="6.268055555555556in"
height="2.8715277777777777in"}

While uploading transactions, users need to add valuation amounts only
at the partnership level; the system will auto-allocate valuation to
partners using ownership percentage as of the given transaction date
(partner details are not required for valuation transaction). Users can
change valuation share percentage to profit share from column 'Valuation
Share %'.\
\
*Note: If 'Valuation Share %' is blank, then by default, valuation will
be calculated using the ownership percentage.* \
\
*Valuation via upload file (Mandatory fields are highlighted in red)*

![](media/image3.jpeg){width="6.268055555555556in"
height="0.9729166666666667in"}

 

*List view of valuation transaction*

![](media/image4.jpeg){width="6.268055555555556in"
height="1.2451388888888888in"}

*Edit view of valuation transaction*

![](media/image5.jpeg){width="6.268055555555556in"
height="2.8555555555555556in"}

*Additional Notes:*

- *The system\'s multi-currency support ensures partnership valuation is
  converted into a partner\'s currency (if it differs from the main
  partnership currency). List screen displays partnership and partners
  valuation in respective currencies.*

- *No vouchers will be created for commitment and valuation transactions
  as they have no accounting impact.*

**Auto Allocate Amount**

- For transaction types Contribution and Withdrawal, auto allocate check
  box will be available for user to auto allocate amounts to each
  partner based on their respective ownership or profit share
  percentage.

- Once user checks the auto allocate check box, all the respective
  partners along with held away partners will be displayed and amount
  will be auto allocated to partners using 'Ownership %' as default
  method. User can change the allocation percentage to profit share
  percentage if required.

*Note: The user can also overwrite the auto-allocated amounts of
partners and add additional partners.*

![](media/image6.jpeg){width="6.268055555555556in"
height="3.161111111111111in"}

**Position master** 

The 'Position Master' now shows partnership positions as well.

**Step 1**

Go to \'Menu,\' then \'Masters,\' and \'Positions\'.

**Step 2**\
\
The \'Account Type\' dropdown shows the new 'Asset : Partnership'
option, which loads all partnership positions by default.

**Step 3** 

Users can recategorize sector, strategy, asset class, etc. for
partnership positions like any other position.

![](media/image7.jpeg){width="6.268055555555556in"
height="1.3430555555555554in"}

![](media/image8.jpeg){width="6.268055555555556in"
height="0.8895833333333333in"}

![](media/image9.jpeg){width="6.268055555555556in"
height="3.8993055555555554in"}

**Partnership Flow Down**

This enhancement enables auto-posting of valuations across all
partnership entities for their respective partners. The system will
auto-compute the valuations from last level of partnership to the top
level. Valuation will be Total Equity (or Net Worth) amount from balance
sheet (on valuation basis).

**Step 1 **\
**\**
Check \'User Access Permission\'. Users need to have user access
permission to post valuation via Partnership Flow Down. For more
information on how to view and change user access permissions, please
read [this
article](https://support.assetvantage.com/hc/en-us/articles/360018470337-Setting-up-users-to-access-the-system-with-their-own-login-credentials-to-assign-user-level-profile-permissions-Admin-Read-View-Edit-Delete-etc-).

![](media/image10.jpeg){width="6.268055555555556in"
height="3.535416666666667in"}

**Step 2\**
\
Visit \'Partnership Flow Down\' from the \'Partnership\' page
(**Menu **\> **Transactions** \> **Partnership **\> **Partnership Flow
Down**).\
Alternatively, users can also take this path: **Menu** \> **General
Ledger (Pro)** \> **Partnership Flow Down**.

**Step 3**\
\
Users must select the date for which they want to post the
auto-valuations and click on \'Process\'. System will load all
Partnership type entities and their respective partners. System will
display the last available valuation and date. \
\
Refer to below image (Vox Investments LLP- last Valuation: 271,096.97,
Valuation Date: 31-Dec-2020)

![](media/image11.jpeg){width="6.268055555555556in"
height="4.116666666666666in"}

**\**

**Step 4** \
\
The partnership entities are displayed on the left with their equity
(net worth) values. Partners are reflected on top with respective
ownership percentages in each partnership.

![](media/image12.jpeg){width="6.268055555555556in"
height="2.9902777777777776in"}

**Step 5**\
\
Clicking on \'Post\' button will auto-post the valuations for the
respective partners. Once this step is completed, the \'Posted Value\'
column turns green. System will update Valuation transaction date under
the Valuation (below image).\
\
*Note: Users cannot select specific entities -- all partnerships and
partners will have to be processed together as there may be inter-entity
dependencies.*

![](media/image13.jpeg){width="6.268055555555556in"
height="2.9784722222222224in"}

The new valuation transaction can be viewed in the \'Details\' tab.
There is a new column added in the list view as "Entry Method", whenever
the Valuation is posted via Partnership Flow Down, system will update
the value in this column as "A" (for \'Auto\')  and shows \'M\' if a
manual transaction is entered. Users can see an explanation of these
values if they hover over each letter.\
\
Users will **not be allowed** to edit/delete auto-posted valuations
(except for Notes, Documents, and Tags) via the partnership list screen
as it will disturb computed numbers through flow down. Auto-posted
valuations can only be deleted via the Partnership Flow Down screen.

![](media/image14.jpeg){width="6.268055555555556in"
height="1.2868055555555555in"}

**Step 8**\
\
The posted valuation will be used on all reports (Wealth Register (WR),
Portfolio Performance Summary (PPS), Multi-Period Performance Report
(MPPR), Balance sheet, etc).\
\
*Note: Partnership Flow Down feature will only be available for the Pro
license version.*

 

**Impact on Reports**

Wealth Register (WR), Portfolio Performance Summary (PPS), Multi-Period
Performance Report (MPPR), Capital Flow, Capital flow by Investments,
Balance Sheet, Consolidating Balance Sheet, and Multi-period Balance
Sheet reports will show the impact of this enhanced partnership
functionality.

Filters of WR, PPS, MPPR, Capital flow, and Capital flow by Investment
have an additional check box - \'Include Partnership Position' - which
is checked by default. System will show the partnership positions in the
report based on the filters selected so user can see entire holdings and
if user wants to ignore partnership positions, then uncheck this
checkbox.\
\
*Note: This check box will not appear when the partnership method is
'With Partnership'.*

![](media/image15.jpeg){width="6.268055555555556in"
height="2.6166666666666667in"}

*Partnership positions displayed on report.*

![](media/image16.jpeg){width="6.268055555555556in"
height="1.9784722222222222in"}

Clicking the Partnership position name on the reports will open a
position pop-up, which shows details like Commitment Amount, Total
Contributions and Withdrawals, Incorporation Date, Default Share, etc.

![](media/image17.jpeg){width="6.268055555555556in"
height="2.115972222222222in"}**\**

Auto or manual posted valuations will be displayed as \'Valuations\' on
all these reports.

In case valuations are not available then system will use cost basis
(running ledger balance) as valuation. Auto or interim valuation logic
will be applicable for partnership positions where if valuation
transaction is not latest and after last available valuation transaction
there are contribution and/or withdrawal transactions then system will
add contribution amount and deduct withdrawal amount to last available
valuation transaction to compute auto valuation. 

**Points to Note**

The Partnership Flow Down process allows the user to automatically value
all partners of a partnership entity on a given day. Please be aware of
the following items for this process to work correctly:

All partnerships cash flows must follow the below guidelines:

1.  Any cashflow movement between partners must be processed through
    the **Transactions **\> **Partnerships module**.

2.  For cash transactions made through the Bank, Cash, Credit Card
    module, the "Consider For Return" field MUST be checked as "Yes"
    (except for cash transfers between accounts within the same
    partnership entity) -- see image below. If this is not done, the TWR
    of the partnership entity will not match with the partner entities.

![](media/image18.png){width="6.268055555555556in"
height="2.9743055555555555in"}

The "Value" of the partnership is calculated from the Equity (or Net
Worth) section of the Balance Sheet (i.e. Assets minus Liabilities).
There should be no ledger accounts on the partnership's Balance Sheet
which are not reflected on its Wealth Register. Ledger balance entries
which are not on the Wealth Register will cause a difference in values
and TWRs between the partnership and the partners. We recommend that
such accounts be set up as Managed Accounts so that they reflect on the
Wealth Register and performance numbers are consistent.

Since the "Value" is coming from the Balance Sheet and not the Wealth
Register, the value of the partners will not include any accrued income
on fixed income investments in the partnership. This will cause a slight
difference in the TWR and the value of the partnership that includes the
accrued income.

The automated Partnership Flow Down process works only for "Ownership
Percentage" method; it does not work for partnerships that use only
"Profit Share" as the allocation method. To use the automated flowdown,
please ensure that you establish the relationship between Partner and
Partnership entities using the Transactions \> Partnership module.

However, once this Ownership percentage relationship is established, you
can use the Profit Share method instead but only while posting
a [manual]{.underline} Valuation transaction (and not through the flow
down process) -- see image below.

With Profit share 'Valuation' allocation TWR% of Partnership and Partner
will not match.

![](media/image19.png){width="6.268055555555556in"
height="2.8569444444444443in"}

When a partner moves non pro rata basis then need to adjust the capital
balance of the partners to match the total value of the partnership.
These adjustments can be done with "Contributions" or "Withdrawals" with
a K1 Adjustment ledger account however this will result in difference
between TWR/IRR return of the partners compared to the partnership.
These adjustment cashflows need to be ignored while computing IRR/TWR
for which \'Cost Basis Adjustment\' transaction will be introduced in
future.

**We hope with the help of this article you are able to make better use
of these Partnership enhancements. Still have questions? Reach out to
AV\'s Customer Success Team.**

 

 

 
