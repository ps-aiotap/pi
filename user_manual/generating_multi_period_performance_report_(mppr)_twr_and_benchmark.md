**Explaining TWR and how the report works**

The time-weighted return (TWR) measures the compound rate of growth in
an investment. The TWR breaks up the return on investment into separate
intervals based on whether money was added or withdrawn, and then
provides the rate of return for each sub-period or interval that had
cash flow changes.

This report allows you generate Absolute or Annualized Time Weighted
Returns for a single entity or a group of multiple entities. You can
even track TWR performance for multi periods like month-to-date (MTD),
quarter-to-date (QTD), year-to-date (YTD), calendar-year-to-date (CYTD),
financial-year-to-date (FYTD), 1 year, 2 years, since inception, and
more.

The report is available two ways:

- Cumulative Multi-Period

- Custom

Note: The TWR benchmark return percentage is supported too, for both
Cumulative multi-period and Custom ranges. Generate the report with
AV\'s standard grouping filters for entities or groups, along with
partnership look-through and multi-currency support. 

**The TWR formula for positions or grouping**

Formula for day 1 = Ending Market Value/ Absolute Cashflow

Formula for other days = \[(Ending Market Value + Cashflow) / Previous
Ending Market Value\]

**The TWR formula for benchmark positions**

Formula = \[Benchmark Value on Report To Date or full sell Date
(whichever is earlier)/ Report From Date - 1 or first transaction date -
1 (whichever is earlier)\]

**Generating the multi-period performance report**

**Step 1 **

Go to 'Menu', 'Analytics', then 'Multi-Period Performance Report'.

![](media/image1.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 2**

Select the dropdowns to generate your report.

![](media/image2.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

- **Report Type:** Choose between \'Cumulative Multi-Period\' or
  \'Custom\'; the latter helps you generate the report for a specific
  period using the 'From' and 'To' sections, while the former lets you
  generate the report for multiple periods like MTD, QTD, CYTD, and more
  via the 'Period' column.

- **Report Currency:** Select your preferred reporting currency.

- **Denomination**: Select the denomination that best allows you to read
  large figures

- **Show Columns:** Select options to be shown in your report, including
  'Benchmark', \'Position ID\'.

Tip: The TWR Report is also available in the grid view format; selecting
this view shows you details like 'Security Identifiers' and 'All
Position Tags'. 

- **Valuation with Accrued Income checkbox:** This shows bond valuations
  with accrued income (aka dirty value) when checked, and without
  accrued income (aka clean value) when unchecked.

Note: Clicking this will not have any impact on your TWR computation. 

**Step 3**

Now, you can view your processed report.

![](media/image3.png){width="6.268055555555556in"
height="3.4770833333333333in"}

Note:  In the image above, the column 'TWR% (A)' is the annualized TWR
for that specific period. 

**Assigning a benchmark at the position level**

**Step 4**

Update the benchmark by going to 'Menu', 'Masters', and finally,
'Positions'.

![](media/image4.png){width="6.268055555555556in"
height="3.4770833333333333in"}

**Assign a benchmark at the grouping level (primary/secondary)**

**Step 5**

To assign benchmarks at the grouping level, go to 'Masters' from the
'Menu, then head to 'Benchmarks'. Select your group from the dropdown at
the top left, then selecting the benchmarks you want to edit.

Note:  The default benchmark will be set to none, although it can be
adjusted to align with chosen benchmarks that reflect both your
investment preferences and your investment manager\'s strategy.

![](media/image5.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

![](media/image6.png){width="6.268055555555556in"
height="3.4770833333333333in"}

**Generating MPPR on the report book **

**Step 6**

Go to 'Menu', 'Report Book', then to 'Add Widget', and finally, to the
'Pie & Table' widget.

![](media/image7.gif){width="6.268055555555556in"
height="3.5256944444444445in"}

**Step 7**

Click the filter icon to get a pop-up that lets you select your report
type. There, choose 'Cumulative Multi-Period Performance Report' or
'Custom Multi-Period Performance Report', check 'Benchmark Information'
in the 'Other fields' section if required, and click 'Process' to
generate the report.

![](media/image8.png){width="6.268055555555556in"
height="3.4770833333333333in"}

![](media/image9.png){width="6.268055555555556in"
height="3.4770833333333333in"}

Note: MPPR computes and shows the TWR for a period at an aggregate level
(Strategy, Account, Advisor, etc.) even if the first underlying
investments are incepted within the reporting period and not held for
the entire period. 

*Want more information about the report book? Check out this article on
'Creating configurable reports'.*

**We hope you are now familiar with the multi-period performance report
and are ready to use it. Still have questions? Feel free to reach out to
AV\'s Customer Success Team.**
