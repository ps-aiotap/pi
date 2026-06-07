**Background:** \
\
Time-weighted return is a measure used to calculate profit or loss in
percentage terms. It is somewhat complex because it uses the geometric
mean to determine the return. 

In the AV system, time-weighted return is available in both the
Analytics section and the Report Book. Additionally, you
may encounter terms such as Annualized Time-Weighted Return and
Benchmark Time-Weighted Return, which are variations of the
time-weighted return. 

We will now help you understand time-weighted returns by using an
example to demonstrate how the calculations are done in the AV system. 

To calculate the Time-Weighted Return (TWR), we will divide the process
into two parts: 

1.  In the first part, we will calculate the gains generated between two
    cash flows and determine the ratios based on those returns. 

<!-- -->

2.  In the second part, we will use the geometric mean to calculate
    TWR. 

3.  

**Part 1: What is a Ratio, and how is it Calculated?** 

1.  A ratio is the percentage return calculated to measure the change in
    value between two cash flows over the selected reporting period. 

 

2.  The following formula is used to calculate the ratio: 

 \
**a. For the first cashflow:**   \
 ![](media/image1.png){width="2.4166666666666665in"
height="0.5416666666666666in"}

***Note:** The ratio should be 1 if there are no cash flows in the first
row (i.e., only the opening value is available).*

Both the cash flow and Ending Market Value (EMV) are available in the
debug file, as shown in the image below. 

![](media/image2.png){width="6.208333333333333in"
height="1.6666666666666667in"} 

**\**

**b. For the remaining cashflows  ** 

 ![](media/image3.png){width="3.625in" height="0.6180555555555556in"}

 

 

Cashflow and Ending Market Value (EMV) is available in the debug files
as shown in the image below. 

 ![A screenshot of a computer Description automatically
generated](media/image4.png){width="6.104166666666667in"
height="1.6458333333333333in"} 

 

**Part 2: How to Calculate TWR Using the Geometric Mean?** 

1.  Time-weighted return is simply the geometric mean of the multiple
    returns. 

<!-- -->

2.  The TWR formula used in the AV system is based on the following
    equation: 

**TWR = \[ Product (Select the range of all ratios) -- 1\]**. 

3.  The formula should be directly applied in the Excel workbook using
    the "=Product" function. 

<!-- -->

4.  Please refer to below image for a sample: 

![A screenshot of a computer Description automatically
generated](media/image5.png){width="6.268055555555556in"
height="1.601388888888889in"} 

**Pre-Defined rules:** 

1.  If there is no cashflow in the debug file in the first row, the
    ratio will be 1. 

2.  By default, the debug file provides details up to 2 levels, i.e.,
    primary and secondary. If the user wants to see details of each
    holding in the debug file, the primary and secondary filters need to
    be changed accordingly. 

**Basic Checks for TWR Queries:**    ** ** 

1.  The ratio should be the first item to check in the case of any TWR
    queries. A high ratio usually has a greater impact on the final TWR
    percentage. 

2.  Check the very first line of the debug file. The first cashflow and
    its EMV might show a significant difference due to an incorrect
    price taken in the transaction. 
