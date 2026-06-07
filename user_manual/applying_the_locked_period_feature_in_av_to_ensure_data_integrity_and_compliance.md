**Overview**

The **Locked Period **feature allows you to prevent any addition,
modification, or deletion of transactions on or before a specified date.
It helps you maintain compliance, ensure financial data accuracy, and
protect data integrity at the entity level.

**How to Access and Enable the Locked Period Feature:**

To enable the Locked Period feature, go to: \
 **Menu \> Settings \> User Access Profile \> User Access Permission** 

- Under the **Master** module, locate **Locked Period. **

<!-- -->

- You'll see two access types: 

<!-- -->

- **Edit** -- lets you set or change the lock date. 

<!-- -->

- **View** -- lets you view the locked period without making changes. 

<!-- -->

- If you\'re an Admin, access is enabled by default. For all other
  users, you'll need to manually grant permission. 

![A screenshot of a computer AI-generated content may be
incorrect.](media/image1.png){width="6.268055555555556in"
height="3.5180555555555557in"}

** **

**Setting a Locked Period:** ** **

Go to: **Menu \> Master \> Entity/Group \> Locked Period Tab** 

- In the** Entity Master Screen**. Click "Edit" on any entity to open
  the "Entity Add/Edit" pop-up. 

<!-- -->

- Navigate to the **Locked Period** tab (you'll find it at the end of
  the tab list).  

<!-- -->

- Click the **Edit **icon to access the date-picker, select your lock
  date using the calendar, and hit **Save** icon to apply it. 

![](media/image2.png){width="6.268055555555556in"
height="4.034027777777778in"}

- **Removing Lock Date:** \
  If you leave the lock date blank and click Save, it will unlock all
  transactions from inception. So, for example, if you had previously
  set a lock date and now want to completely unlock the period---and
  also track any changes made during that time---you can simply save
  without selecting a date. This will unlock all transactions from
  inception, and the Audit Trail will log any changes made. 

- You will observe that instead of a date, "unlocked since inception"
  gets updated in the list below, indicating that all transactions are
  now unlocked from inception.

![](media/image3.png){width="6.268055555555556in" height="2.31875in"}

- When saving, the system will trigger an alert to highlight any bank
  accounts with unreconciled transactions up to the lock date. The alert
  displays a list of affected bank accounts categorized under assets or
  liabilities along with their last reconciliation date.

<!-- -->

- This ensures users are aware of pending reconciliations before
  finalizing their actions, and click on "OK"to proceed ahead. A
  following password alert message will come up. And in case all the
  bank accounts are reconciled then system will not show this pop-up and
  will directly show the Password alert pop-up.\
  \
  \
  ![](media/image4.png){width="6.268055555555556in"
  height="2.8361111111111112in"}

- Users must enter their **system login password** to confirm and apply
  the lock.\
  \
  ![](media/image5.png){width="6.268055555555556in"
  height="2.8305555555555557in"}

- **Audit Trail Logging for Lock Period Changes\**
  To ensure full transparency and accountability, all changes related to
  lock period settings are logged in below table. You can track when a
  lock period was set, modified, or removed, along with the details of
  the user who made the change---visible under the **\"Locked
  By\"** column.

**System-Wide Impact of the Locked Period **

Once the lock period date is set, the system will restrict access to all
transactional data, vouchers, masters, ledgers, and other relevant
records within the locked period. This ensures that no data can be
manipulated, deleted, or altered in any way during this period. \
The following areas will be subject to lock period restrictions, and
guidance is provided on how to navigate and view the system when the
lock is applied. 

**Transaction Module Restrictions     ** 

Maintaining accurate financial records is essential, especially when it
comes to historical transactions. To protect data integrity, lock period
restrictions are applied across all investment modules, preventing any
changes to transactions dated on or before the locked date. Here\'s how
it works: 

**1. Adding New Transactions**

- You cannot add a new transaction with a date that falls on or before
  the locked period. 

<!-- -->

- If you try, the **Save** option will be disabled, and the transaction
  won\'t be recorded unless you select a date beyond the locked period.

![](media/image6.png){width="6.268055555555556in"
height="3.466666666666667in"}

**2. Editing Existing Transaction**

- Transactions posted before the lock period remain view-only.

- Users cannot edit transaction details or change the date of locked
  transactions.

- The Save option will not be available in view-only mode, ensuring no
  unintended modifications.

- Additionally, features like document uploads, multi-account editing,
  and related fields are also disabled to prevent changes.

![](media/image7.png){width="6.268055555555556in"
height="3.4569444444444444in"}\
\
**3️. Multi-Edit Restrictions**

- In the transaction list view, all transactions within the locked
  period will have their checkboxes disabled.

- This means users cannot select these transactions for bulk edits,
  ensuring historical data remains unchanged.

![](media/image8.png){width="6.268055555555556in" height="2.55in"}

**4️. Deleting Transactions**

The system requires users to select transactions before the Delete
option is enabled.

Since checkboxes for locked transactions are disabled, users cannot
delete any transaction within the locked period.

**Uploads & Contract note Restrictions**

**1. Detecting uploaded transactions in the locked period:**

- When users upload transactions via Uploads, the system automatically
  scans for any transactions that fall on or before the locked date.

- If a transaction is within the locked period, it will be flagged with
  the respective error description in red on the Transaction Processing
  Screen, similar to other error-flagged transactions.

![](media/image9.png){width="6.268055555555556in"
height="2.5791666666666666in"}

- These transactions **will not be processed or posted** into the system
  until they are corrected.

  - If you still want to post these uploaded transactions into the
    system, you can take corrective actions: 

  - Click on the **edit** icon to open the transaction edit pop-up.
    You'll notice that the transaction is currently restricted as it
    falls within the locked period (**as you can see below**).

![](media/image10.png){width="6.268055555555556in"
height="3.932638888888889in"}

- **Edit the transaction date** → Change the transaction date to a valid
  one outside the locked period. You'll then be able to save the edited
  information. Once corrected and saved, the transaction status will
  update from **error** (red) to **ready-to-process** (green).\
  \
  ![](media/image11.png){width="6.268055555555556in"
  height="3.1770833333333335in"}\
  ![](media/image12.png){width="6.268055555555556in"
  height="2.692361111111111in"}\
  \
  **2. Identifying Locked Transactions in Contract Notes**:\
  When you upload a **Contract Note (PDF) **into the AV system, it
  automatically detects any transactions that fall within the locked
  period. In the example shown, the locked date is set as
  31-Sep-2024.  Transactions that fall within the locked period will be
  highlighted in red on the Contract Note Processing Screen.

  - These transactions cannot be posted into the system. While you\'re
    in the **Contract Note** tab of Direct equity module, you won't be
    able to change the transaction date, modify any other fields, or
    save them. However, if the contract note includes other asset class
    types like **Derivatives**, the system will redirect you to
    the **Derivative module's Upload** section---where the same lock
    period restrictions will still apply. 

  - The **Status** column in the **transaction list **will update based
    on the processing state of locked transactions.\
    ![](media/image13.png){width="6.268055555555556in"
    height="2.9125in"} 

**Transaction Sync **\
Maintaining data integrity and consistency is crucial when syncing
transactions from external feeds. To ensure compliance with locked
period restrictions, the system allows syncing of transactions but
prevents their processing if they fall within the locked period\
\
**1. How the System Handles Locked Transactions in Manual Sync:**

- When you **manually sync transactions**, the system
  automatically identifies any that fall within the locked period and
  applies restrictions---preventing those transactions from being edited
  or posted into the system. You won't be able to save any changes, as
  the **Save** option will be disabled. 

**2. Auto Post Restrictions for Locked Period Transactions:**

Unlike manual sync, where you can review transactions before
posting, **Auto Post** automatically posts transactions into the system
without any user intervention. So, what happens if a transaction falls
within the locked period? 

- The transaction will not be posted. It will appear in the Transaction
  Process screen, highlighted in red.

- All previously mentioned restrictions will also apply to these
  transactions in the processing screen. 

- This ensures that locked transactions remain visible for review but
  cannot be altered or processed, preserving historical data integrity.

**Corporate Actions Restrictions**

What Happens When Equity or Fixed Income Corporate Action Falls in the
Locked Period?

- When users navigate to the Transaction List View, they will notice the
  following:

- Checkboxes for locked transactions are disabled, preventing selection
  for corporate actions.

- The Status column clearly indicates locked transactions, making it
  easy to identify them at a glance.\
  \
  **Status Indicators:**

- **\"Locked - Unprocessed\"** → Transactions that fall within the
  locked period and have not been processed.

- **\"Locked - Processed\"** → Transactions that were processed before
  the lock period was applied (e.g., dividend payouts that were recorded
  before the lock date).

![](media/image14.png){width="6.268055555555556in"
height="2.8569444444444443in"}

- If you try to process a corporate action for a locked entity,
  the **transaction cannot be selected **since the checkboxes are
  disabled. Additionally, **no modifications or updates **can be made to
  these transactions that could affect the locked information.** **

**Bank Reconciliation**

You can update the **Cleared Date** for transactions within the locked
period, but all other edits will be restricted. 

When you access **Bank Reconciliation**, you'll notice: 

- The \"Save\" icon is disabled for transactions falling on or before
  the locked period date.  

<!-- -->

- All fields except \"Cleared Date\" are view-only, preventing
  modifications i.e., you can edit and save the **Cleared Date**, but no
  changes are allowed for any other data points. 

![](media/image15.png){width="6.268055555555556in"
height="2.533333333333333in"}

**Reports & Ledgers**

- **Editing Restrictions**: Users cannot edit transactions from
  the **Transaction Tab**, **Ledger Tab**, **Voucher
  Report**, **Document Vault Screen from Analytics report position
  pop-up **and all other places on the AV system from where transaction
  can be Accessed. 

<!-- -->

- The **Save** button will be disabled for all restricted transactions,
  and an alert message will guide you accordingly.

**Account Master Restrictions**

The system enforces editing restrictions on both transactions and
account master when an entity has a lock date. You can still manage
account details within permitted limits, while ensuring that locked
financial data stays unchanged. 

**1. For Already Created Account Masters in the system:** 

- You can edit fields like **Account Name **and **Account Number **even
  if the entity has locked transactions. 

<!-- -->

- Other sensitive fields that impact locked data---such as **Opening
  Balance**, **Currency**, and **Default Lot Relief**---will remain
  editable. This ensures the accuracy of your historical records is
  preserved and prevents accidental changes that could affect your
  financial reporting.

![](media/image16.png){width="6.268055555555556in"
height="3.073611111111111in"}

**2. How to Create New Account Masters with Lock Period
Restrictions?** \
Even when an entity has a lock date, users can create new Account
Masters but cannot assign an opening balance if the selected account
type requires one. 

**If you want to manually create a new Account Master using the (+)
icon.** 

- You can create new accounts without any issue. However, if the
  selected **Account Type** requires an **Opening
  Balance** (e.g., *Asset: Bank*, *Equity: Ledger*, *Asset: Payor*),
  the **Opening Balance** field will be disabled (greyed out). For
  account types that don't require an opening balance, you can proceed
  without any restrictions. \
   

**Uploading Account Masters (File Upload Section**) : \
When you upload an Account Master file, the system performs the
following validation: 

- If an **Account Type** requires an **Opening Balance** and the entity
  has a lock date, your **Account Master** will **not** be created if
  you\'ve entered an opening balance in the upload file. 

<!-- -->

- The error will be highlighted in **red **on the processing screen. \
   

**3. Fixing Errors while uploading and adding new masters:**

- If you click **Edit** on an errored Account Master, a pop-up will open
  displaying its details. 

<!-- -->

- The **Opening Balance** field stays visible and once the value is
  removed, the **Save** button/icon will be enabled, allowing you to
  save the Account Master without an opening balance. It will then
  turn **green** in the transaction processing screen and can be posted
  into the system. 

**Partnership Transactions**

To maintain data integrity and consistency, the system enforces lock
period restrictions at both the **partnership level** and
the **individual entity level** within partnerships---ensuring that past
financial records remain unchanged. 

**Locking at the Partnership Level:** 

- If a **lock date** is set for a partnership, all transactions under
  that partnership will be locked. 

<!-- -->

- You cannot **add** or **edit** any transactions dated before the lock
  period within the partnership while the lock is active. 

<!-- -->

- This works the same way as lock period restrictions at
  the **individual entity** level. 

![](media/image17.png){width="6.268055555555556in"
height="2.686111111111111in"}

**Handling Locked Entities Within Partnerships:** 

When an individual entity within a partnership is locked: 

- Any transaction that includes that entity will also be locked within
  the **Partnership Module**. 

<!-- -->

- You can edit partnership transactions only if they don't include a
  locked entity. 

<!-- -->

- If a partnership transaction includes a locked entity, you won't be
  able to modify any part of it. 

<!-- -->

- If an entity gets locked later because of a newly set lock period,
  you won't be able to make any edits to that transaction in
  the **Partnership Module**. 

<!-- -->

- You cannot add a new transaction dated on or before the lock date if
  it includes a locked entity. 

<!-- -->

- The system will prompt you to remove the locked entity before you can
  proceed. 

- In the example below, the partner \"**James J**\" has a locked date of
  31-Dec-2023. The user is attempting to post a transaction
  dated** 1-Nov-2023**, which falls within the locked period. As a
  result, this transaction will not be allowed to be posted.

![](media/image18.png){width="6.268055555555556in"
height="2.8027777777777776in"}

**Multi-Selection & Deletion Restrictions:** 

If a **locked** entity/partner or partnership is included in a
multi-selection, deletion will be disabled---preventing you
from deleting any locked transactions.

**Partnership flow-down valuations will also be restricted:**

- If a partnership has a lock date set, or if individual partners within
  the partnership have their own lock dates, then when the user runs the
  partnership flow-down for a specific date falling within the effective
  lock period, they will be restricted from posting or deleting any
  valuations on or within the lock period.

- The partnership or entity name will be highlighted with a red border,
  displaying the lock date (as shown in the attached image below), and
  no data will be allowed to be manipulated.

![](media/image19.png){width="6.268055555555556in"
height="2.6173611111111112in"}

      
