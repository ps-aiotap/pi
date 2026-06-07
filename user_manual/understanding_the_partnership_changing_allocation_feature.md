**A brief background of the feature**

Previously, all cash flows, Ending Market Values (EMV), and amounts for
reports such as the Portfolio Activity Report, Multiple Period
Performance Report (MPPR), and widgets were allocated based on
partnership percentages as of the report's 'To Date.' However, this
approach led to inaccuracies when contributions or withdrawals occurred
mid-period. 

To address this issue, the Partnership Changing Allocation feature
ensures that allocations are based on actual sub-periods within the
reporting period, improving accuracy.     

**How does the feature work?  **

The feature introduces sub-periods whenever contributions or withdrawals
occur during the reporting period. Each sub-period is allocated based on
the partnership ratios applicable for that specific sub-period. 

**Example of Partnership Changing Allocation in action** \
\
Suppose Alex, Casey, and Jordan are partners with equal shares
initially. If Alex withdraws from the partnership on 15th May 2023, the
system creates the following sub-periods: 

 \
**1. April 1, 2023 -- May 14, 2023 \**
\
**2. May 15, 2023 -- March 31, 2024 **

- For the first sub-period, the allocation remains equal among all three
  partners. 

<!-- -->

- For the second sub-period, since Alex has withdrawn, only Casey and
  Jordan share the cash flows equally. 

**\
3. Key components of the feature\
A. Sub-Period Splits**

When a contribution or withdrawal occurs, the system splits the
reporting period into sub-periods. Each sub-period follows an allocation
logic based on the applicable partnership ratios. 

**B. Debug File Enhancements **

The debug file now includes a new **"Partners Table"** tab, displaying
individual partner shares per sub-period, original cash flows, and
adjusted cash flows based on applicable ratios. 

**C. Circular Reference Detection **

The system alerts users to circular references in partnership
configurations, providing clear details and steps for resolution. 

**4. Visualizing the process **

The table below illustrates how sub-period splits occur based on
partnership transactions. 

  --------------------------------------------------------------------
  **Period **            **Partners **          **Allocation **
  ---------------------- ---------------------- ----------------------
  **1st April - 14th     Alex, Casey, Jordan    33.33%, 33.33%,
  May **                                        33.33% 

  **15th May - 31st      Casey, Jordan          50%, 50% 
  March **                                      

  ** **                                          
  --------------------------------------------------------------------

**5. Real-world example **

Consider a scenario where three partners share profits equally.
Mid-year, one partner leaves, and another joins. The system dynamically
adjusts the allocation to reflect these changes, ensuring a fair
distribution for each sub-period. 

**6. Benefits of the feature **

1\. Accurate reporting: Allocation percentages are dynamic and reflect
actual partnership changes. \
2. Improved debugging: Enhanced debug files provide clarity on
partner-level allocation. \
3. User-friendly: UI enhancements and detailed error messages make the
feature easy to use. 
