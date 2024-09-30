# nasdaq100_hedge_fund_dashboard
Hedge funds and investors can leverage insights from the top KPI performers of NASDAQ-100 companies to identify high-growth opportunities and make informed investment decisions, utilizing key metrics such as P/E ratio, YoY revenue growth, D/E ratio etc. to assess financial health and growth potential in a dynamic market.

# Financial Metrics Explained

## Introduction
This document provides explanations for various financial metrics used to evaluate companies. These metrics help investors make informed decisions by assessing different aspects of a company's financial health and performance.

## Key Financial Metrics in our Data Set

### 1. Asset Turnover
**Definition:** Measures how efficiently a company uses its assets to generate revenue.
**Formula:** $$\text{Asset Turnover} = \frac{\text{Revenue}}{\text{Total Assets}}$$
**Explanation:** A higher ratio indicates better efficiency in using assets to generate sales.

### 2. Buyback Yield
**Definition:** The percentage of shares a company buys back from the market relative to its market capitalization.
**Formula:** $$\text{Buyback Yield} = \frac{\text{Shares Repurchased}}{\text{Market Capitalization}}$$
**Explanation:** Indicates how much a company is returning to shareholders through buybacks.

### 3. CAPEX to Revenue
**Definition:** The ratio of capital expenditures to revenue.
**Formula:** $$\text{CAPEX to Revenue} = \frac{\text{Capital Expenditures}}{\text{Revenue}}$$
**Explanation:** Shows the proportion of revenue being reinvested in the business.

### 4. Cash Ratio
**Definition:** Measures a company's ability to pay off short-term liabilities with cash and cash equivalents.
**Formula:** $$\text{Cash Ratio} = \frac{\text{Cash and Cash Equivalents}}{\text{Current Liabilities}}$$
**Explanation:** A higher ratio indicates better liquidity.

### 5. Cash to Debt
**Definition:** The ratio of a company's cash and cash equivalents to its total debt.
**Formula:** $$\text{Cash to Debt} = \frac{\text{Cash and Cash Equivalents}}{\text{Total Debt}}$$
**Explanation:** Indicates the company's ability to cover its debt with cash.

### 6. COGS to Revenue
**Definition:** The ratio of cost of goods sold (COGS) to revenue.
**Formula:** $$\text{COGS to Revenue} = \frac{\text{COGS}}{\text{Revenue}}$$
**Explanation:** Shows the proportion of revenue that goes into producing goods.

### 7. Beneish M-Score
**Definition:** A model to detect earnings manipulation.
**Formula:** Complex formula involving various financial ratios.
**Explanation:** A higher score suggests a higher likelihood of earnings manipulation.

### 8. Altman Z-Score
**Definition:** A formula to predict the probability of bankruptcy.
**Formula:** $$Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E$$
**Explanation:** A score below 1.8 indicates a high risk of bankruptcy.

### 9. Current Ratio
**Definition:** Measures a company's ability to pay short-term obligations.
**Formula:** $$\text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$$
**Explanation:** A higher ratio indicates better short-term financial health.

### 10. Days Inventory
**Definition:** The average number of days a company holds inventory before selling it.
**Formula:** $$\text{Days Inventory} = \frac{\text{Inventory}}{\text{COGS}} \times 365$$
**Explanation:** A lower number indicates faster inventory turnover.

### 11. Debt to Equity
**Definition:** The ratio of total debt to shareholders' equity.
**Formula:** $$\text{Debt to Equity} = \frac{\text{Total Debt}}{\text{Shareholders' Equity}}$$
**Explanation:** Indicates the relative proportion of debt and equity in financing the company's assets.

### 12. Debt to Assets
**Definition:** The ratio of total debt to total assets.
**Formula:** $$\text{Debt to Assets} = \frac{\text{Total Debt}}{\text{Total Assets}}$$
**Explanation:** Shows the percentage of assets financed by debt.

### 13. Debt to EBITDA
**Definition:** The ratio of total debt to earnings before interest, taxes, depreciation, and amortization (EBITDA).
**Formula:** $$\text{Debt to EBITDA} = \frac{\text{Total Debt}}{\text{EBITDA}}$$
**Explanation:** Indicates how many years it would take to pay off debt using EBITDA.

### 14. Debt to Revenue
**Definition:** The ratio of total debt to revenue.
**Formula:** $$\text{Debt to Revenue} = \frac{\text{Total Debt}}{\text{Revenue}}$$
**Explanation:** Shows the proportion of revenue needed to cover debt.

### 15. E10 (by Prof. Robert Shiller)
**Definition:** The cyclically adjusted price-to-earnings ratio (CAPE) over 10 years.
**Formula:** $$\text{E10} = \frac{\text{Price}}{\text{Average Earnings over 10 years}}$$
**Explanation:** Used to assess long-term market valuation.

### 16. Effective Interest Rate
**Definition:** The actual interest rate on a loan or investment, considering compounding.
**Formula:** $$\text{Effective Interest Rate} = \left(1 + \frac{\text{Nominal Rate}}{n}\right)^n - 1$$
**Explanation:** Provides a true measure of interest cost or earnings.

### 17. Equity to Assets
**Definition:** The ratio of shareholders' equity to total assets.
**Formula:** $$\text{Equity to Assets} = \frac{\text{Shareholders' Equity}}{\text{Total Assets}}$$
**Explanation:** Indicates the proportion of assets financed by shareholders' equity.

### 18. Enterprise Value to EBIT
**Definition:** The ratio of enterprise value (EV) to earnings before interest and taxes (EBIT).
**Formula:** $$\text{EV to EBIT} = \frac{\text{Enterprise Value}}{\text{EBIT}}$$
**Explanation:** Used to value a company, considering its debt and cash.

### 19. Enterprise Value to EBITDA
**Definition:** The ratio of enterprise value (EV) to earnings before interest, taxes, depreciation, and amortization (EBITDA).
**Formula:** $$\text{EV to EBITDA} = \frac{\text{Enterprise Value}}{\text{EBITDA}}$$
**Explanation:** A lower ratio indicates a potentially undervalued company.

### 20. Enterprise Value to Revenue
**Definition:** The ratio of enterprise value (EV) to revenue.
**Formula:** $$\text{EV to Revenue} = \frac{\text{Enterprise Value}}{\text{Revenue}}$$
**Explanation:** Used to compare the value of companies with different capital structures.

### 21. Financial Distress
**Definition:** A situation where a company cannot meet its financial obligations.
**Explanation:** Indicators include low liquidity ratios and high debt levels.

### 22. Financial Strength
**Definition:** A measure of a company's overall financial health.
**Explanation:** Assessed using various ratios like current ratio, debt to equity, etc.

### 23. Joel Greenblatt Earnings Yield (by Joel Greenblatt)
**Definition:** The ratio of EBIT to enterprise value.
**Formula:** $$\text{Earnings Yield} = \frac{\text{EBIT}}{\text{Enterprise Value}}$$
**Explanation:** Used to compare the profitability of companies.

### 24. Free Float Percentage
**Definition:** The percentage of shares available for trading by the public.
**Formula:** $$\text{Free Float Percentage} = \frac{\text{Shares Available for Trading}}{\text{Total Shares Outstanding}}$$
**Explanation:** A higher percentage indicates more liquidity.

### 25. Piotroski F-Score
**Definition:** A score to assess the financial strength of a company.
**Formula:** Based on nine criteria related to profitability, leverage, liquidity, and operating efficiency.
**Explanation:** A higher score indicates a stronger financial position.

### 26. Goodwill to Assets
**Definition:** The ratio of goodwill to total assets.
**Formula:** $$\text{Goodwill to Assets} = \frac{\text{Goodwill}}{\text{Total Assets}}$$
**Explanation:** Indicates the proportion of intangible assets.

### 27. Gross Profit to Assets
**Definition:** The ratio of gross profit to total assets.
**Formula:** $$\text{Gross Profit to Assets} = \frac{\text{Gross Profit}}{\text{Total Assets}}$$
**Explanation:** Shows how efficiently a company generates profit from its assets.

### 28. Interest Coverage
**Definition:** The ratio of EBIT to interest expenses.
**Formula:** $$\text{Interest Coverage} = \frac{\text{EBIT}}{\text{Interest Expenses}}$$
**Explanation:** Indicates how easily a company can pay interest on its debt.

### 29. Inventory Turnover
**Definition:** The number of times inventory is sold and replaced over a period.
**Formula:** $$\text{Inventory Turnover} = \frac{\text{COGS}}{\text{Average Inventory}}$$
**Explanation:** A higher ratio indicates efficient inventory management.

### 30. Inventory to Revenue
**Definition:** The ratio of inventory to revenue.
**Formula:** $$\text{Inventory to Revenue} = \frac{\text{Inventory}}{\text{Revenue}}$$
**Explanation:** Shows the proportion of revenue tied up in inventory.

### 31. Liabilities to Assets
**Definition:** The ratio of total liabilities to total assets.
**Formula:** $$\text{Liabilities to Assets} = \frac{\text{Total Liabilities}}{\text{Total Assets}}$$
**Explanation:** Indicates the proportion of
