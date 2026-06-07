This guide helps you manage and edit Partner and Partnership Income
Accounts in a Cost Basis Adjustment (CBA) transaction.

A CBA is not an actual cash movement. It is an accounting entry to:

- Allocate income (like profit/loss, fees, carried interest, unrealized
  gains/losses, etc)

- Adjust the capital balances between the partnership and individual
  partners

- Book non-cash income to partner accounts

So instead of affecting bank accounts, it affects Income Ledgers and
Capital Accounts.

File Path: **Menu **\> **Transactions **\> **Partnership**

**Step 1:** Default Income Account for Partner and Partnership

Select Type as Cost Basis Adjustment (CBA)
under **Partnership **\> **Transactions** module

a.  These fields are auto filled with:

    - A system-generated K-1 Income Account for the Partnership

    - A partner-specific K-1 Income -- CBA Account for the Partner

<!-- -->

b.  Use the dropdown to select any other Income Account (system or
    custom).\
    Only Income-type ledgers are shown in the dropdown.

![A screenshot of a computer AI-generated content may be
incorrect.](media/image1.png){width="6.268055555555556in"
height="2.6590277777777778in"}

 

**Step 2:** Add a CBA transaction under Partnership module

 If user checks **'Allocate Net Income'** → Only Income Accounts are
allowed.

![](media/image2.png){width="6.268055555555556in"
height="2.029861111111111in"}

![](media/image3.png){width="6.268055555555556in"
height="1.9319444444444445in"}

The Partner and Partnership ledgers auto-fill from Account Master
defaults. Use dropdowns to change them if needed (within account type
restrictions).

**Step 3:** Understanding the Accounting Logic

1.  The system posts the same logic based on selected ledgers:

    - Partnership ledger is **debited** (for income) or credited (for
      loss)

    - Partner ledger is **credited** (for income) or debited (for loss)

2.  FX translation between ledgers is applied automatically if ledgers
    are in different currencies.

This feature thereby gives users the flexibility to manage income
account mappings while maintaining accounting integrity and
auditability.
