In partnership accounting, maintaining accurate capital balances and
ownership percentages is important. There are some specific events
taking place in partnership such as partial partner contribution or
withdrawal, new partner addition, existing partner withdrawal in such
events the allocation of realized and unrealized income needs to be done
to reflect correct allocation of gain/loss and subsequent holding %. To
handle these allocations, AV offers a solution through a Cost Basis
Adjustment (CBA) transaction, which allows seamless adjustments to the
tax basis of the partners without impacting performance or cash flows.

In AV upon setting up a partnership entity, initial contributions from
partners are captured, and a Partner Capital (Equity Account) is
established. The Ownership % in the partnership is computed based on the
capital balance of each partner account relative to the total capital
balance of all partners. This ensures an accurate representation of each
partner\'s stake in the venture.

Want to know more about Partnership module? [Click
here](https://assetvantage.freshdesk.com/support/solutions/articles/1070000063121-partnership-enhancement-valuation-auto-valuation-flowdown-positions-on-analytics).

Based on partnership accounting rules, for every subsequent non-pro-rata
movement of a partner will result in (ownership % change).  Before this
can take effect, the profit/loss and valuation need to be attributed to
existing partner share.  The Cost Basis Adjustment (CBA) transaction
allows users to distribute this increase or decrease in the tax basis of
the partnership before the non-pro-rata partner movement without
impacting performance or cash flow.

**What is?**

**Non-pro-rata movement:** Non-pro-rata movements are situations where
gain/loss cannot be divided into existing ownership ratios among
partners due to partial partner contribution or withdrawal, new partner
addition, existing partner withdrawal.

**Pro-rata partner movement:**\
All existing partners contribute and distribute in the same proportion
as their current ownership%.

**This article explains how to use this feature on the AV system and its
impact on your reports and investments.**

Let's look at a Partnership scenario!

Three (3) partners invest \$100,000 each in a Partnership as of
01-Jan-18. The ownership after the investment is as follows:

  --------------------------------------------
  **Partner**   **Cost**      **Ownership%**
  ------------- ------------- ----------------
  Mark Ruffalo  100,000       33.33%

  John Wick     100,000       33.33%

  Jia Williams  100,000       33.33%

  **Total**     **300,000**   **100.00%**
  --------------------------------------------

![](media/image1.jpeg){width="6.268055555555556in"
height="2.5708333333333333in"}

The value of the partnership increases from \$300,000 to \$450,000 (as
of 31-Dec-2018) i.e., unrealized gain/loss of \$120,000 and realized
gain/loss of \$30,000. So, the value of each partner is now \$150,000.

  ------------------------------------------------------------
  **Partner**   **Cost**      **Valuation**   **Ownership%**
  ------------- ------------- --------------- ----------------
  Mark Ruffalo  100,000       150,000         33.33%

  John Wick     100,000       150,000         33.33%

  Jia Williams  100,000       150,000         33.33%

  **Total**     **300,000**   **450,000**     **100.00%**
  ------------------------------------------------------------

![](media/image2.jpeg){width="6.268055555555556in"
height="2.4784722222222224in"}

A new Partner (Stephan Henry) wants to invest as of 02-Jan-19 with a
capital of \$100,000. In above scenario there is a gain of \$50,000 for
each existing partners (\$150,000 - \$100,000), Before adding a new
partner in this Partnership structure, the gain should be distributed
among the existing partners in their old ratio. 

To post the gain/loss in existing partners through CBA transaction
please follow the below steps:

1.  **Post Valuation** via Auto-flow down for the Partnership as of
    31-Dec-2018 (\$450,000 i.e. \$150,000 for each partner). Want to
    know more about how auto-valuation in partnership works in
    AV? [Click
    here](https://assetvantage.freshdesk.com/support/solutions/articles/1070000063121-partnership-enhancement-valuation-auto-valuation-flowdown-positions-on-analytics). 

![](media/image3.jpeg){width="6.268055555555556in"
height="3.1909722222222223in"}

2.  **Post two Cost Basis Adjustment **transactions as on 01-Jan-2019 at
    a Partnership level to distribute Realized Gain/loss of \$30,000 and
    Unrealized Gain/loss of \$120,000. The cost of every Partner will
    increase by \$50,000 (\$10,000 Realized Gain/Loss and \$40,000
    Unrealized Gain/loss). 

    - **Distribute Realized Gain/Loss:** Select "**Allocate Net
      Income"** on the transaction screen to distribute Realized
      gain/loss. It will hit the 'K-1 Income -- CBA' account for Partner
      and 'K-1 Income -- Income' account for Partnership (\$10,000 each
      partner).![](media/image4.jpeg){width="6.268055555555556in"
      height="2.9819444444444443in"}

*Note: When Auto Allocate system is checked, the system will
automatically allocate rounding difference to the first entity. Select
the radio button next to any entity if you would like to change the
rounding entity.  *  

**Accounting entry for
Partnership:**![](media/image5.jpeg){width="6.268055555555556in"
height="2.092361111111111in"}

                 

**Accounting entry for Partner (Mark
Ruffalo):**![](media/image6.jpeg){width="6.268055555555556in"
height="2.448611111111111in"}

- **Distribute Unrealized Gain/Loss: **Select** "Allocate Unrealized
  Gain/Loss" **on the transaction screen to distribute Unrealized
  Gain/Loss. It will hit a system-generated Equity ledger account
  (Unrealized MTM from
  Partnership).![](media/image7.jpeg){width="6.268055555555556in"
  height="2.9493055555555556in"}

*Note: *

- *You can also use the upload functionality to post the Cost Basis
  Adjustment (CBA) transactions.*

- *Cost Basis Adjustment (CBA) transactions will not impact Performance
  numbers i.e., IRR or TWR.*

- *The CBA realized and unrealized income/expense break up of various
  income & expense heads can be split through Journal Entry. *

**Accounting entry for
Partnership:**![](media/image8.jpeg){width="6.268055555555556in"
height="2.092361111111111in"}

**Accounting entry for Partner (Mark
Ruffalo):**![](media/image9.jpeg){width="6.268055555555556in"
height="2.386111111111111in"}

3\. Enter Contribution for Stephen Henry as of 02-Jan-2019 for \$
100,000. 

![](media/image10.jpeg){width="6.268055555555556in"
height="2.8944444444444444in"}

The Ownership % after the new Partner joining shall be as follows -

  -------------------------------------------------------------
  **Partner**   **Cost (after  **Valuation**   **Ownership%**
                CBA)**                         
  ------------- -------------- --------------- ----------------
  Mark Ruffalo  1,50,000       1,50,000        27.27%

  John Wick     1,50,000       1,50,000        27.27%

  Jia Williams  1,50,000       1,50,000        27.27%

  Stephen Henry 1,00,000       1,00,000        18.18%

  **Total**     **5,50,000**   **5,50,000**    **100.00%**
  -------------------------------------------------------------

**Impact on reports:**

The Balance sheet of the Partnership after the new partner joining shall
be as follows:

![](media/image11.jpeg){width="6.268055555555556in"
height="2.9027777777777777in"}

*Note: Cost Basis Adjustment (CBA) transactions shall not be considered
while auto computing valuations in the system.*

The Balance sheet of the Partner (Mark Ruffalo) after the new partner
joining shall be as follows:

![](media/image12.jpeg){width="6.268055555555556in"
height="2.9298611111111112in"}

**We hope this article help you post Cost Basis Adjustment transaction
for Partnership module. Still have questions? Feel free to reach out to
AV\'s Customer Success Team.**
