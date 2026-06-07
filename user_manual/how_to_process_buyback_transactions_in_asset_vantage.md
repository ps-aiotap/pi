**What is a Buyback?**

A buyback occurs when a company purchases its own shares from
shareholders, reducing the number of shares outstanding in the market.
In terms of capital gains, a buyback can impact Short-Term Capital Gains
(STCG) and Long-Term Capital Gains (LTCG) depending on the holding
period. 

However, as per the Indian taxation rule, gains derived from buybacks
are exempt from tax for transactions dated between July 6th, 2019, and
September 30th, 2024.

**Booking a Buyback Transaction**

To properly account for a buyback transaction in Asset Vantage, follow
the steps below:

**Step 1: Navigate to the Transaction Module**

Go to Menu \> Transactions \> Direct Equity Module

**Step 2: Add the Sell Transaction with Buyback Tag**

Either add a new Sell Transaction using the "+" in the top right-hand
corner, or click the edit symbol next to an existing Sell Transaction.

When entering the sell transaction details, locate the Tags field on the
Add/Edit/Copy transaction screen.

**Add the \'\_Is Buyback\' Tag:**

Select the \'\_Is Buyback\' tag from the Tags dropdown. This
system-generated tag is crucial for identifying the transaction as a
buyback.

The \'\_Is Buyback\' tag is only applicable to sell transactions within
the Direct Equity module. The system will ignore this tag for other
transaction types or modules.

**Important:** In the case the transaction date falls between July 6th,
2019, and September 30th, 2024, it qualify for the tax exemption. If the
transaction is tagged as \'\_Is Buyback,\' the gains derived from this
transaction will not be taxable and will not appear in the UI or export
files.

**Impact on the Transaction Module**

Once the \'\_Is Buyback\' tag is applied, it will influence both the
transaction module and the Gains Report as follows:

**In the Transaction Module - **The \'\_Is Buyback\' tag will be visible
in the Tags column of the transaction list screen. This ensures
transparency and easy identification of buyback transactions.

**Impact on the Gains Report**

Go to menu \> analytics \> gains report.

Once the user processes from the filter and the Gains Report opens up.
You will observe a Buyback Tag column positioned after the Purchase
Index Value column. This column will display the \'\_Is Buyback\' tag
for transactions where it is applied.

**Exemption Based on Date Range:**

The special tax treatment and gain/loss exemptions for buyback
transactions apply only if the buyback occurred between July 6th, 2019,
and September 30th, 2024. For transactions tagged as \'\_Is Buyback\'
within this date range:

- Short-Term Capital Gains (STCG) and Long-Term Capital Gains (LTCG)
  will not be calculated, and these columns will display 0.

- Grandfathering & Indexation will not apply, ensuring the gains are
  completely exempt and these columns will also display 0. 

(Please Note: The logic applies regardless of the lot relief method
selected for the transaction)

**Outside the Exempt Date Range:**

If a buyback transaction is booked outside this specified date range,
the gains/losses will be computed and reported as usual:

- For shares held for less than 12 months, STCG will apply, and the
  gains will be taxable.

- For shares held for more than 12 months, LTCG will apply, with gains
  being subject to taxation based on current rules.

- All relevant columns, including Short Term, Long Term, Indexation
  Gain/Loss, LTCG (Taxable), and Grandfathered LTCG (Non Taxable), will
  be computed and displayed under their respective column headers.
