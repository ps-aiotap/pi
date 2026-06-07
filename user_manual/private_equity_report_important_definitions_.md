**What's in this article? **

This article explains everything you need to know about private
equity-related definitions as on the AV system, including important
terms like \'vintage\', \'commitment\', \'IRR\', and much more.

![First](media/image1.png){width="6.268055555555556in"
height="3.5256944444444445in"}

**How to get to the private equity report**

**Step 1 **

From your account in the system, go to 'Menu', then 'Analytics', and
finally, 'Private Equity'. 

![Step](media/image2.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Selecting filters**

**Step 2 **

Choose the appropriate filters. 

![Step](media/image3.png){width="6.268055555555556in"
height="3.2055555555555557in"}

**Generating the report **

**Step 3 **

Click 'Process' to view your private equity report.  

![Step](media/image4.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Definition of columns in the private equity report **

- **Vintage**

          This is the vintage year of the fund from the private equity
master.

- **Commitment**

          This is the sum of all commitment transactions as on the
report date in report currency.

- **Unfunded Commitment**

         This appears one of two ways:

- - When the 'Add Balance Recallable Capital in Unfunded Commitment'
    checkbox is checked on the report filter, Unfunded Commitment =
    Commitment -- Amount Called + Balance Recallable Capital.

  - When the checkbox is unchecked, Unfunded Commitment = Commitment --
    Amount Called.

- 

<!-- -->

- **Updated Date**

         This is the date of the most recent transaction before the
report date.

- **Amount Called**

        This is the sum of all Drawdowns entered till report date in
report currency.\
        'Total Amount' (including all charges) will be considered for
computation.

- **Called %**

         This is the Amount Called/Commitment.

- **Amount Distributed**

         This is the sum of all Distributions/Recallable Distributions
entered till report date in report currency.\
        'Total Amount' (including Income and Expenses) will be
considered for computation.

- **Distributed %**

         This is the Amount Distributed/Commitment.

- **Recallable Distributions**

         This is the sum of all positive Recallable Distributions
entered till report date in report currency.

         'Total Amount' (including Income and Expenses) will be
considered for computation.

- **Balance Recallable Capital**

       This is the sum of all (positive and negative) Recallable
Distributions entered till report date in                  report
currency.

  "Total Amount" (including Income and Expenses) will be considered for
computation.

- **Cost Basis**

        This refers to the running ledger balance without considering
Cost Basis Adjustment (CBA)                      transactions in report
currency. This includes the sum of all Drawdown transactions minus the
sum of all 'Return of Capital' amounts under the Distribution and
Recallable Distribution transactions.

- **Cost Basis Adjustment**

         This is the sum of all CBA transactions entered till the report
date in report currency. Cost Basis Adjustment (CBA) allows you to
increase or decrease the tax basis of the security.

- **Tax Basis**

         This is the running ledger balance as on report date (which
will include CBA transactions) in report                 currency.

- **Invested Cost**

         This is calculated as the Amount Called -- Balance Recallable
Capital + Expense (values are taken                    from the report
generated as of date).

- **Valuation**

         This is the valuation as on the report date. If this is not
available, and Drawdowns, Distributions, and             Recallable
Distributions transactions are entered after the previous valuation
transaction and                         before report date, then
valuation is to be computed using Auto-Val logic.

Note:

- If no valuation is entered, AV shows a running ledger balance, i.e.,
  Tax basis as Valuation.

- In case of multi-currency, values are converted using the foreign
  exchange (FX) rate as on report date.

- If the valuation is stale, AV will show the valuation date under the
  amount in subscript.

<!-- -->

- **Valuation %**

         This refers to the Valuation/Commitment.

- **(Val + Dist.) as % of Called**

         This expands to (Valuation + Amount Distributed) / Amount
Called.

- **Income**

        This is the sum of all income transactions entered till report
date in report currency.

        'Total Amount' will be considered for computation. 

- **Expense**

         This is the sum of all expense transactions entered till report
date in report currency.

         'Total Amount' will be considered for computation.

- **IRR**

          It is the Internal Rate of Return computed using dates and
cashflows of the investment.

          IRR is used to calculate returns on investments where there
are multiple transactions taking place                   on different
dates.

Tip:  This follows the same logic as IRR on the Wealth Register report.
Learn more with the [Wealth Register
Report](https://support.assetvantage.com/hc/en-us/articles/360018629618-Wealth-Register-Report-wealth-across-entities-holdings-asset-classes-with-partnership-look-through)* article.*

- **DV/PI**

         This is the Amount Distributed/Amount Called.

- **TV/PI**

         This is calculated as (Amount Distributed + Valuation) / Amount
Called

Note:  In case of multi-currency in the Commitment, Amount Called,
Amount Distributed, Recallable Distributions, Balance Recallable
Capital, Cost Basis, Cost Basis Adjustment, Tax Basis, Income, and
Expense columns, values are converted using the FX rate as of
transaction dates.

**We hope you are now familiar with the important terminologies of the
private equity report. Still have questions? Feel free to reach out to
AV\'s Customer Success Team.**

 

 
