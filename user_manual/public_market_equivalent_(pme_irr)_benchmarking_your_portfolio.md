PME Benchmarking is the performance of a public market index expressed
in terms of an internal rate of return (IRR), using the same cash flows
and timing as those of the measured portfolio over the same time period.

**Nitty-gritty of (PME IRR) Benchmarking**

PME metrics benchmark the performance of a fund, or a group of funds,
against an appropriate public market index while accounting for the
timings of the fund cash flows.

The AV system considers all capital contribution and capital withdrawal
transactions into and out of a portfolio as corresponding contributions
in to the PME at the price of the PME on the date of the contribution
cash flow.

**Treatment of income-expense transactions**

Any income pay out from the portfolio such as dividends, interest that
are not reinvested into the portfolio are ignored as corresponding
contributions into the PME.  Similarly, any expense cash flows within
the portfolio that are not part of the contributions.  Correspondingly,
any reinvestment cashflows are also marked as capital flows into the
PME.

This is because if the investor portfolio capital investments were
substituted into the PME, then the investor would not incur or
experience the expense outflow or income inflow.

 

+-------------------------+----------------------+--------------------+
|                         | **Contributions into | **Withdrawals from |
|                         | PME**                | PME**              |
+=========================+======================+====================+
| Buy, Purchase           | Yes                  | \-                 |
+-------------------------+----------------------+--------------------+
| Sell, Redemption        | \-                   | Yes                |
+-------------------------+----------------------+--------------------+
| Contribution            | Yes                  | \-                 |
+-------------------------+----------------------+--------------------+
| Distribution            | \-                   | Yes                |
+-------------------------+----------------------+--------------------+
| Dividend Payout         | \-                   | \-                 |
+-------------------------+----------------------+--------------------+
| Interest Payout         | \-                   | \-                 |
+-------------------------+----------------------+--------------------+
| Dividend Reinvestment   | Yes                  | \-                 |
+-------------------------+----------------------+--------------------+
| Cash Deposits           | Yes                  | \-                 |
+-------------------------+----------------------+--------------------+
| Cash Withdrawals        | \-                   | Yes                |
+-------------------------+----------------------+--------------------+
| Cash Deposits (CFI=Yes) | \-                   | \-                 |
| \*                      |                      |                    |
|                         |                      |                    |
| Eg: Interest income     |                      |                    |
+-------------------------+----------------------+--------------------+
| Cash Withdrawals        | \-                   | \-                 |
| (CFI=Yes) \*            |                      |                    |
|                         |                      |                    |
| Eg: Management Fees     |                      |                    |
+-------------------------+----------------------+--------------------+

\** Transactions with Consider for income "yes"*

 

To compute a portfolio performance, contribution/withdrawals, dividend
payouts, performance fees, custody fees etc all add to IRR performance.

However, choosing to invest the same capital in a PME benchmark, the
investor will not occur the same expenses or experience the same
payouts.

Hence, expense transactions marked as *Consider for Return Computation
"Yes"*, are ignored for the PME benchmark computation.

Example portfolio with a cash account :

  ---------------------------------------------------------------------------------
  **Txn**   **Date**      **Type**     **Description**      **Amount**   **PME Cash
                                                                         Flow**
  --------- ------------- ------------ -------------------- ------------ ----------
  1         01-Jan-2021   Deposit      Capital In           10,000.00    10,000

  2         15-Jan-2021   Withdrawal   Bought Security      3,000.00     (3,000)

  3         16-Jan-2021   Withdrawal   Bought Security      3,690.00     (3,690)

  4         31-Mar-2021   Withdrawal   Management Fees for  540.00       \-
                                       Q1\*                              

  5         15-Apr-2021   Deposit      Dividend received    150.00       150
                                       from Security                     

  6         30-Apr-2021   Deposit      Sold Security        4,100.00     4,100

  7         30-Jun-2021   Withdrawal   Custody Fees\*       700.00       \-
  ---------------------------------------------------------------------------------

*\* Transactions with Consider for income "yes".*

 

**We hope you are now familiar with Public Market Equivalent (PME IRR)
Benchmarking. Still have questions? Reach out to AV\'s Customer Success
Team .**
