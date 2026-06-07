In wealth management reporting, it is important for you to reflect
income that has been earned but not yet received. One such area is the
booking of accrued interest on coupon-bearing fixed income
investments. This article outlines how Asset Vantage enables you to
account for accrued interest in the balance sheet, particularly when you
need to reflect this data point in your financials on a monthly basis. 

 

For all your coupon-bearing fixed income instruments, Asset Vantage
calculates accrued interest on a daily basis. You can run the Wealth
Register with Accrued Interest to see exactly how much interest
has accrued between any two interest payout dates. 

 

On each interest payout date, as defined in the interest schedule set up
in the security master, the accrued interest automatically resets to
zero. You will then need to pass the corresponding interest payout as a
cash flow entry using the relevant investment transaction module. 

 

If you want to book interest accrued to the balance sheet, you can do so
in the following manner: 

 

- Create an interest accrued asset ledger under
  **Menu **\>** Masters **\>** Account**, so that it appears on the
  asset side of your balance sheet.\
  \
  ![Picture 1, Picture](media/image1.png){width="6.268055555555556in"
  height="3.7618055555555556in"}

 

- Once you've created the ledger, generate the Wealth Register with
  Accrued Interest on the last date of the month to get the value of
  interest accrued for that month. 

 

Filter Selection: 

![Picture 1, Picture](media/image2.png){width="4.9375in"
height="6.680555555555555in"} 

![Picture 1, Picture](media/image3.png){width="6.268055555555556in"
height="2.165277777777778in"} 

- Pass a journal entry from **Menu **\> **Transactions **\>
  **Journal Entry**, as follows: 

<!-- -->

- Debit Accrued Interest ledger 

- Credit Interest Income ledger

                ![Picture 1,
Picture](media/image4.png){width="6.268055555555556in"
height="2.98125in"}                 

                ![Picture 1,
Picture](media/image5.png){width="6.268055555555556in"
height="2.2416666666666667in"} 

- On the date of interest payout, when you pass the entry using the
  transaction module, select the transaction type as Interest Payout. 

<!-- -->

- Once you select the transaction type, the system will automatically
  pick Interest Income as the credit ledger. You will need to change
  this and select the Accrued Interest ledger instead.  

![Picture 1, Picture](media/image6.png){width="6.268055555555556in"
height="4.039583333333334in"} 

- Once you select the correct ledger and enter the details, saving the
  transaction will automatically pass the following accounting entry: 

<!-- -->

- Debit Bank Account (where the interest cash flow has been received) 

<!-- -->

- Credit Accrued Interest ledger 

                ![Picture 1,
Picture](media/image7.png){width="6.268055555555556in"
height="2.2111111111111112in"} 

- This entry will adjust the total accrued interest amount that you
  initially booked through the journal entry, and the net entry that
  will remain will be: 

<!-- -->

- Debit Bank Account 

<!-- -->

- Credit Interest Income 

<!-- -->

- This therefore makes the Accrued Interest ledger a running account
  ledger. 

Here's how you need to pass transactions for accrued interest when you
make an additional purchase of a coupon-bearing fixed income security
during a particular month: 

- For newly purchased bonds, AV calculates accrued interest from
  the *purchase date*, not from the last interest payout date. 

<!-- -->

- When recording the purchase transaction, the purchaser must include
  the interest accrued from the last interest payout date to the
  transaction date. This amount is paid upfront by the purchaser to the
  seller, allowing the seller to receive interest for the holding
  period---from the last interest payout date to the purchase date. The
  system classifies this as interest paid from the *Interest Income
  ledger*, reflecting the concept of *dirty pricing* in bond
  transactions. 

<!-- -->

- At month-end, in the month of the new purchase, the system will show
  accrued interest from the purchase date to the end of the month. You
  must add the upfront interest paid at the time of purchase to this
  amount and pass a journal entry. This ensures that the full
  interest---from the last interest payout date to month-end---is
  reflected as accrued income. 

<!-- -->

- On the interest payout date, the current holder will receive interest
  for the entire period. Therefore, when booking the accrued interest,
  you must include both the interest paid upfront at the time of
  purchase and the accrued interest calculated by AV from the purchase
  date to month-end. 

<!-- -->

- When booking the interest payout transaction, you must ensure that the
  Accrued Interest ledger is tagged under *Income Account*, not the
  Interest Income ledger.  

<!-- -->

- From the following month-end onward, you should refer to the Wealth
  Register with Accrued Interest to derive the current accrued income
  balance. The difference between the current and previous
  month's accrued interest balances should be booked through a journal
  entry. If the accrued income shown in the Wealth Register is lower
  than the previous month, the journal entry should reflect a
  corresponding adjustment. 

 

For example - If, in the following month (January 2025), the accrued
interest as shown in the Wealth Register report is \$22,052,352, then
the journal entry for that month should be: 

Jan 2025 accrued interest - Dec 2024 accrued interest.  

\$22,052,352 - \$21,982,436.16 = \$69,915.84

![A screenshot of a computer AI-generated content may be incorrect.,
Picture](media/image8.png){width="6.268055555555556in"
height="2.2055555555555557in"} 

 

On the other hand, if the accrued interest for the following month is
lower than the previous month, the journal entry should reflect a
reduction accordingly: 

 

For example, if in February 2025 the accrued interest shown in the
Wealth Register is \$21,923,525, then the journal entry for that month
should be: 

 

Feb 2025 accrued interest minus Jan 2025 accrued interest. 

\$21,923,525 - \$22,052,352 = (\$128,827)

![A screenshot of a computer AI-generated content may be incorrect.,
Picture](media/image9.png){width="6.268055555555556in"
height="2.248611111111111in"} 

 

 

*Note: The accrued interest ledger in your balance sheet will match the
accrued interest amount in the Wealth Register on the date you pass the
journal entry at month-end. After that date, the Wealth Register will
continue to accumulate interest on a daily basis. As a result, during
the month, the amounts in the balance sheet and the Wealth Register will
not match.* 

 
