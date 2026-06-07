In our system, the Benchmark IRR is calculated using the Public Market
Equivalent (PME) method. 

**How is it Calculated?** 

- The PME method determines the final cash flow using index values and
  specific formulas. 

<!-- -->

- Once this final cash flow is established, the XIRR function is applied
  to calculate the Internal Rate of Return (IRR).

**Example:**\
As shown in the image below, the Report Period is from 2014-03-31 to
2015-06-18, and the calculated IRR is 15.87%, derived using the XIRR
function on the given cash flows. \
![A screenshot of a computer Description automatically
generated](media/image1.png){width="4.729166666666667in"
height="2.736111111111111in"} 

**Step 1: Understanding Cashflows and Cashflows Date** 

To calculate the IRR, cashflows (CF) and their corresponding dates (CF
Date) must be available as shown in the image above. 

- Purchase type cashflows are recorded as negative values, while sell or
  valuation type cashflows appear as positive values.

<!-- -->

- The cashflow array typically starts with a purchase transaction.
  However, if there is no purchase on the "From Date" of the report, an
  opening value (represented as a negative amount) is used instead. 

<!-- -->

- If neither a purchase transaction nor an opening value exists on the
  "From Date", then the first available purchase transaction becomes the
  starting point of the cashflow array. 

- 

**Step 2: Assigning Index Values** 

For each cashflow, make sure to assign the corresponding index value as
shown in the image below. 

![A screenshot of a computer Description automatically
generated](media/image2.png){width="5.756944444444445in"
height="1.8055555555555556in"} 

 

**Step 3: Calculating PME Equivalent** 

- The first row in this column is determined by the first actual
  cashflow or the opening value, which serves as the starting point for
  the calculation.![A screenshot of a computer Description automatically
  generated](media/image3.png){width="6.268055555555556in"
  height="1.457638888888889in"} 

 

- **For the second row and onwards:** \
  Use the following formula to calculate the PME Equivalent as shown
  below: 

 

**(Current Index Value / Previous Index Value)
× Previous PME Index Equivalent + Current Cashflow**![A screenshot of a
computer Description automatically
generated](media/image4.png){width="6.268055555555556in"
height="1.4277777777777778in"} 

 

- **For the last row:** \
  The PME equivalent is calculated using the formula as shown below: 

 

**(Current Index Value / Previous Index Value)
× Previous PME Index Equivalent** 

![A screenshot of a computer Description automatically
generated](media/image5.png){width="6.268055555555556in"
height="1.4465277777777779in"} 

**Step 4: Calculating PME Cashflow** 

- All cashflows in this column **(PME Cash Flows)** remain identical to
  the original cashflows **(CF column)**, except for the last cashflow. 

<!-- -->

- The last cashflow is derived from the final value in
  the **\"PME Index Equivalent\"** column. If this value is negative, it
  should be converted into a positive value.\
  \
  ![A screenshot of a computer screen Description automatically
  generated](media/image6.png){width="6.268055555555556in"
  height="1.1861111111111111in"}

**Step 5: Calculation Of IRR**

- Now that the final PME cashflow has been determined in Step 4, we can
  calculate the PME Benchmark IRR (%) using the XIRR function. This is
  done by applying the highlighted PME Cash Flows along with their
  respective cashflow dates (CF column) as inputs in the formula, as
  shown in the image below. 

![A screenshot of a computer screen Description automatically
generated](media/image7.png){width="6.268055555555556in"
height="1.7409722222222221in"} 

 

 
