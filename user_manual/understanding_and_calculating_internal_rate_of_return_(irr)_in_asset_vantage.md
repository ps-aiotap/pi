**What is IRR?  \**

The Internal Rate of Return (IRR) is a financial metric used to assess
an investment\'s profitability. It represents the discount rate at which
the net present value (NPV) of all cash flows from a project or
investment equals zero. IRR allows investors to compare and rank
potential investments based on their expected returns---the higher the
IRR, the more attractive the investment.** **

**Finding and Calculating IRR in the Asset Vantage Platform **

**\**
a. You can find IRR in multiple reports under "Analytics" and the
"Report Book".  ** **

**\**
b. Asset Vantage system lets you calculate IRR using either the transfer
date or the transaction date, depending on your preference.** **

 

**IRR Calculation -- Simplified Explanation** 

a\. The initial cash flow should be negative, usually representing a
purchase. If no purchase occurs on the report\'s \'From Date,\' the
first cash flow will be the opening value with a negative sign. If
neither a purchase nor an opening value exists on the \'From Date,\' the
next purchase will be considered the initial cash flow. 

b\. The IRR cash flow range always begins with a negative value and ends
with a positive value. 

c\. If the position is closed within the selected period or before the
report\'s \'To Date,\' the positive sell value will be the last cash
flow. If the position remains open within the selected period or by the
\'To Date,\' its valuation will be considered the final cash flow and
recorded as a positive value. 

d\. Purchase & Opening value (i.e. Cash outflow) will have a negative
value. 

e\. Please note that IRR is a reliable performance metric when the
investment period exceeds one year. However, for periods shorter than a
year, IRR may produce inflated values. In such cases, the Time-Weighted
Return (TWR) is a more suitable metric for measuring performance. 

f\. In AV, we use XIRR function of the MS Excel to compute the IRR. 

** **

**Sample\**

+---------------+--------------+-------------------+
| Transaction   | Date         | Cashflow          |
| type          |              |                   |
+===============+==============+===================+
| Purchase      | 05-Mar-2020  |   (2,50,000.00)   |
+---------------+--------------+-------------------+
| Purchase      | 12-Mar-2020  |   (2,50,000.00)   |
+---------------+--------------+-------------------+
| Purchase      | 19-Mar-2020  | (2,50,000.00)     |
+---------------+--------------+-------------------+
| Full Sell     | 16-Aug-2021  |                   |
|               |              |                   |
|               |              | 15,66,233.31      |
+---------------+--------------+-------------------+

 

If we use the XIRR function on the above cashflow and dates, IRR will be
67.34% 

![A screenshot of a computer Description automatically
generated](media/image1.png){width="4.729166666666667in"
height="2.1180555555555554in"}
