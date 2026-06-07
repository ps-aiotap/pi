A wash sale takes place when you sell a security at a loss and then buy
the same---or a substantially identical---security within 30 days before
or after the sale date. 

**Steps with example:** 

**Information Given as per statement:** 

Transaction Details: 

  --------------------------------------------------------------------------
  Date           Type           Security       Units          Amount 
  -------------- -------------- -------------- -------------- --------------
  Jan 06, 25     Sold           Siemens        257            13,765.83 
                                Energy                        

  Jan 29, 25     Bought         Siemens        2,803.000      151,221.29 
                                Energy                        
  --------------------------------------------------------------------------

 

Gains Details: 

+-----------+--------+----------+-------+------------+------------+---------+--------+
| Security  | Units  | Purchase | Sale  | Sale       | Cost       | Wash    | Loss/  |
|           |        | Date     | Date  | Amount     | Basis      | Sale    |        |
|           |        |          |       |            |            |         | Gains  |
+===========+========+==========+=======+============+============+=========+========+
| Siemens   | 257    | Dec 06,  | Jan   | 13,765.83  | 13,765.83  | \-      | 0      |
| Energy    |        | 24       | 03,   |            |            | 342.16  |        |
|           |        |          | 25    |            |            |         |        |
+-----------+--------+----------+-------+------------+------------+---------+--------+

 

Holding Details as on Dec 31,24 

  -----------------------------------------------------------
  Security       Trade Date     Units          Cost Basis 
  -------------- -------------- -------------- --------------
  Siemens        Nov 19, 24     4,283.000      206,546.39 
  Energy                                       

                 Dec 6, 24      1,241.000      68,124.57 

  Total                         5,524.000      274,670.96 
  -----------------------------------------------------------

 

Holding Details as on Jan 31,25 

  -----------------------------------------------------------
  Security       Trade Date     Units          Cost Basis 
  -------------- -------------- -------------- --------------
  Siemens        Nov 19, 24     4,283.000      206,546.39 
  Energy                                       

                 Dec 6, 24      984.000        54,016.58 

                 Jan 29, 25     2,803.000      151,563.45 

  Total                         8,070.000      412,126.42 
  -----------------------------------------------------------

 

**Explanation:** 

Under IRS wash sale rules, a capital loss is disallowed if you
repurchase the same---or a substantially identical---security within 30
days before or after the sale date that triggered the loss. In this
case, the sale and repurchase of Siemens Energy falls within the scope
of this rule. 

**Transaction Overview:** 

- **Sale:** On **Jan 6, 2025**, 257 units of Siemens Energy were sold
  for **\$13,765.83**. 

<!-- -->

- **Repurchase:** On **Jan 29, 2025** (within 30 days of the sale date),
  2,803 units of Siemens Energy were bought for **\$151,221.29**. 

- 

**Gains & Loss Details:** 

- The **cost basis** of the **257 units sold** was **\$13,765.83**,
  which matched the **sale amount**. However, a **wash sale
  adjustment** of **--\$342.16** is listed, indicating that a **loss of
  \$342.16** would have occurred but has been **disallowed**. 

<!-- -->

- As per the wash sale rule, this loss is not recognized at the time of
  the sale because the security was repurchased within 30 days. 

<!-- -->

- Instead, the disallowed loss must be **added to the cost basis** of
  the newly purchased security (the 2,803 units bought on Jan 29,
  2025). 

- 

**System Adjustment (AV System):** 

In the AV System, this adjustment is handled as follows: 

1.  **No loss is recognized** on the **January 6 sale**---the **realized
    gain/loss** is recorded as **\$0**. 

<!-- -->

2.  A **disallowed loss adjustment** of **\$342.16** is applied
    by **adding it to the cost basis** of the **January 29 purchase**. 

- Original cost of Jan 29 purchase: **\$151,221.29** 

<!-- -->

- Adjusted cost basis in AV System: **\$151,563.45** 

This ensures accurate **cost basis tracking** for **future tax
calculations** and aligns with **IRS rules** by **deferring the
loss** to the next sale of the repurchased securities. 

 \
**Transaction Steps:** 

1.  **1) Cost Basis Adjustment (CBA) Before the Sell Transaction** 

A **Cost Basis Adjustment** must be entered against the **December
6, 2024 lot**, since this is the lot from which the **security is being
sold**, as indicated in the **Gains Details**. To book this transaction,
you can use either the **\"Wash Sale\" ledger** or the **\"Cost Basis
Adjustment\" ledger**. 

**Calculation:** 

As per the **Gains Details**, the **cost basis** for **257
units** is **\$13,765.83**. Based on that, the **cost **    **basis for
1,241 units** is calculated as follows: 

 

![A number and a number AI-generated content may be incorrect.,
Picture](media/image1.png){width="4.666666666666667in"
height="0.8958333333333334in"} 

![Picture](media/image2.png){width="6.268055555555556in"
height="3.076388888888889in"} 

**2) Add the Sell Transaction** 

Ensure that the sell transaction is booked against the **December
06, 2024** lot. If the system doesn't automatically consider this lot
based on the default relief method, use the **\"specific lot\"** option
to **manually designate** it. 

 ![Picture](media/image3.png){width="6.268055555555556in"
height="3.076388888888889in"}     

**3) Add the Buy Transaction** 

![Picture](media/image4.png){width="6.268055555555556in"
height="3.076388888888889in"} 

**4) Cost Basis Adjustment (CBA) After Buy Transaction** \
 

After the transaction, add a **Cost Basis Adjustment** using
the **holding details as of January 31, 2025** as your reference. 

Make sure that the **CBA amount after the buy** fully **offsets the
adjustment made before the sell**, so that there's **no remaining
balance** left in the **\"Wash Sale\" ledger**. 

 

![Picture](media/image5.png){width="6.268055555555556in"
height="3.076388888888889in"} 

**5) The Wealth Register and Gains Report will now show the values as
given in the statement.** 

![Picture](media/image6.png){width="6.268055555555556in"
height="3.076388888888889in"} 

 

![Picture](media/image7.png){width="6.268055555555556in"
height="3.076388888888889in"} 

 
