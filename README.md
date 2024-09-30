# nasdaq100_hedge_fund_dashboard
Hedge funds and investors can leverage insights from the top KPI performers of NASDAQ-100 companies to identify high-growth opportunities and make informed investment decisions, utilizing key metrics such as P/E ratio, YoY revenue growth, D/E ratio etc. to assess financial health and growth potential in a dynamic market.

# NASDAQ-100 Companies Financial Dashboard for Hedge Funds and Investors
Investors often rely on various financial metrics to make informed decisions about their investments. Among these, key performance indicators (KPIs) such as asset turnover, revenue growth, and liquidity ratios provide critical insights into a company's operational efficiency, profitability, and financial stability. For instance, by analyzing the asset turnover ratio, investors can gauge how effectively a company utilizes its assets to generate revenue. A rising trend in this metric suggests improved efficiency and stronger sales performance, making it an appealing option for investment.

Moreover, metrics like year-over-year (YoY) revenue growth and earnings per share (EPS) growth are vital in assessing a company's profitability trajectory. Consistent growth in revenue indicates that a company is successfully expanding its market share, while increasing EPS signifies improved profitability on a per-share basis. These metrics, when monitored over time, can help investors identify companies with sustainable growth potential. Our dashboard prominently features these metrics, allowing users to easily track and compare performance trends for different companies within the NASDAQ-100.

In addition to performance and profitability metrics, liquidity measures such as the cash ratio and current ratio play a crucial role in assessing a company's financial health. The cash ratio helps investors understand a company’s ability to cover its short-term obligations, while the current ratio provides insight into overall liquidity. A company with a strong liquidity position is generally seen as less risky, making it a more attractive investment option. We have implemented these liquidity metrics in our dashboard, enabling investors to evaluate a company's short-term financial stability at a glance.

Furthermore, debt and leverage metrics, including the debt to equity ratio and interest coverage ratio, allow investors to understand the level of financial risk associated with a company. A lower debt to equity ratio indicates that a company is using less leverage, which is often perceived as a sign of financial prudence. On the other hand, a high interest coverage ratio suggests that a company can comfortably meet its interest obligations, thereby reducing the risk of default. Our dashboard provides these insights, helping investors assess the financial leverage and risk profile of potential investments.

Finally, average risk metrics such as the Altman Z-Score and Beneish M-Score serve as crucial indicators of a company's financial health and transparency. The Altman Z-Score predicts the likelihood of bankruptcy, while the Beneish M-Score assesses the potential for earnings manipulation. By incorporating these scores into our dashboard, we empower investors to filter out high-risk companies and focus on those with strong financial fundamentals.

In summary, our dashboard has been designed to present these essential metrics clearly and intuitively, providing investors with the tools they need to make informed decisions. By leveraging these performance, liquidity, and risk metrics, investors can better navigate the complexities of the market and identify the best opportunities for their investment portfolios.

# Project Structure

This project consists of the following files and directories:
```markdown
project_root/
├── .streamlit/
│   └── config.toml
├── virtual_env/
│   └── activate_this.py
├── .gitignore
├── README.md
├── app.py
├── cleaned_data.csv
├── company_assets.png
├── create_a_virtual_environment.bat
├── daq.png
├── nasdaq_100_metrics_ratios.csv
└── nasdaq_100y.ipynb
└── requirements.txt
```

- `.streamlit/`
  
- `config.toml`: Configuration file for Streamlit, an open-source app framework used to create and share data apps.

- `virtual_env/`
  
- `activate_this.py`: Script to activate the virtual environment, ensuring the project uses the correct dependencies.

- `.gitignore`: Specifies files and directories that Git should ignore, preventing them from being tracked in version control.

- `README.md`: Contains information about the project, including an introduction, installation instructions, and usage guidelines.

- `app.py`: Main Python script for running the application, including helper functions, sidebar, and main panel setup.

- `cleaned_data.csv`: CSV file with cleaned NASDAQ-100 data, ready for analysis or use within the application.

- `company_assets.png`: Image file, possibly used for visual representation within the project.

- `create_a_virtual_environment.bat`: Batch script to create a virtual environment on Windows systems.

- `daq.png`: Another image file, likely used for visual representation within the project.

- `nasdaq_100_metrics_ratios.csv`: CSV file containing raw financial metrics and ratios for NASDAQ-100 companies.

- `nasdaq_100y.ipynb`: Jupyter notebook for exploratory data analysis on historical NASDAQ data.

- `requirements.txt`: Lists all dependencies needed to run the project, ensuring the correct packages are installed.


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
