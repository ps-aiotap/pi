**Example 1:**\
** \**
Sometime when there are complex or multiple corporate actions, it is
important to look at the impact the transaction has on the security in
the custodian statement along with the flow of corporate action to
understand how you would be able to add that in the System.

As of April,'2025: 

  --------------------------------------------------------------------------
  **Holdings**                       **Quantity**   **Cost**   **Market
                                                               Value**
  ---------------------------------- -------------- ---------- -------------
  Lions Gate Entertainment Corp      105            618.44     932.4
  Class A                                                      

  Lions Gate Entertainment Corp      190            1,038.15   1516.2
  Class B                                                      

  TOTAL                                             1,656.59   2,448.6
  --------------------------------------------------------------------------

 

In May'2025, There was following corporate actions:

As per Custodian:

  ----------------------------------------------------------------------------------
  **Transactions**                            **Date**      **Units**   **Amount**
  ------------------------------------------- ------------- ----------- ------------
  1\) Received from a merger with Lions Gate  7^th^ May     7            
  Entertainment Corp Class A                  2025                      

  2\) Received from a merger with Lions Gate  7^th^ May     117          
  Entertainment Corp Class A                  2025                      

  3\) Removal of Lions Gate Entertainment     7^th^ May     -105         
  Corp Class A due to merger                  2025                      

  4\) Received from a merger with Lions Gate  7^th^ May     12           
  Entertainment Corp Class B                  2025                      

  5\) Received from a merger with Lions Gate  7^th^ May     190          
  Entertainment Corp Class B                  2025                      

  6\) Removal of Lions Gate Entertainment     7^th^ May     -190         
  Corp Class B due to merger                  2025                      

  7\) Cash in lieu proceeds from Lions Gate   7^th^ May                 4.28
  Entertainment Corp                          2025                      
  ----------------------------------------------------------------------------------

 

  ---------------------------------------------------------------------
  **Holdings**                  **Quantity**   **Cost**   **Market
                                                          Value**
  ----------------------------- -------------- ---------- -------------
  Lions Gate Entertainment Corp 307            930.15     2219.61

  Starz Entertainment Corp      19             726.44     398.24

  TOTAL                                        1,656.59   2,617.85
  ---------------------------------------------------------------------

 

As Per Google Reference:

1.  Lions Gate Entertainment Corp Class A: Shareholder of Lions Gate
    Entertainment Corp Class A got 1.12 shares of both Lions Gate
    Entertainment Corp and Starz Entertainment Corp.

2.  Lions Gate Entertainment Corp Class B: Shareholder of Lions Gate
    Entertainment Corp Class B got 1 share of both Lions Gate
    Entertainment Corp and Starz Entertainment Corp.

3.  Starz Entertainment Corp: The shares of Starz Entertainment Corp had
    a reverse split of 1:15 after shares were distributed. 

 

**AV System:**

**Step 1:**\
\
Book a **"Merger"** transaction on **7th May 2025** for **Lions Gate
Entertainment Corp Class A** security.

![](media/image1.jpeg){width="6.263888888888889in" height="3.0in"}

- The ratio is added based on the removed and received quantities as per
  the *2^nd^ and 3^rd^ *transaction details.

** **

**Step 2:**\
\
Book a **"Merger"** transaction on **7th May 2025** for **Lions Gate
Entertainment Corp Class B** security.

![A screenshot of a computer AI-generated content may be
incorrect.](media/image2.jpeg){width="6.268055555555556in"
height="3.0055555555555555in"}

- The ratio is added based on the removed and received quantities as per
  the *5^th^ and 6^th^ *transaction details.

**Step 3:**\
\
Book a **"Demerger"** transaction on **8th May 2025** for **Lionsgate
Studios** security.

![A screenshot of a computer AI-generated content may be
incorrect.](media/image3.jpeg){width="6.263888888888889in"
height="2.9930555555555554in"}

- The ratio is added based on the received quantities of **Starz** as
  per the *1^st^ and 4^th^ *transaction details.

 

- The cost allocation is calculated using the holding details
  of **Starz**, by dividing the cost of Starz in proportion to the total
  holding cost.

 

**Step 4:**\
\
Add the Cash in lien transaction as deposit in Bank Module using the
ledger "Long Term Capital Gains -- Indirect" ledger since the cash
coming in is not impacting the cost. 

![A screenshot of a computer AI-generated content may be
incorrect.](media/image4.jpeg){width="6.263888888888889in"
height="3.0in"}

 
