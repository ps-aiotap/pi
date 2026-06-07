The Specific Lot mode in a Sell, Redemption or Transfer-Out transaction
allows users to select specific open tax lot and custom quantities
against each lot to relieve.  Users can either select a pre-set method
such as FIFO, LIFO, Minimum Gain / High Cost, Tax Efficient Loss
Harvesting or select Specific Lot to custom select open tax lots to be
relieved.

**Entering Specific Lot Transactions**

- **Menu **\> **Transactions **\> **Direct Equity** \> **Sell /
  Transfer-Out Transaction**\>** Specific Lot (check)**.

- **Menu **\> **Transactions **\> **Mutual Fund** \> **Redemption /
  Transfer-Out Transaction**\> **Specific Lot (check)**.

![](media/image1.png){width="6.268055555555556in"
height="3.765972222222222in"}

*Note: Please enter the quantity, price, and net amount in the above
fields before checking the "Specific Lot" checkbox.*

**Lot relief Method**

Once the Specific Lot checkbox is checked, Open Tax lots as on
Transaction date will show in the transaction window. The relieved
quantity in Open Tax Lots will be updated based on method selected as
per logic defined below: 

**FIFO (First In First Out)**

Relieves lots based on Buy date (Ascending Order). Lots Purchased first
will be relieved first. 

**LIFO (Last In First Out)**

Relieves lots based on Buy date (Descending Order). Lots Purchased last
will be relieved first. 

**Minimum Gain / High Cost**R\
elieves lots based on Adjusted Buy Price. Lots with highest Adjusted Buy
Price will be relieved first. 

**TELH (Tax Efficient Loss Harvesting)**

Relieves lots in a fashion that will result in lowest tax liability.
Lots are relieved in following sequence:  

1.  Lots resulting in Short-Term loss (If multiple, lot with highest
    Adjusted Price will be considered first)

2.  Lots resulting in Long-Term Loss (If multiple, lot with highest
    Adjusted Price will be considered first)

3.  Lots resulting in Long-Term Gain (If multiple, lot with highest
    Adjusted Price will be considered first)

4.  Lots resulting in Short-Term Gain (If multiple, lot with highest
    Adjusted Price will be considered first)

**Specific Lot**

User can select the \'Specific Lot\' checkbox to relieve quantity from
any open tax lots. Relieved Qty field will be editable.

![](media/image2.png){width="6.268055555555556in"
height="3.7756944444444445in"}

![](media/image3.png){width="6.268055555555556in"
height="2.395138888888889in"}

If a custodial electronic feed is enabled and tagged to an account, for
ease of posting and verifying remaining tax lots with the custodian,
user can also refer to** Feed Tax** **Lots** within the Sell /
Transfer-Out transaction which will list the Lot wise open holding from
Feed at close of business on the Transaction date for the Selected
Security. If user selects specific lot method there will be Auto Relieve
button which will automatically adjust the relieved Qty of the feed
lot.\
\
Note - Auto relief button will be applicable only if feed tax lots is
available from feed 

![](media/image4.png){width="6.268055555555556in"
height="3.115972222222222in"}

Once user saves the transaction, the voucher will be created based on
lots selected while posting the transaction. The Gain/Loss will be
computed based on Adjusted price of the lots relieved and same will be
reflected on Gains report.

![](media/image5.png){width="6.268055555555556in"
height="3.3090277777777777in"}

In the transaction list view, users can also easily filter Specific Lot
transactions using the column "Specific Lot".  Transaction type column
will also mention "Specific lot" as shown for easy identification.

![](media/image6.png){width="6.268055555555556in" height="1.025in"}

**Open Lot Report after posting Specific Lot transaction**

![](media/image7.png){width="6.268055555555556in"
height="1.0916666666666666in"}

 

**Out of turn edits / deletions **

In case of any out of turn transactions posted that have specific tax
lot sells or transfer outs the system will re-process all the subsequent
transactions as per account default lot relief method.  The impacted
transactions that have been changed from Specific Lot to the account
default method will be highlighted in red for reference for the user to
re-post. 

**Impact on Analytics / Performance Reporting **

There is no impact on performance across any of the analytics reports as
a Specific Lot sell or Transfer-Out doesn't change the cash flow.

**Upload Specific lot transactions**

- There is a new column added in upload formats of Direct Equity and
  Mutual fund as "Specific Lot". The new column will also be part of the
  transaction export.

- While uploading a Specific Lot transaction, the value in this column
  to be updated as "Yes".

![](media/image8.png){width="6.268055555555556in"
height="0.30069444444444443in"}

- The transaction will be highlighted in red for user to update Relieved
  Qty.

![](media/image9.png){width="6.268055555555556in"
height="0.9548611111111112in"}

- User can Edit the transaction, update Relieved Qty and Save.

![](media/image10.jpeg){width="6.268055555555556in" height="3.825in"}

- The transaction will be saved, and voucher will be created as per lots
  relieved by the user.

![](media/image11.jpeg){width="6.268055555555556in"
height="4.072222222222222in"}

**We hope you are now familiar with using specific lot relief method.
Still have questions? Reach out to AV\'s Customer Success Team.**

 
