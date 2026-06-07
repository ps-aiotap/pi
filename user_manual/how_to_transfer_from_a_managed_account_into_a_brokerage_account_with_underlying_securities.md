Are you tracking a brokerage account or a managed account in AV as a
single line item (without the underlying securities)?

And now want to track it in AV as a detailed brokerage account with the
underlying securities?

We have got some best practices to follow. Kindly follow the below
steps:

**Let's take an example!**

You have currently entered a Managed account in AV. 

Considering the cost basis for this account is \$1,000,000 and the
market value is \$1,200,000. 

![Snip](media/image1.jpeg){width="6.268055555555556in"
height="1.8118055555555554in"}

That will show an Unrealized Gain of \$200,000 for that account.

![Snip](media/image2.jpeg){width="6.268055555555556in"
height="2.113888888888889in"}

Want to more about Managed Account? Refer to [Managed
Account](https://support.assetvantage.com/hc/en-us/articles/7538504896541).

**Step to Enter Withdrawal Transaction in Managed Account.**

**Step 1**

- Enter a withdrawal transaction in the managed account as of a specific
  date.\
  *Tip: You could use month ends as a best practice.*

- In the withdrawal transaction, enter \$1,000,000 as Return of Capital
  and \$200,000 as Gains upon Withdrawal. This will result in zeroing
  out the managed account.

![Snip](media/image3.jpeg){width="6.268055555555556in"
height="3.311111111111111in"}

- Since this is not an actual cash withdrawal, please use a dummy
  account for the second side of the journal entry -- e.g. Transfer
  Clearing account.

- This will also result in the following journal entry:

![Snip](media/image4.jpeg){width="6.268055555555556in"
height="2.9868055555555557in"}

- However, this entry creates an incorrect Realized Gain which needs to
  be zeroed out -- we will explain this in the following steps.

**Create a new Custodian Account**

**Step 2**

- In the account masters, create a new Asset: Custodian (and Asset:
  Bank) account which will hold the underlying securities.\
  *Tip**:** If necessary; the underlying assets can also be held in the
  same account as the managed account security.*

![Snip](media/image5.jpeg){width="6.268055555555556in"
height="3.1173611111111112in"}

Need to know more about Master setup? [Click
here](https://support.assetvantage.com/hc/en-us/articles/360019127698)

**Enter Transfer-in transactions for underlying securities**

**Step 3**

- For the same date that you chose in step 1 above, enter Transfer-in
  transactions for all the various tax lots and cash balances whose cost
  basis will sum up to \$1,000,000.

         *Note: You must enter Transfer In transactions and not Buy
transactions.*

- With transfer transactions, you will be able to enter the current
  market price and correct transfer date in the "Transfer Date" and
  "Transfer Price" fields for all these securities to ensure that
  performance is correctly calculated.

- In the Transaction Date field, select the original date of purchase,
  and in Net Amount field enter the original cost basis. At the bottom
  of the transaction window, you will find details to enter transfer
  date and price. In these fields, select the date as chosen in Step 1
  and enter the closing market price of the securities.

![Snip](media/image6.jpeg){width="6.268055555555556in"
height="3.204861111111111in"}![Snip](media/image7.jpeg){width="6.268055555555556in"
height="3.1666666666666665in"}![Snip](media/image8.jpeg){width="6.268055555555556in"
height="3.172222222222222in"}

Also, enter a Deposit transaction in the Bank & Cash module against the
same Transfer Clearing account. This amount is the cash portion of your
brokerage account which needs to be transferred in as well.

![Snip](media/image9.jpeg){width="6.268055555555556in"
height="3.0770833333333334in"}

Want to know more about how to enter transfer transactions? [Click
here](https://support.assetvantage.com/hc/en-us/articles/360019586717-Transfer-securities-Transfer-in-and-Transfer-out-from-one-account-to-another-)

- Again, since this is not an actual cash transaction, choose the same
  Transfer Clearing account, that you chose in step 1, for the second
  side of the journal entry.

- This will result in the following journal entries:

![Snip](media/image10.jpeg){width="6.268055555555556in"
height="2.921527777777778in"}![Snip](media/image11.jpeg){width="6.268055555555556in"
height="3.0444444444444443in"}![Snip](media/image12.jpeg){width="6.268055555555556in"
height="2.9138888888888888in"}

![Snip](media/image13.jpeg){width="6.268055555555556in"
height="3.025in"}

The above entry will result in balances in the below two accounts:

Dr balance in Transfer Clearing account for \$200,000 and 

Cr balance in Capital Gains -- Indirect -- On Managed Account for
\$200,000.

![Snip](media/image14.jpeg){width="6.268055555555556in"
height="2.1381944444444443in"}

![Snip](media/image15.jpeg){width="6.268055555555556in"
height="3.1173611111111112in"}

**Pass a Journal Entry**

**Step 3**

**\**
A simple journal entry (as follows) between the two will zero out these
balances.

![Snip](media/image16.jpeg){width="6.268055555555556in"
height="3.1527777777777777in"}![Snip](media/image17.jpeg){width="6.268055555555556in"
height="3.082638888888889in"}

**We hope you are now able to post transfers from a managed account into
a brokerage account with underlying securities. Still have questions?
Reach out to AV\'s Customer Success Team.**
