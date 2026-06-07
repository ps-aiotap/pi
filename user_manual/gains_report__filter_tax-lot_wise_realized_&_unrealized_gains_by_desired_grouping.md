This report maintains tax-lot wise gain & loss and can be run for both
realized and unrealized gains.

Powered by AV\'s robust report filtering, this is a great report for
liquidity planning and also makes tax planning a breeze for your
accountant. You can see a complete break-up on every lot under every
script, whether it is in long term or in short term - if in short term
then the system constantly updates the number of days to long term.

Grandfathering computation of long-term capital gains is also integrated
in regions where applicable.

**Generating Gains report**

**Step 1:** Go to Menu \> Analytics \> Gains Report

------------------------------------------------------------------------

**Step 2: **Put your custom filters to generate the report as you
desire.

------------------------------------------------------------------------

The gains report can also be generated in Grid View to export into a
comma-separated value CSV or MS Excel format for further analysis and
processing outside of AV.

 

------------------------------------------------------------------------

*Notes* -

1.  For faster report generation and export of report there is an option
    available of \'Download CSV\'. On click of \'Grid View\' checkbox
    this option will be enabled and user can download CSV grid view
    export for quick output in case of large data.

2.  Indexation will be computed only for INR Entities (Entities with
    base currency as INR).

3.  Total LTCG column - A single column to refer for the applicable long
    term or grandfathering or indexation gain/loss. This column will be
    visible only when the \'Grandfathered LTCG (India)\' checkbox is
    checked.

4.  **Direct Equity (INR Entity):**

    - For all Non-INR securities, upto 2 years holding period- system
      will treat Gain as Short term Gain. For Holding Period more than 2
      years, system will treat Gain as Long Term Gain.

    - Indexation will be computed for non-INR equity (listed/ Unlisted)
      and INR equity (Unlisted).

5.  **Mutual Fund (INR Entity):**

    - For all Non-INR securities, upto 3 years holding period- system
      will treat Gain as Short term Gain. For Holding Period more than 3
      years, system will treat Gain as Long Term Gain.

    - Indexation will be computed for non-INR securities.

    - For INR debt mutual funds purchase and redeem on or after 1st
      April, 2023 - system will treat Gain as Short term Gain.

6.   **Market Linked Debenture  (INR Entity): **

- For Bond & Debentures marked as \'Market Linked Debenture\' under bond
  master screen (Listed & Unlisted)  - the system will treat Gain as
  Short term Gain if the sell is on or after 1st April, 2023.

7\. The gains/losses from Private Equity, Managed Accounts and Unitized
Funds are categorised as Short Term by default. These can be manually
classified as Long Term by using the system generated tag \'\_Is Long
Term\' in the following transactions irrespective of the period for
which these are held:\
\
For Private Equity Funds - Distribution, Income, Expense, Recallable
Distribution\
For Managed Accounts - Withdrawal, Income, Expense\
For Unitized Funds - Withdrawal, Income, Expense

**We hope this article helps you understand the Gains report. Still have
questions? Reach out to AV\'s Customer Success Team.**

 
