Bank Reconciliation feature helps you to reconcile the transactions,
ledger entries and ending balances in AV with your bank statements. For
accounts that have a direct electronic feed, you can also reconcile your
AV balances to the live account balance using feed balances.

**User Access Profile**

**Go to Menu \> Settings \> User Access Profile**

- Add permission will allow you to mark the transaction/ledger entry as
  cleared or reconciled.

- Edit permission will allow you to mark the reconciled transaction as
  unreconciled, user with edit permission only can mark the reconciled
  transaction as unreconciled.

- View permission will allow you to view the menu and bank
  reconciliation screen.

- Export permission will allow you to export the bank reconciliation
  report in excel format.

![](media/image1.jpeg){width="6.268055555555556in"
height="1.7652777777777777in"}

*Want to know more about User Access Permission? Click here [User access
permission
article](https://support.assetvantage.com/hc/en-us/articles/360018470337-Setting-up-users-to-access-the-system-with-their-own-login-credentials-to-assign-user-level-profile-permissions-Admin-Read-View-Edit-Delete-etc-).*

**Finding Bank Reconciliation**

**Go to Menu \> Transactions \> Bank Reconciliation**

![](media/image2.jpeg){width="6.268055555555556in"
height="3.267361111111111in"}

 

**Knowing Bank Reconciliation **

- Select Bank account in order to see reconciled/ unreconciled
  transactions. The default date will be month-end date of last
  reconciled transaction which you can change to any date (if no
  transactions reconciled previously then current system date will be
  displayed).

- Fire icon next to Bank account name will display Feed Account details,
  only for accounts which have a feed mapped to them.

- 'Get from feed' button will be displayed only when a feed is mapped to
  the account and the cash account balances from the feed as of selected
  date will be fetched when clicked on it.

- For non-linked accounts, you can enter 'Balance as per Bank' manually.

- You can mark the transaction as Reconciled by selecting the checkbox,
  updating cleared date, and clicking on "Save" button. (By default,
  cleared date is same as transaction date, which the you can override
  to any specific date).

- Multiple transactions can be selected to mark them as reconciled.

- Once transactions are marked as reconciled, they will be highlighted
  in green and will remain collapsed under bank account name. All
  reconciled transactions can be viewed anytime by clicking on + icon
  before account name.

- At the bottom of the screen, the system will show the sum of
  reconciled transactions, reconciled ending balance, sum of
  unreconciled transactions, ending balances as per AV's running ledger
  balance and difference if any after considering reconciled,
  unreconciled and balance as per bank. Please note that the amount in
  \"Total Reconciled Transactions" changes dynamically as you select
  respective transactions to be saved as reconciled.

- You can with edit permission mark the reconciled/cleared transaction
  as unreconciled by clicking on checkbox and clear date will be removed
  automatically by system. The transaction will be moved from reconciled
  block to unreconciled block and balances will be updated on click of
  Save button.

- If you edit any reconciled transaction and updates any amount or
  account related fields, then system will give a soft validation
  message and you will still be able to save the transaction.
  Transaction will be marked as Un- reconciled if values in any
  above-mentioned fields are updated.

![](media/image3.jpeg){width="6.268055555555556in"
height="3.2159722222222222in"}

**Exporting Bank Reconciliation**

- After saving all the changes, you can export Bank reconciliation
  report using Excel, PDF Export icon on the top right to see the
  summary, reconciled transactions in the last session and remaining
  unreconciled transactions till selected.

- Reconciled transactions in the export will be of last saved session.

- To get correct details on export make sure 'Balance as per Bank' is
  not empty for system to compute other numbers.

![](media/image4.jpeg){width="6.268055555555556in"
height="3.5256944444444445in"}

**Show/Hide reconciled transaction in export:**

There is a new checkbox added on bank recon screen as "Export reconciled
transactions" that will allow you to include/exclude the reconciled
transactions of the last session in the export.

![](media/image5.jpeg){width="6.268055555555556in"
height="3.154166666666667in"}

If checked and exported, the system shall include transactions
reconciled by you in the last session.

![](media/image6.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

If unchecked and exported, the system shall not include transactions
reconciled by you in the last session.

![](media/image7.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Reconciled status in Bank cash**

All the transactions reconciled via bank reconciliation will have the
status "R : Reconciled" in the bank cash transaction edit and list
screen.

![](media/image8.jpeg){width="6.268055555555556in"
height="3.017361111111111in"}

If you mark a transaction status as "R : Reconciled" via bank cash
transaction screen, the transaction will automatically be marked as
reconciled in bank reconciliation.

Marking transaction status as "R : Reconciled" on Bank cash transaction
screen

![](media/image9.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

The marked transaction gets automatically reconciled  on the Bank
Reconciliation screen.

![](media/image10.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

The "R : Reconciled" status is also available in the upload of bank cash
transaction.

**Notes:**

- By default, cleared date will be same as transaction.

- You cannot mark cleared date prior to transaction date.

- Multiple transactions can be marked as reconciled/ unreconciled

- You can edit balances even if it is fetched by Feeds.

- If you mark a Check transaction as 'Cleared' through check print
  functionality, you will have to still reconcile the transaction via
  bank reconciliation.

- Click on ledger names will open the ledger pop-ups and you can edit
  the transactions by clicking on edit icon and view vouchers using
  voucher icon.

- For Asset bank and liability bank ledger pop-up, a new column is added
  as "Reconciled". All the reconciled transactions will have value as
  "Yes".

**We hope with the help of this article you are more equipped to do Bank
Reconciliation. Still have questions? Reach out to AV\'s Customer
Success Team.**
