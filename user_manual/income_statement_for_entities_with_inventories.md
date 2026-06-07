 

**Income Statement for entities with Inventories**

AV now supports creation of Income (Profit & Loss) statement for
entities with assets held as inventory/for business purpose using a
template (spreadsheet) created for this purpose.

**What kind of entities can make use of this?**

Entities that have assets held as inventories, or inventories and
investments both.

**Pre-requisites to be set-up in AV**

- Separate custodian accounts are created for assets held as inventory

- Such Custodian accounts are marked as business account in the account
  master

- Purchase and Sale transactions for any such investments are routed
  through a separate payor/ bank account specifically designated for
  this purpose

- The above designated custodian and payor/bank accounts have
  \'Inventory\' mentioned in it\'s name. 

*Note: In case a single bank account is used for purchase and sale of
assets held as investment and inventory both, we recommend you create an
additional payor account and route the inventory transactions through
that payor account only. This is a necessary step to ease identification
and tracking of inventory purchase and sale through a period.*

*Tip: You may add 'Inventory' in Custodian, Payor/Bank accounts' name
for ease of identification.*

**Impact of marking custodian account as business account in the
accounts master:**

- Marking an account as business account will classify any gains made
  from sale/redemption of such assets as business income in the income
  statement instead of gains.

- This also means that such gains will not reflect in the gains report
  under analytics report since only capital gains are reported in this
  report.

**Methodology to create Income / Profit & Loss Statement considering
inventory accounting:**

1.  Define the period for which the income statement is desired to be
    generated

2.  Use the Transaction by Account (TBA) report under General Ledger
    (Pro) to generate excel exports of custodian accounts & payor/ bank
    accounts with filter combinations mentioned in the accompanying
    detailed help document.

3.  Export Income Statement for the same period

4.  Data from these exported files will have to be plainly copy pasted
    in the template prepared for this purpose. Once the pivot is
    refreshed, the final income statement worksheet will be updated with
    the latest numbers. This gives you the profit and loss statement.
