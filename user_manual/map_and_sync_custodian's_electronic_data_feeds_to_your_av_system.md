**Listing Unmapped Feeds**

**PCR/Electra Data Feed Sync**

- Click on "Menu" and go to "Masters".

![](media/image1.png){width="6.268055555555556in"
height="2.9243055555555557in"}

![](media/image2.png){width="6.268055555555556in"
height="2.9243055555555557in"}

- Go to "Accounts".

![](media/image3.png){width="6.268055555555556in"
height="2.9243055555555557in"}

- Select your "Entity/Firm" ; Select "Asset: Custodian" and then hit
  "Process".

It's imperative to select only "Asset: Custodian". While investment
transactions from the feed are posted in the custodian account, Cash
transactions are posted in the default bank (or payee/payor) account
associated with that custodian account. This prevents duplication.

![](media/image4.png){width="6.268055555555556in"
height="2.9180555555555556in"}

All custodian accounts will be listed. Notice that some will have an
extra set of icons as opposed to others. This is because those accounts
(with extra set of icons) are mapped to the feed. What we will see is
how to map feed to corresponding Custodian Account created in AV by the
user.

![](media/image5.png){width="6.268055555555556in"
height="2.9277777777777776in"}

**Mapping Feeds**

- Click on the "Edit" button of the "Unmapped" Custodian account (ones
  with 3 sets of icons).

![](media/image6.png){width="6.268055555555556in"
height="2.2729166666666667in"}

- Edit Dialogue box will open. Click on "Sync Accounts" to map the
  PCR/Electra Account to AV Account.

![](media/image7.png){width="6.268055555555556in"
height="2.9368055555555554in"}

You will have to find the corresponding PCR/Electra Account for which
you want to map it to the AV custodian Account. Quick way is to type the
last 4 digits of the "Account Number" and match it with the AV Custodian
Account Number as shown below.

- Select the appropriate account and click on on "Save".

![](media/image8.png){width="6.268055555555556in"
height="3.4520833333333334in"}

Now you will notice a series of new icons that have come up against the
Custodian account we just\
mapped with the PCR/Electra Account. All the icons are still WIP but the
most Important of all is to check if the feeds are coming in properly.

**Checking Feeds**

- Click on Feed Account \"Details\".

![](media/image9.png){width="6.268055555555556in"
height="2.890972222222222in"}

- A Feed Account dialogue box will open. Select "transactions" from the
  filter and then select the date range for which you want to check the
  details for. Hit on "Process".

![](media/image10.png){width="6.268055555555556in"
height="3.722916666666667in"}

You can now see the list of transactions that came in through the
PCR/Electra Feed. You have an option to also export them in CSV format
by clicking on the CSV export icon on the top right corner.

![](media/image11.png){width="6.268055555555556in" height="3.73125in"}

- Close the box. On the right hand corner you can see a Satellite icon.
  Click on it. This gives a real time\
  update on which PCR/Electra Accounts are sitting unmapped and that you
  have to Sync it to the existing AV Custodian Account. This is just a
  quick check on the Mapped/Unmapped PCR/Electra Feeds.

![](media/image12.png){width="6.268055555555556in"
height="2.845138888888889in"}

**Syncing Transactions**

- Now let's look at how to sync and process the transactions from the
  feed. Go to "Menu" and hit "Transactions\".

![](media/image13.png){width="6.268055555555556in"
height="2.8569444444444443in"}

- Click on "Transaction Sync".

![](media/image14.png){width="6.268055555555556in"
height="2.890972222222222in"}

- Select your "Entity" and then hit on "Process".

![](media/image15.png){width="6.268055555555556in"
height="2.8666666666666667in"}

This page displays the sync history for all mapped accounts. You can see
the list of accounts that are\
waiting to be synced with the system or already have been synced. You
can make out by the number of transactions that are mentioned. To see if
there any more transactions to be synced, select the date range and then
check the box against that account and click "Start Sync".

*Note: These transactions are just sitting here for your review and have
not being posted into the\
system as yet. We will look at that in the next steps.*

![](media/image16.png){width="6.268055555555556in"
height="2.8847222222222224in"}

- Notice the amount of transactions that are now waiting to be
  processed. You will be able to see those\
  transactions under the "Process" Tab. Go to "Process" tab on the top
  right corner.

![](media/image17.png){width="6.268055555555556in"
height="2.8847222222222224in"}

- Select your "Entity" , "Account" and the appropriate date range for
  which you want to process the transactions. Note that if you don't
  select the account, all the transactions and accounts that were listed
  in the "Sync" screen will be listed.

![](media/image18.png){width="6.268055555555556in"
height="2.8847222222222224in"}

You will see the list of transactions that are synced and are ready to
be processed in the system.

**Processing Synced Transactions**

The ones in green are denoting correctly synced transactions. The ones
in pink show errors. Please note you will have to go through every
transactions to run through for any errors/wrong mapping etc before\
processing. Its always a good idea to do a quick review.

- To fix the errors click on "Edit" button against the line transaction.

![](media/image19.png){width="6.268055555555556in"
height="2.8847222222222224in"}

*Note: After fixing errors, if you hit on "Save" that particular
transaction will directly get posted in the system. If there are any
corporate action transactions, then you need to update complete details
and save the transaction.*

![](media/image20.png){width="6.268055555555556in"
height="2.1354166666666665in"}

- Select the transactions you want to post and then hit on "Process".

*Note: you may either select multiple transactions or individual ones to
have better control over what is\
being processed.*

![](media/image21.png){width="6.268055555555556in"
height="2.8847222222222224in"}

- To see the recently uploaded transaction, go back to "Menu" \>
  "Transactions" \> and click on the corresponding "Asset Class" of
  recently uploaded transaction. In this case Direct Equity.

![](media/image22.png){width="6.268055555555556in"
height="2.847916666666667in"}

![](media/image23.png){width="6.268055555555556in"
height="2.8847222222222224in"}

- Select the "Entity" \> "Account" \> "Date Range" and hit "Process".

![](media/image24.png){width="6.268055555555556in"
height="2.8819444444444446in"}

All the transactions are now listed down on the screen. These include
the transactions posted from the feed as well.

![](media/image25.png){width="6.268055555555556in"
height="2.847916666666667in"}

This completes the process of how to Sync your PCR/Electra Feeds with
your AV Custodian Accounts and then check the transactions at a staging
area before finally uploading it into the system.

**We hope you are now able to map, sync and process transactions
seamlessly through feeds. Still have questions? Reach out to AV\'s
Customer Success Team.**
