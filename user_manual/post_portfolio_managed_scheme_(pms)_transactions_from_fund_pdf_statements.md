Following are the steps to upload detailed PMS transactions (Buy/Sell)
PDF statement.

**Finding File Converter**

**Step 1**

Go to : **Menu** \> **Transactions **\> **File Converter**.** **

![](media/image1.png){width="6.268055555555556in"
height="2.877083333333333in"}

**Uploading Statements**

**Step 2**

- If the fund house format is supported, it will be listed below.
  ([Complete
  List](https://assetvantagehelp.zendesk.com/knowledge/articles/4402984945553/en-us?brand_id=360001836298))

- Upload the fund PDF statement, then click on Go icon (orange check
  icon) to process.

- If the file is password protected, please select check box and
  mentioned the password before processing the file.

![](media/image2.png){width="6.268055555555556in"
height="1.9333333333333333in"}

**Step 3**

On processing, AV generates a zip folder.

Extract the zip folder and open the excel file(s) which
have ***Assetvantage DE*** and ***Assetvantage MF ***in the filenames.

![](media/image3.png){width="5.270833333333333in"
height="0.4861111111111111in"}

**Check your *Asset Vantage -- DE* file before uploading to AV.**

Please ensure following items are correctly captured in excel files:

- **Column A (Entity name / First holder\*)**:\
  Ensure this name is exactly same as the display name in Asset Vantage
  system.

- **Column C (ISIN\*)**:\
  Check ISIN numbers are available against all stocks. There should not
  be any NA.

- **Column J (DP Client ID No / Custodian Account Number \*) and column
  N (Payee/Payor/Bank Account Number\*)**:\
  Add your PMS account number/client ID in this column.

Also, ensure the (Quantity, Price, Net amount, STT, brokerage etc)
columns are in number format. There shouldn't be any text commas in
columns.

**Check your *Asset Vantage -- MF* file before uploading to AV.\**
Please ensure following items are correctly captured in excel files:

- **Column B (INVESTOR_NAME \*):**\
  Ensure this name is exactly same as the display name in Asset Vantage
  system.

- **Column D (Folio Number \*)**:\
  Ensure this is same your PMS account number/client ID.

- **Column G (ISIN\*)**:\
  Check ISIN numbers are available. There should not be any NA or blank.

Also, ensure the (Quantity, Price, Net amount, STT, brokerage etc)
columns are in number format. There shouldn't be any text commas in
columns.

**Setting up accounts**

**Step 4**

Bank Account Setup and Custodian Account Setup. 

Please refer
to [Masters](https://support.assetvantage.com/hc/en-us/articles/360018602817-Creating-masters-for-advisor-credit-rating-position-derivatives-future-options-Equities-stocks-securities-using-bulk-file-upload)

**Uploading**

**Step 5**

File upload.

Once the account masters are setup, you can upload the direct equity and
mutual funds files.

**Direct Equity Upload**

- Go to **Menu **\> **Transactions **\> **Direct Equity**.

- Go to upload tab. Choose Entity from drop down.

- Select date format as "dd-mmm-yyyy". 

- You can now attach your file from upload icon.

- Once the transactions are uploaded, you can select checkbox and
  process the transactions.

- If you see transactions in red, please rectify the error in excel and
  reupload the file or edit the transaction from screen and save the
  transaction.

![](media/image4.png){width="6.268055555555556in"
height="2.0708333333333333in"}

![](media/image5.png){width="6.268055555555556in"
height="0.6576388888888889in"}

![](media/image6.png){width="6.268055555555556in" height="2.34375in"}

**Mutual Fund Upload**

- Go to **Menu **\> **Transactions **\> **Mutual Funds**.

- Go to upload tab. Choose Entity from drop down.

- Select file format as "AVMutualFund" and date format as
  "dd-mmm-yyyy". 

- You can now attach your file from upload icon.

- Once the transactions are uploaded, you can select checkbox and
  process the transactions.

- If you see transactions in red, please rectify the error in excel and
  reupload the file or edit the transaction from screen and save the
  transaction.

![](media/image7.png){width="6.268055555555556in"
height="2.0708333333333333in"}

![](media/image8.png){width="6.268055555555556in"
height="0.7534722222222222in"}

![](media/image9.png){width="6.268055555555556in"
height="2.227777777777778in"}

**Position Tagging**

**Step 6**

- Go to **Master** \> **Position**.** **

- Choose an entity and type the *PMS account number* in the search box.\
  \
  ![](media/image10.png){width="6.268055555555556in"
  height="2.089583333333333in"}

- You can now select all positions and edit any one position master.
  Before saving the position master, make sure check box against
  strategy/Asset class/Advisors are selected. This will help you to
  apply same tagging for other selected positions.

![](media/image11.png){width="6.268055555555556in"
height="2.5506944444444444in"}

![](media/image12.png){width="6.268055555555556in"
height="3.634027777777778in"}
