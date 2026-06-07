**Understanding Buybacks and Their Impact on Capital Gains**

A **buyback** happens when a company repurchases its own shares from
shareholders, reducing the total number of shares available in the
market. This can have an impact on **capital gains**, which are
categorized based on the holding period of the shares: 

- **Short-Term Capital Gains (STCG):** Applies if the shares are held
  for **less than 12 months** before the buyback. 

<!-- -->

- **Long-Term Capital Gains (LTCG):** Applies if the shares are held
  for **more than 12 months** before the buyback.

**Tax Implications of Buybacks in India** 

Under Indian tax regulations, **any gains from buybacks are exempt from
tax** for transactions that occur **between July 6, 2019, and September
30, 2024**. This means shareholders do not have to pay **STCG or LTCG
tax** on buybacks during this period. 

**Booking a Buyback Transaction** 

To properly account for a buyback transaction in Asset Vantage, follow
the steps below: 

**Step 1: Navigate to the Transaction Module** 

- Go to **Menu \> Transactions \> Direct Equity Module**. 

**Step 2: Add the Sell Transaction with Buyback Tag** 

- **Add a New Sell Transaction:** 

<!-- -->

- When entering the sell transaction details, locate the Tags field on
  the Add/Edit/Copy transaction screen. 

<!-- -->

- **Add the \'\_Is Buyback\' Tag:** 

<!-- -->

- Select the \'\_Is Buyback\' tag from the Tags dropdown. This
  system-generated tag is crucial for identifying the transaction as a
  buyback. 

<!-- -->

- The \'\_Is Buyback\' tag is only applicable to sell transactions
  within the Direct Equity module. The system will ignore this tag for
  other transaction types or modules. 

**Important:** If your buyback transaction falls between **July 6, 2019,
and September 30, 2024**, it qualifies for a **tax exemption**. When you
tag the transaction as **\"\_Is Buyback,\"** any gains from it **will
not be taxed** and **will not be displayed** in the UI or export files. 

 

**How \'\_Is Buyback\' tag impacts the Transaction Module and Gains
Report?** 

Once the \'\_Is Buyback\' tag is applied, it will influence both the
transaction module and the Gains Report as follows: 

- **Impact on the Transaction Module** 

In the Transaction Module, the \'\_Is Buyback\' tag will be visible in
the Tags column of the transaction list screen. This ensures
transparency and easy identification of buyback transactions. 

- **Impact on the Gains Report** 

Let's first understand the steps through which you can generate
and analyze your **Gains Report**: 

1.  **Navigate to the Gains Report:** \
    Go to **Menu \> Analytics \> Gains Report**. 

2.  **Select the Entity:** \
    Choose the **desired entity** for which you want to view the
    report. 

3.  **Apply Filters for Detailed Insights:** \
    Apply **Primary and Secondary Grouping** along with their
    respective **sub-grouping** to the data as needed.\
     

4.  **Set the Report Period:** \
    Select the time frame using the **dropdown menu** for automatic date
    selection. \
    Alternatively, **manually enter the dates** for a custom period. 

5.  **Generate the Report:**\
    Click the **Process** button in the filter pop-up to generate and
    view the report 

 

**Now let's see how \'\_Is Buyback\' tag impacts the Gains Report.** 

In the Gains Report, a new Buyback Tag column will be added to the Gains
Report, positioned after the Purchase Index Value column. This column
will display the \'\_Is Buyback\' tag for transactions where it is
applied. 

**Exemption for Buyback Transactions Based on Date Range** 

If your buyback transaction occurred between **July 6, 2019, and
September 30, 2024**, it qualifies for **special tax treatment and
gain/loss exemptions**. When a transaction is tagged as **\"\_Is
Buyback\"** within this date range: 

- **Short-Term Capital Gains (STCG) and Long-Term Capital Gains
  (LTCG)** **will not be calculated**---these columns will
  display **0**. 

<!-- -->

- **Grandfathering & Indexation will not apply**, ensuring that the
  gains are **fully exempt from tax**. 

<!-- -->

- This logic applies **regardless of the lot relief method
  selected** for the transaction. 

 

**Tax Treatment for Buybacks Outside the Exempt Date Range** 

If a buyback transaction occurs **outside** the specified exemption
period, the gains and losses will be **calculated and reported as per
standard tax rules**: 

- **For shares held for less than 12 months:** **Short-Term Capital
  Gains (STCG) will apply**, and the gains will be **taxable**. 

<!-- -->

- **For shares held for more than 12 months:** **Long-Term Capital Gains
  (LTCG) will apply**, and taxation will follow the **current rules**. 

All relevant columns, including **Short-Term Gains, Long-Term Gains,
Indexation Gain/Loss, LTCG (Taxable), and Grandfathered LTCG
(Non-Taxable),** will be **calculated and displayed** just like any
other normal sell transaction. 
