Without a streamlined process, transferring funds between bank accounts
within the same legal entity can lead

to some complications, such as duplicated transactions when syncing bank
feeds. Hence, the best practice is

to create and use an intermediate ledger account called \'Cash
Transfer\' to record such transactions as follows:

**Illustration **

If \$5,000 is transferred from account number xxxx4235 to account number
xxxx3443:

**Step 1**\
\
Record \$5,000 as a \'Withdrawal\' entry type for account number
xxxx4235 but tag the \'Cash Transfer\' ledger

account instead of the transferee account number xxxx3443 directly.\
\
![](media/image1.png){width="6.268055555555556in"
height="3.0729166666666665in"}\
**Step 2**

Record \$5,000 as a \'Deposit\' entry type for account number xxxx3443,
but tag the \'Cash Transfer\'\
ledger account instead of the transferor account number xxxx4235
directly.

![](media/image2.png){width="5.451388888888889in"
height="2.6666666666666665in"}

The \'Cash Transfer\' ledger account will thus not have any effective
balance but of both the bank accounts will 

reflect accurate amounts without directly interfering with each other.

**Common Issues**

If only one transaction for the above transfer is recorded by tagging
the transferor and transferee bank accounts directly, instead of using
an intermediate 'Cash Transfer' ledger account, the following issues may
arise:

- **Risk of duplication:** If the individual bank feeds of both bank
  accounts are enabled, duplicate entries may appear in the transferee
  account upon syncing transactions from its feed. This occurs because
  tagging the transferee bank account updates its ledger balance, but
  the transaction does not appear on the transaction list screen.

- **Risk of human error:** Since the transferee bank account's ledger
  balance gets updated if it is tagged directly, users need to manually
  check for and delete any duplicate entries in the transferee
  account's feed before syncing transactions. This leaves room for human
  error and may result in inaccurate account balances.

** **

![](media/image3.png){width="5.458333333333333in"
height="2.6666666666666665in"}

Hence, using an intermediate \'Cash Transfer\' ledger account for
booking cash transfers between bank accounts within the same legal
entity enhances accuracy, reduces duplication risk, and simplifies the
reconciliation process. 

It is advisable to implement this approach for error-free financial
records and streamlined internal cash management procedures.

 
