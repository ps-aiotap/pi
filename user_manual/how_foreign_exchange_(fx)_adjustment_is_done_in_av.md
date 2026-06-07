**Introduction**

Entities having transactions in different foreign currencies may want to
translate such foreign currency transactions into their home currency to
make the data comparable or to comply with the financial reporting
requirements. Such translation may result in mismatches in the ledger
balances due to different foreign exchange (FX) rates used over time for
translation.

Consider a US entity making investment of INR 100,000 in INR securities.
In home currency, this was recorded at value USD 1,354.6 using
transaction foreign exchange rate prevalent on that date
(**Transaction FX Rate**). This investment of INR 100,000 was fully
redeemed later and recorded in home currency at USD 1,341.8 using the
transaction foreign exchange rate applicable on that date.

As visible in the below table, despite the INR 100,000 investment being
completely redeemed, when converted in home currency USD, there is a
residual balance of USD 12.8 that is visible in the ledger account. This
is owing to the different foreign exchange rates used to translate the
investment and redemption transactions.

+-----------------+-----------------+-----------------+----------------+
| **Transaction** | **Transaction   | **Exchange      | **Base         |
|                 | Currency        | Rate**          | Currency **    |
|                 | (INR)**         |                 |                |
|                 |                 |                 | **(USD)**      |
+=================+=================+=================+================+
| Investment in   | 100,000.00      | USD/INR         | 1,354.60       |
| INR             |                 | 0.013546        |                |
+-----------------+-----------------+-----------------+----------------+
| Redemption in   | -100,000.00     | USD/INR         | -1,341.80      |
| INR             |                 | 0.013418        |                |
+-----------------+-----------------+-----------------+----------------+
| Difference      | 00.00           |                 | 12.80          |
+-----------------+-----------------+-----------------+----------------+

This difference of USD 12.8 will have to be adjusted to nullify the
difference by recording this amount in a separate account (FX Adjustment
account).

Recording FX Adjustment will enable correction in the ledger balances
and makes the data accurate and comparable. FX adjustments will be done
using Average FX rate.

**Scope**

The applicability of Average FX will be limited to:

1.  All the ledger accounts with account currency different from entity
    base currency.

2.  All the ledger accounts with account currency same as entity base
    currency but having transactions in currency different than entity
    base currency. For e.g., a bank account in USD (same as entity base
    currency) has transactions of EUR security posted to it.

**Methodology used**

1.  Determination of **Entity Currency** - In AV, the currency set as
    the *Base Currency* in the entity master will be considered the
    Entity currency.

2.  **Translation of first transaction/opening balance** of the ledger
    account using Transaction FX Rate. For custodian accounts, the first
    transaction/ opening balance for every position will be translated
    using Transaction FX Rate.

3.  Computation of **Average FX Rate** using the formula:\
    Running ledger balance in Entity Base currency                     
                                                                   
    Running ledger balance in Account currency

Translation of **further transactions** will use following logic:

Opening Balance/ first transaction to be considered on Transaction FX
rate and then further logic:

- Previous running balance in local account currency is positive (debit
  side) then debit entries will use Transaction FX rate and credit
  entries will use Average FX rate.

- Previous running balance in local account currency is negative (credit
  side) then debit entries will use Average FX rate and credit entries
  will use Transaction FX rate.

- When running ledger balance becomes zero then the first transaction is
  considered with Transaction FX rate.

4\. Computation and recording of **FX Adjustment**:

- - FX Adjustment will be computed whenever Average FX Rate is used to
    translate a transaction from account currency to entity Base
    Currency.

  - Formula = (Transaction FX Rate -- Average FX Rate) \* (amount in
    account currency)

  - FX Adjustment debit/ credit logic will depend on the below matrix:

  ----------------------------------------------------------------
  **Average FX Rate used **FX             **Post to** **It is**
  for**                  Adjustment**                 
  ---------------------- ---------------- ----------- ------------
  Debit ledger entry     +ve amount       Debit       Loss

                         -ve amount       Credit      Gain

  Credit ledger entry    +ve amount       Credit      Gain

                         -ve amount       Debit       Loss
  ----------------------------------------------------------------

**Impacts**

- 1.  **General Ledger Reports --**

      - Balance Sheet, Consolidating Balance Sheet, Multi-period Balance
        Sheet and Trial Balance, Income Statement, Multi-period Income
        Statement & Consolidating Income Statement.

  2.  **Ledger Pop-up --**

      - Ledger Pop-up display the Average FX rate whenever applicable
        when report is run in entity base currency. Column FX/Rate
        display Transaction FX Rate and Average FX Rate wherever
        applicable. The debit and credit columns should reflect the
        amounts as computed using Transaction FX Rate and Average FX
        Rate wherever applicable.

  3.  **Analytics Reports --**

      - Wealth Register -- Purchase Value Column

      - Portfolio Performance -- Opening Cost Basis, Closing cost Basis
        Column

      - Private Equity (PE) Report -- Tax Basis column, Cost Basis
        Adjustment Column

  4.  **Report Book --** The reports Wealth Register, Portfolio
      Performance and PE Report, Transaction by Account report also
      reflect the updated values using the logic mentioned
      in *Methodology*.

**We hope you are now familiar with FX Adjustment working in AV. Still
have questions? Reach out to AV\'s Customer Success Team.**
