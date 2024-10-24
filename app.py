###############################################################################
# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from typing import Tuple, List, Dict
import os
import openai
import time
import tempfile
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
###############################################################################
# Page configuration
st.set_page_config(
    page_title = "NASDAQ-100 Index",
    page_icon = ":line_chart:",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# Define CSS for the box design
st.markdown("""
    <style>
    .box {
        background-color: #47413f;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 16px;
        font-weight: bold;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
    }
    .metric-delta {
        font-size: 22px;
        color: green;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

###############################################################################
# Define helper functions

# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Construct the full path to the data file
data_path = os.path.join(current_dir, 'cleaned_data.csv') 

# Function to load the dataset
@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Loads data from a CSV file named 'cleaned_data.csv'.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(data_path)

def get_arrow(value: float) -> str:
    """
    Determines the arrow direction based on the value.

    Parameters:
    value (float): The value to evaluate.

    Returns:
    str: An HTML arrow character. Returns an upward arrow (▲) if the value 
    is greater than 0, otherwise returns a downward arrow (▼).
    """
    return "▲" if value > 0 else "▼"

def get_arrow_color(value: float) -> str:
    """
    Sets the arrow color based on the value.

    Parameters:
    value (float): The value to evaluate.

    Returns:
    str: The color of the arrow. Returns 'green' if the value is greater than 0, otherwise returns 'red'.
    """
    return "green" if value > 0 else "red"

def find_top_performer(data: pd.DataFrame, metric: str) -> pd.Series:
    """
    Finds the top performer based on a specified metric.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the data.
    metric (str): The metric to evaluate.

    Returns:
    pd.Series: The row of the DataFrame corresponding to the top performer for the specified metric.
    If no data is found for the metric, a warning is displayed and None is returned.
    """
    filtered_data = data[data['metric'] == metric].dropna(subset=['value'])
    if not filtered_data.empty:
        return filtered_data.loc[filtered_data['value'].idxmax()]
    else:
        st.warning(f"No data found for the metric: {metric}")
        return None


# Function to create a donut plot
def make_donut(input_response: float, input_text1: str, input_text2: str, input_color: Dict[str, str]) -> plt.Figure:
    """
    Creates a donut chart using Altair to visually represent two categories, such as Safe and Unsafe investments.

    The chart displays a percentage of one category (e.g., Safe investments) and the remainder as the other category
    (e.g., Unsafe investments). The center of the chart shows the percentage of the first category. Hovering over each 
    section reveals a tooltip with the category name and percentage.

    Parameters:
    -----------
    input_response : int
        The percentage of the first category to display (e.g., Safe investments).
        
    input_text1 : str
        The label for the first category, which corresponds to the input_response value (e.g., "Safe Investments").
        
    input_text2 : str
        The label for the second category, representing the remainder (e.g., "Unsafe Investments").
        
    input_color : str
        The color scheme for the chart, expected values are 'green' for safe investments or 'red' for unsafe investments.

    Returns:
    --------
    alt.LayerChart
        An Altair LayerChart object containing the donut chart, where users can see both categories with their percentages.
    
    Example:
    --------
    >>> st.altair_chart(make_donut(90, "Safe Investments", "Unsafe Investments", 'green'), use_container_width=True)
    This would display a donut chart where 90% of the chart represents safe investments in green and the other 10% 
    represents unsafe investments in red.
    
    Notes:
    ------
    - The chart shows the percentage for the first category (e.g., safe investments) in the center.
    - Tooltips are enabled to display the category name and percentage upon hover.
    """
    
    # Define the color scheme based on the input_color
    chart_color = ['#27AE60', '#12783D'] if input_color == 'green' else ['#E74C3C', '#781F16']
    
    # Create the data source for the donut chart
    source = pd.DataFrame({"Category": [input_text2, input_text1], "Value": [100 - input_response, input_response]})
    
    # Create the background arc of the donut chart
    plot_bg = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="Value:Q",
        color=alt.Color("Category:N", scale=alt.Scale(domain=[input_text1, input_text2], range=chart_color), legend=None)
    ).properties(width=260, height=260)
    
    # Create the main arc of the donut chart
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="Value:Q",
        color=alt.Color("Category:N", scale=alt.Scale(domain=[input_text1, input_text2], range=chart_color), legend=None)
    ).properties(width=260, height=260)
    
    # Add the percentage text in the center of the chart
    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=32, fontWeight=700).encode(
        text=alt.value(f'{input_response} %')
    )
    
    # Return the combined chart with background, arcs, and center text
    return plot_bg + plot + text


# Define a function to create line plot for select metrics
def create_financial_plot(
    pivot_df: pd.DataFrame, 
    unique_companies: List[str], 
    color_map: Dict[str, str], 
    metric1: str, 
    metric2: str, 
    years: Tuple[int, int], 
    subplot_titles: List[str], 
    title: str
) -> go.Figure:
    """
    Create a financial plot with two subplots for the specified metrics.

    This function generates a 1x2 subplot figure displaying trends for two different
    financial metrics across a specified year range for multiple companies.

    Parameters:
        pivot_df (pd.DataFrame): DataFrame containing financial data with 'year' and 'company' columns.
        unique_companies (List[str]): List of unique company names to plot.
        color_map (Dict[str, str]): Dictionary mapping company names to their respective colors for the plot.
        metric1 (str): The first metric to be plotted on the first subplot.
        metric2 (str): The second metric to be plotted on the second subplot.
        years (Tuple[int, int]): A tuple containing the start and end years for filtering the data.
        subplot_titles (List[str]): List of titles for the subplots.
        title (str): The main title for the entire figure.

    Returns:
        go.Figure: A Plotly figure object containing the subplots with the specified metrics.
    """
    # Create a 1x2 subplot figure 
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)

    # Filter the DataFrame for the selected year range
    filtered_df = pivot_df[pivot_df['year'].between(years[0], years[1])]

    # Add traces for the first metric (metric1)
    for company in unique_companies:
        company_data = filtered_df[filtered_df['company'] == company]
        if not company_data.empty:  # Check if company_data is not empty
            fig.add_trace(go.Scatter(
                x=company_data['year'],
                y=company_data[metric1],
                mode='lines',
                name=company,
                legendgroup=company,
                line=dict(color=color_map[company])
            ), row=1, col=1)

    # Add traces for the second metric (metric2)
    for company in unique_companies:
        company_data = filtered_df[filtered_df['company'] == company]
        if not company_data.empty:  # Check if company_data is not empty
            fig.add_trace(go.Scatter(
                x=company_data['year'],
                y=company_data[metric2],
                mode='lines',
                name=company,
                legendgroup=company,
                showlegend=False,
                line=dict(color=color_map[company])
            ), row=1, col=2)

    # Update layout to ensure x-axis ticks are integers
    fig.update_xaxes(tickmode='linear', dtick=1)

    # Update layout title
    fig.update_layout(
        title_text=title,
        showlegend=True
    )

    return fig

# Define a function to calculate average m_score and companies that carries risk of manipulation
def avoid_mrisk(df: pd.DataFrame, m_threshold: float = -1.78) -> Tuple[float, List]:
    """
    Identify companies with an M-score below a specified threshold and calculate the percentage of such companies.

    The M-score is a measure used to detect the likelihood of earnings manipulation. This function filters companies
    based on their average M-score and identifies those that fall below the given threshold, indicating higher risk.

    Parameters:
    df (pd.DataFrame): DataFrame containing the following columns:
        - 'company': The name of the company.
        - 'metric': The type of metric (should include 'mscore').
        - 'value': The value of the metric.
    m_threshold (float): The threshold for the M-score to identify high-risk companies. Default is -1.78.

    Returns:
    Tuple[float, pd.Series]: A tuple containing:
        - The percentage of companies with an M-score above the threshold.
        - A Series of companies with an M-score above the threshold.
    """
    # Filter the DataFrame for M-score metrics
    m_score = df[df['metric'] == 'mscore']
    
    # Calculate the mean M-score for each company
    m = m_score.groupby('company').agg({'value': 'mean'})
    
    # Calculate the percentage of companies with an M-score below the threshold
    risk_company_pc = round(len(m[m['value'] > m_threshold]) * 100. / len(m), 0)
    
    # Identify the companies with an M-score below the threshold
    risk_company = m[m['value'] > m_threshold].index.to_list()
    
    return risk_company_pc, risk_company

# Define a function to calculate average z_score and companies that carries risk of bankruptcy
def avoid_zrisk(df: pd.DataFrame, z_threshold: float = 1.81) -> Tuple[float, List]:
    """
    Identify companies with an Z-score below a specified threshold and calculate the percentage of such companies.

    The M-score is a measure used to detect the likelihood of earnings manipulation. This function filters companies
    based on their average Z-score and identifies those that fall below the given threshold, indicating higher risk.

    Parameters:
    df (pd.DataFrame): DataFrame containing the following columns:
        - 'company': The name of the company.
        - 'metric': The type of metric (should include 'zscore').
        - 'value': The value of the metric.
    z_threshold (float): The threshold for the Z-score to identify high-risk companies. Default is 1.81.

    Returns:
    Tuple[float, pd.Series]: A tuple containing:
        - The percentage of companies with an Z-score below the threshold.
        - A Series of companies with an Z-score below the threshold.
    """
    # Filter the DataFrame for M-score metrics
    z_score = df[df['metric'] == 'zscore']
    
    # Calculate the mean M-score for each company
    z = z_score.groupby('company').agg({'value': 'mean'})
    
    # Calculate the percentage of companies with an M-score below the threshold
    risk_company_pc = round(len(z[z['value'] < z_threshold]) * 100. / len(z), 0)
    
    # Identify the companies with an M-score below the threshold
    risk_company = z[z['value'] < z_threshold].index.to_list()
    
    return risk_company_pc, risk_company

# Define a function to calculate compound annual growth rate 
def cagr(df: pd.DataFrame, cagr_period: int = 5) -> int:
    """
    Calculate the Compound Annual Growth Rate (CAGR) based on YoY EPS growth data.

    The compound annual growth rate (CAGR) is the mean annual growth rate of an 
    investment over a specified period of time longer than one year. It represents
    one of the most accurate ways to calculate and determine returns for individual
    assets, investment portfolios, and anything that can rise or fall in value over time.

    Parameters:
    - df (pandas.DataFrame): It contains columns value, metric and year.
    - cagr_period: The number of years we would want to calculate cgar over.
        

    Returns:
    int: The CAGR expressed as a percentage.
    """
    # Get the most recent year in the dataset
    current_year = df['year'].max()
    
    # Filter data for the past 5 years
    df_filtered = df[(df['metric'] == 'yoy_eps_growth') & 
    (df['year'].isin(range(current_year - cagr_period, current_year + 1)))]

    # Group by year and calculate the average YoY EPS growth for each year
    annual_avg_growth = df_filtered.groupby('year')['value'].mean()

    # Calculate the cumulative growth factor
    cumulative_growth_factor = (1 + annual_avg_growth / 100).prod()

    # Calculate the CAGR
    n = len(annual_avg_growth)
    cagr = cumulative_growth_factor ** (1 / n) - 1

    # Return the CAGR as a percentage
    return int(cagr * 100)


######################################################################
# Load data
df = load_data()

######################################################################
# Sidebar: Filters for sector, subsector, and company
with st.sidebar:
    # Construct the full path to the image file
    image_path = os.path.join(current_dir, 'daq.png')  
    # Display the image
    try:
        st.image(image_path)
    except FileNotFoundError:
        st.error(f"Image not found at path: {image_path}")
    # Add a sidebar label
    st.write("Filter the data by:")

    # User guide expander
    with st.expander("User Guide", expanded = False):
        st.write("""
        ### Welcome to the Dashboard!
        
        This application allows you to analyze various key performance indicators (KPIs) for NASDAQ-100 companies.
        
        **How to Use:**
        - Filter the data by:
            - **Select Sector**: Choose an option to filter companies by their sector.
            - **Select Subsector**: Choose an option to narrow down by subsector.
            - **Select Company**: Choose a specific company to analyze.
            - **Select Year Range**: Filter data from 2017 to 2023.

        - You can click and unclick on legends in the plot to remove or restore specific metrics for better visualization.
        
        **Data Range:** The application provides data for the years 2017 to 2023.
                 
        **Metric Trend Description**: Refer to the descriptions provided below each metric trend 
        for definitions and insights into their trends.
        """)
    # Dropdown for sector selection
    sectors = df['sector'].unique()
    selected_sector = st.multiselect('Select sector', sectors)

    # Subsector filtering based on sector selection
    if selected_sector:
        filtered_subsectors = df[df['sector'].isin(selected_sector)]['subsector'].unique()
    else:
        filtered_subsectors = df['subsector'].unique()
    selected_subsector = st.multiselect('Select subsector', filtered_subsectors)

    # Company filtering based on sector and/or subsector selection
    if selected_sector and selected_subsector:
        filtered_companies = df[(df['sector'].isin(selected_sector)) & (df['subsector'].isin(selected_subsector))]['company'].unique()
    elif selected_sector:
        filtered_companies = df[df['sector'].isin(selected_sector)]['company'].unique()
    elif selected_subsector:
        filtered_companies = df[df['subsector'].isin(selected_subsector)]['company'].unique()
    else:
        filtered_companies = df['company'].unique()
    
    selected_company = st.multiselect('Select company', filtered_companies)

    # Date range selector
    years = st.slider('Select Year Range', 2017, 2023, (2017, 2023))

    # Filter dataset based on the selection, taking into account that users can select any combination
    filtered_df = df[
        (df['year'].between(years[0], years[1])) & 
        (df['sector'].isin(selected_sector) if selected_sector else True) & 
        (df['subsector'].isin(selected_subsector) if selected_subsector else True) & 
        (df['company'].isin(selected_company) if selected_company else True)
    ]

    # Only fallback to top 5 companies if no specific filters are applied, and filtered_df would otherwise be empty
    if filtered_df.empty:
        if not selected_sector and not selected_subsector and not selected_company:
            st.write(f"Displaying the top 5 companies for the year {years[1]} based on YoY revenue growth:")
            top_companies = df[(df['metric'] == 'yoy_revenue_growth') & (df['year'] == years[1])].nlargest(5, 'value')['company']
            filtered_df = df[df['company'].isin(top_companies) & (df['year'] == years[1])]
        else:
            st.write("No data available for the selected filters.")
    else:
        st.write(f"Data for years {years[0]} to {years[1]} using your filters:")
    
    pivot_df = filtered_df.pivot_table(index=['year', 'company'], columns='metric', 
                values='value').reset_index()

    # Display the filtered DataFrame
    st.dataframe(filtered_df)


    # Allow users to download the filtered DataFrame
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )  

######################################################################
# Main panel: Display top KPIs and charts
st.markdown("<h1 style='text-align: center;'>NASDAQ-100 Financial \
            Indicators Dashboard</h1>", unsafe_allow_html=True)

# Define top performers for KPIs
current_df = df[df['year'] == years[1]].reset_index(drop=True)

pe_top_performer = find_top_performer(current_df, 'price_to_earnings_ratio')
revenue_top_performer = find_top_performer(current_df, 'yoy_revenue_growth')
debt_equity_top_performer = find_top_performer(current_df, 'debt_to_equity')

# Display top KPI performers in 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="box">
        <div class="metric-label">Highest Price-to-Earnings (P/E)</div>
        <div class="metric-value">{pe_top_performer['company']}</div>
        <div class="metric-delta">
            {get_arrow(pe_top_performer['value'])} {pe_top_performer['value']:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="box">
        <div class="metric-label">Highest Revenue Growth (YoY)</div>
        <div class="metric-value">{revenue_top_performer['company']}</div>
        <div class="metric-delta">
            {get_arrow(revenue_top_performer['value'])} {revenue_top_performer['value']:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="box">
        <div class="metric-label">Lowest Debt to Equity (D/E)</div>
        <div class="metric-value">{debt_equity_top_performer['company']}</div>
        <div class="metric-delta">
            {get_arrow(debt_equity_top_performer['value'])} {debt_equity_top_performer['value']:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Add expander for explaining the top KPI performers
with st.expander(f"Top KPI Performers for NASDAQ-100 Companies in {years[1]}"):
    st.write(f"""
        The following key metrics highlight the top-performing NASDAQ-100 companies for the year {years[1]} based on the data provided:
        
        **Price-to-Earnings (P/E) Ratio:**  
        - The Price-to-Earnings ratio (P/E) is a popular measure used to value a company by comparing its current share price 
        to its earnings per share (EPS).
        - A higher P/E suggests that investors are willing to pay more for a company's earnings, often indicating strong growth
          potential or high expectations.
        - The highest P/E ratio performer for {years[1]} is **{pe_top_performer['company']}** with a ratio of 
        **{pe_top_performer['value']:.2f}**.

        **Year-over-Year (YoY) Revenue Growth:**  
        - This metric measures the percentage increase in a company's revenue compared to the previous year. It reflects the 
        company's ability to grow and expand its sales.
        - Companies with high YoY revenue growth are typically seen as leaders in their industry, showing strong operational 
        performance.
        - The company with the highest YoY revenue growth for {years[1]} is **{revenue_top_performer['company']}**, 
        with a growth of **{revenue_top_performer['value']:.2f}%**.

        **Debt-to-Equity (D/E) Ratio:**  
        - The D/E ratio is a measure of a company's financial leverage, calculated by dividing its total liabilities by its
          shareholders' equity. A lower ratio is generally considered better, as it indicates a lower level of debt relative to equity.
        - Companies with lower D/E ratios are typically less risky, as they rely less on borrowing and have a more stable financial structure.
        - The company with the lowest D/E ratio for {years[1]} is **{debt_equity_top_performer['company']}**, with a D/E 
        ratio of **{debt_equity_top_performer['value']:.2f}**.
    """)


# Section: Donut plots for risk metrics
st.header("NASDAQ 100: Risk and Gain Metrics Over the Past 5 Years")
col1, col2, col3 = st.columns(3)

with col1:
    st.altair_chart(make_donut(int(avoid_mrisk(df)[0]), "M-Score: Likely a Manipulator", "M-Score: Safe to Invest", 'red'), 
    use_container_width=True)

with col2:
    st.altair_chart(make_donut(int(avoid_zrisk(df)[0]), "Z-Score: Likely Heading to Bankruptcy", "Z-Score: Safe to Invest", 'red'), 
    use_container_width=True)

with col3:
    st.altair_chart(make_donut(cagr(df), "NASDAQ-100 Compound Annual Growth Rate", '', 'green'), use_container_width=True)

# Add the "Read More" expander
with st.expander("Read More about Investment Avoidance and Average Retuen on Investment"):
    st.write(f"""
        **Investment Avoidance Metrics:**
        
        - The M-Score and Z-Score are key financial ratios used to assess a company's risk for fraudulent or distress behavior. 
        - Companies with a high M-Score are considered more likely to manipulate earnings, whereas a low Z-Score may indicate
         financial distress.
        - Avoidance percentages reflect how much of the total sample falls into these risky categories.
        - Companies to avoid based on current M-score: {', '.join(avoid_mrisk(df)[1])}
        - Companies to avoid based on current Z-score: {', '.join(avoid_zrisk(df)[1])}
        
        **Average Return for NASDAQ-100 Over Past 5 Years**
        
        - A high EPS growth rate is an indicator of a company's profitability and potential for long-term growth.
         The overall average return on investment when invetsed in NASDAQ-100 over past 5 years is {cagr(df)} %.
    """)

#Define a dynamic color palette using Viridis
# Generate a list of unique companies
unique_companies = pivot_df['company'].unique()

# Get the desired colormap (tab20)
cmap = plt.get_cmap('tab20')

# Generate colors dynamically based on the number of unique companies
n_colors = len(unique_companies)
colors = [cmap(i % 20) for i in range(n_colors)]  # Repeat colors after 20

# Convert RGBA colors to RGB strings
color_map = {
    company: f'rgba({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)}, {color[3]})'
    for company, color in zip(unique_companies, colors)
}

# Section 1: Performance & Profitability
st.header("Performance & Profitability Metrics")

# Line chart for Asset Turnover and Gross Profit to Assets
fig1 = create_financial_plot(pivot_df, unique_companies, color_map, 'asset_turnover', 
        'gross_profit_to_assets', years, ('Assets Turnover', 'Gross Profit to Assets'), 
        'Assets Turnover and Gross Profit to Assets')

st.plotly_chart(fig1)

# Create expander for Asset Turnover and Gross Profit to Assets Analysis
with st.expander("Asset Turnover & Gross Profit to Assets Analysis"):
    st.write(r'''
    ### Asset Turnover
    Asset Turnover is a financial metric that measures the efficiency of a company's use of its assets to generate sales revenue. 
    It is calculated using the following formula:
    
    $$ 
    \text{Asset Turnover} = \frac{\text{Net Sales}}{\text{Average Total Assets}} 
    $$

    A higher asset turnover ratio indicates that a company is utilizing its assets more efficiently. 
    - **Good:** An asset turnover ratio above 1 suggests that the company is generating more than $1 
             in sales for every dollar of assets.
    - **Bad:** A ratio below 1 indicates that the company is not effectively using its assets to generate sales,
              which could be a red flag for investors.

    Over the years, a consistently high asset turnover ratio suggests that the company is maintaining 
             its efficiency, whereas a declining ratio may signal operational issues or inefficiencies.
    ''')

    st.write(r'''
    ### Gross Profit to Assets
    Gross Profit to Assets measures the relationship between a company's gross profit and its total assets. 
    It indicates how effectively a company is using its assets to generate gross profit. The formula is:

    $$ 
    \text{Gross Profit to Assets} = \frac{\text{Gross Profit}}{\text{Average Total Assets}} 
    $$

    A higher value indicates better performance in generating gross profit relative to the assets utilized. 
    - **Good:** A ratio above 0.2 (or 20%) is often considered favorable, as it suggests the company is effectively 
        converting its assets into gross profit.
    - **Bad:** A ratio significantly below 0.1 (or 10%) may indicate that the company is struggling to convert its 
        assets into gross profit, raising concerns about its profitability.

    Year-over-year improvements in this metric can demonstrate effective management and strategic use of assets.
     Conversely, a decline could indicate increased costs or inefficiencies that need to be addressed.
    ''')

    st.write(r'''
    ### Summary
    Both metrics provide valuable insights into a company's operational efficiency and asset utilization. 
    Investors should monitor these ratios over time and compare them against industry benchmarks to assess a company's performance. 
    Improvements in these ratios often correlate with a company's ability to manage its resources effectively and maximize profitability.
    ''')


# Line chart for Year-over-Year Revenue & EPS Growth
fig2 = create_financial_plot(pivot_df, unique_companies, color_map, 'yoy_revenue_growth', 
        'yoy_eps_growth', years, ("Year-over-Year Revenue Growth", "Year-over-Year EPS Growth"),
          "Year-over-Year Revenue & EPS Growth")

st.plotly_chart(fig2)

# Create expander for YoY Revenue Growth and EPS Growth Analysis
with st.expander("YoY Revenue Growth & EPS Growth Analysis"):
    st.write(r'''
    ### YoY Revenue Growth
    Year-over-Year (YoY) Revenue Growth is a metric that compares a company's current revenue to its revenue from the same 
    period in the previous year. It helps investors gauge how well a company is growing its sales over time. The formula is:

    $$ 
    \text{YoY Revenue Growth} = \frac{\text{Current Year Revenue} - \text{Previous Year Revenue}}{\text{Previous Year Revenue}} \times 100 
    $$

    A higher YoY revenue growth percentage indicates strong sales performance.
    - **Good:** A positive growth rate suggests that the company is successfully increasing its sales, which is a positive sign for investors.
    - **Bad:** A negative growth rate indicates a decline in sales, which may signal underlying issues in the business.

    Consistent YoY revenue growth over multiple periods can indicate a strong market position and effective business strategies.
    ''')

    st.write(r'''
    ### EPS Growth
    Earnings Per Share (EPS) Growth measures the increase in a company's earnings on a per-share basis, allowing 
             investors to assess profitability growth over time. The formula for EPS growth is:

    $$ 
    \text{EPS Growth} = \frac{\text{Current Year EPS} - \text{Previous Year EPS}}{\text{Previous Year EPS}} \times 100 
    $$

    A higher EPS growth indicates better profitability and is a key metric for investors. 
    - **Good:** Positive EPS growth reflects a company that is effectively increasing its profits relative to the number of shares 
        outstanding, which can drive stock prices higher.
    - **Bad:** Negative EPS growth suggests declining profitability, raising concerns about the company's financial health.

    Monitoring EPS growth alongside revenue growth can provide deeper insights into a company's operational efficiency and profitability.
    ''')

    st.write(r'''
    ### Summary
    Both YoY Revenue Growth and EPS Growth are critical indicators of a company's financial performance and potential for future success. 
    Investors should analyze these metrics in conjunction with other financial data to make informed investment decisions. Consistent positive
     growth in these areas is often indicative of a well-managed and financially sound company.
    ''')


# Section 3: Liquidity & Cash Management
st.header("Liquidity & Cash Management Metrics")

# Line chart for Cash Ratio and Current Ratio
fig3 = create_financial_plot(pivot_df, unique_companies, color_map, 'cash_ratio', 
        'current_ratio', years, ("Cash Ratio", "Current Ratio"),
          "Cash Ratio and Current Ratio")

st.plotly_chart(fig3)

# Create expander for Cash Ratio and Current Ratio Analysis
with st.expander("Cash Ratio & Current Ratio Analysis"):
    st.write(r'''
    ### Cash Ratio
    The Cash Ratio is a liquidity metric that measures a company's ability to cover its short-term liabilities with its cash and
     cash equivalents. This ratio provides a conservative view of a company's liquidity position. The formula is:

    $$ 
    \text{Cash Ratio} = \frac{\text{Cash and Cash Equivalents}}{\text{Current Liabilities}} 
    $$

    A higher cash ratio indicates better liquidity.
    - **Good:** A cash ratio greater than 1 suggests that the company has more cash than current liabilities, indicating a strong 
        liquidity position.
    - **Bad:** A cash ratio below 0.5 may raise concerns about a company’s ability to meet its short-term obligations.

    This metric is especially important during times of financial uncertainty, as it shows how well a company can withstand 
    short-term financial challenges.
    ''')

    st.write(r'''
    ### Current Ratio
    The Current Ratio is another liquidity metric that measures a company's ability to pay its short-term liabilities with its 
    current assets. It provides a broader view of a company's financial health. The formula for the current ratio is:

    $$ 
    \text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}} 
    $$

    A higher current ratio indicates better financial health.
    - **Good:** A current ratio above 1 indicates that the company has more current assets than current liabilities, suggesting 
        it can meet its short-term obligations.
    - **Bad:** A current ratio below 1 may signal liquidity issues, as the company may not have enough current assets to cover its liabilities.

    Monitoring the current ratio alongside the cash ratio provides a more comprehensive view of a company’s liquidity position.
    ''')

    st.write(r'''
    ### Summary
    Both the Cash Ratio and Current Ratio are essential indicators of a company's liquidity and financial stability. 
    Investors should evaluate these ratios in the context of industry benchmarks and alongside other financial metrics to make 
    informed decisions. Consistently high ratios are indicative of a company that can comfortably meet its short-term obligations.
    ''')


# Section 4: Debt & Leverage
st.header("Debt & Leverage Metrics")

# Line chart for Debt to Equity and Debt to Assets
fig4 = create_financial_plot(pivot_df, unique_companies, color_map, 'cash_ratio', 
        'current_ratio', years, ("Debt to Equity", "Debt to Assets"),
          "Debt to Equity and Debt to Assets")

st.plotly_chart(fig4)

# Create expander for Asset Turnover and Gross Profit to Assets Analysis
with st.expander("Asset Turnover & Gross Profit to Assets Analysis"):
    st.write(r'''
    ### Asset Turnover
    Asset Turnover is a financial metric that measures the efficiency of a company's use of its assets 
    to generate sales revenue. It is calculated using the following formula:
    
    $$ 
    \text{Asset Turnover} = \frac{\text{Net Sales}}{\text{Average Total Assets}} 
    $$

    A higher asset turnover ratio indicates that a company is utilizing its assets more efficiently. 
    - **Good:** An asset turnover ratio above 1 suggests that the company is generating more than $1 in sales for every dollar of assets.
    - **Bad:** A ratio below 1 indicates that the company is not effectively using its assets to generate sales, which could be a red flag
             for investors.

    Over the years, a consistently high asset turnover ratio suggests that the company is maintaining its efficiency, whereas a 
    declining ratio may signal operational issues or inefficiencies.
    ''')

    st.write(r'''
    ### Gross Profit to Assets
    Gross Profit to Assets measures the relationship between a company's gross profit and its total assets. It indicates how 
    effectively a company is using its assets to generate gross profit. The formula is:

    $$ 
    \text{Gross Profit to Assets} = \frac{\text{Gross Profit}}{\text{Average Total Assets}} 
    $$

    A higher value indicates better performance in generating gross profit relative to the assets utilized. 
    - **Good:** A ratio above 0.2 (or 20%) is often considered favorable, as it suggests the company is effectively converting 
    its assets into gross profit.
    - **Bad:** A ratio significantly below 0.1 (or 10%) may indicate that the company is struggling to convert its assets into gross 
    profit, raising concerns about its profitability.

    Year-over-year improvements in this metric can demonstrate effective management and strategic use of assets. Conversely, 
    a decline could indicate increased costs or inefficiencies that need to be addressed.
    ''')

    st.write(r'''
    ### Summary
    Both metrics provide valuable insights into a company's operational efficiency and asset utilization. Investors should monitor 
    these ratios over time and compare them against industry benchmarks to assess a company's performance. Improvements in these ratios 
    often correlate with a company's ability to manage its resources effectively and maximize profitability.
    ''')


# Section 5: Risk Metrics
st.header("Average Risk Metrics over Past 5 Years")

# Filter for the last 5 years and selected companies
current_year = df['year'].max()
score_df = df[(df['year'] >= current_year - 4) & (df['company'].isin(unique_companies))]

pivot_df1 = score_df.pivot(index=['company', 'year'], columns='metric', values='value').reset_index()

# Use Altman Z-Score and Beneish M-Score with color-coded bars to visualize risk levels
agg_df = pivot_df1.groupby('company').agg({'mscore': 'mean', 'zscore': 'mean'}).reset_index()

# Assuming pivot_df1 is already defined as per your existing code

# Aggregate data to get average Z-score and M-score
agg_df = pivot_df1.groupby('company').agg({'mscore': 'mean', 'zscore': 'mean'}).reset_index()

# Identify companies to avoid
companies_to_avoid = agg_df[
    (agg_df['zscore'] < 1.81) |  # Generally, Z-score < 1.81 indicates financial distress
    (agg_df['mscore'] > -1.78)      # Generally, M-score < -2 indicates potential earnings manipulation
]['company'].tolist()

# Create subplots for Z-score and M-score
fig5 = make_subplots(rows=1, cols=2, subplot_titles=("Average Z-score", "Average M-score"))

# Add bar traces for Z-scores
for company in unique_companies:
    company_data = pivot_df1[pivot_df1['company'] == company]
    if not company_data.empty:
        z_scores = company_data.filter(like='zscore').iloc[0].values
        years = company_data.filter(like='zscore').columns.str.replace('_', ' ').str.replace('zscore', '').values
        fig5.add_trace(go.Bar(x=years, y=z_scores, name=company, marker_color=color_map[company], 
                              legendgroup= company, showlegend=True), row=1, col=1)

# Add horizontal line for Z-score threshold
fig5.add_trace(go.Scatter(
    x=[years[0], years[-1]],  # Set x-values to match the year range
    y=[1.81, 1.81],
    mode='lines',
    name='Z-Score Threshold (1.81)',
    line=dict(color='red', dash='dash')
), row=1, col=1)

# Add bar traces for M-scores
for company in unique_companies:
    company_data = pivot_df1[pivot_df1['company'] == company]
    if not company_data.empty:
        m_scores = company_data.filter(like='mscore').iloc[0].values
        years = company_data.filter(like='mscore').columns.str.replace('_', ' ').str.replace('mscore', '').values
        fig5.add_trace(go.Bar(x=years, y=m_scores, name=company, marker_color=color_map[company],
                        legendgroup= company, showlegend= False), row=1, col=2)

# Add horizontal line for M-score threshold
fig5.add_trace(go.Scatter(
    x=[years[0], years[-1]],  # Set x-values to match the year range
    y=[-1.78, -1.78],
    mode='lines',
    name='M-Score Threshold (-1.78)',
    line=dict(color='red', dash='dash', width=2)
), row=1, col=2)

# Update layout for better presentation
fig5.update_layout(title_text="Average Z-scores and M-scores",
                   xaxis_title="Year",
                   yaxis_title="Score",
                   barmode='group')  # Group bars for better visibility

# Display the plot in Streamlit
st.plotly_chart(fig5)

# Create expander for Altman Z-score and Beneish M-score
with st.expander("Altman Z-Score & Beneish M-Score Analysis"):
    st.write("The Altman Z-Score is a measure of a company's financial health and bankruptcy risk. A score below 1.81 \
             suggests a higher likelihood of bankruptcy.")
    st.write("The Beneish M-Score is used to detect earnings manipulation. A score above -1.78 indicates potential manipulation.")
    st.write("#### Companies with higher investment risk:")
    if companies_to_avoid:
        st.write(", ".join(companies_to_avoid))
    else:
        st.write("No companies to avoid based on the selected criteria.")

####################################################################################################
#####################LLM Powered Chatbot and Document Q & A ########################################
# Initialize session states for LLM powered chats
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI Assistant with expertise in both document analysis and financial advising."}
    ]

# create a list to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# This particular variable (doc_index) is used to store the FAISS
#  vector database that gets created when users upload documents.
if "doc_index" not in st.session_state:
    st.session_state.doc_index = None

# Header and Mode Selection
st.title("Financial AI Guru: Invest Smart")
mode = st.radio("Select Mode", ["Financial Advisor", "Document Q&A"], horizontal = True)

# Provide options to use models for different purposes
model_options = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo-16k",
    "dall-e-3",
    "tts-1-hd",
    "o1-preview"
]

# select a model for current session state
st.session_state["openai_model"] = st.selectbox(
    "Select Model",
    options=model_options,
    index=0
)

# Control buttons in a single row
cols = st.columns([1, 1, 1, 2])
with cols[0]:
    show_history = st.button("Show Chat History")
with cols[1]:
    clear_history = st.button("Clear History")
with cols[2]:
    st.metric("Messages", len(st.session_state.chat_history))

# Document Q&A Mode Setup
if mode == "Document Q&A":
    uploaded_files = st.file_uploader("Upload PDF documents", type=['pdf'], accept_multiple_files=True)
    
    if uploaded_files:
        if not st.session_state.doc_index: # If the document were not vectorized/embedded
            with st.spinner("Processing documents..."):
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Initialize embeddings
                        embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPEN_AI_KEY"])
                        
                        # Initialize text splitter
                        text_splitter = CharacterTextSplitter(
                            chunk_size = 1000,
                            chunk_overlap = 200
                        )
                        
                        documents = []
                        for uploaded_file in uploaded_files:
                            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                            with open(temp_file_path, "wb") as temp_file:
                                temp_file.write(uploaded_file.getvalue())
                            loader = PyPDFLoader(temp_file_path)
                            documents.extend(loader.load())
                        
                        # Split documents into chunks
                        texts = text_splitter.split_documents(documents)
                        
                        # Create vector store using Meta's FAISS
                        vectorstore = FAISS.from_documents(texts, embeddings)
                        
                        # Store the vectorstore in session state
                        st.session_state.doc_index = vectorstore
                        
                    st.success(f"Processed {len(uploaded_files)} documents")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

# Shared chat interface functions
def call_openai(prompt, mode):
    client = openai.OpenAI(api_key = st.secrets["OPEN_AI_KEY"])
    
    if mode == "Document Q&A" and st.session_state.doc_index:
        # Create ChatOpenAI instance with API key
        chat_model = ChatOpenAI(
            model=st.session_state.get("openai_model", "gpt-3.5-turbo"),
            openai_api_key = st.secrets["OPEN_AI_KEY"]  # Add the API key here
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=chat_model,
            retriever=st.session_state.doc_index.as_retriever(search_kwargs={"k": 1}),
        )
        return chain({"question": prompt, "chat_history": st.session_state.chat_history})["answer"]
    else:
        messages = [m for m in st.session_state.messages if m["role"] != "system"]
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=st.session_state.get("openai_model", "gpt-3.5-turbo"),
            messages=messages,
            stream=True
        )
        return response

# Display chat history if requested
if show_history:
    st.subheader("Chat History")
    for i, (query, response) in enumerate(st.session_state.chat_history):
        with st.expander(f"Conversation {i+1}"):
            st.write("**User:**", query)
            st.write("**Assistant:**", response)

# Clear chat history if requested
if clear_history:
    st.session_state.messages = [st.session_state.messages[0]]  # Keep system message
    st.session_state.chat_history = []
    st.rerun()

# Chat interface
for message in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            if mode == "Document Q&A":
                if not st.session_state.doc_index:
                    st.info("Please upload documents first.")
                    full_response = "Please upload documents before asking questions."
                else:
                    full_response = call_openai(prompt, mode)
                    message_placeholder.markdown(full_response)
            else:
                for chunk in call_openai(prompt, mode):
                    if hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "I encountered an error. Please try again."
        
        # Update chat history
        if full_response:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history.append((prompt, full_response))

# Display current mode and document count
if mode == "Document Q&A" and st.session_state.doc_index:
    st.sidebar.markdown(f"📚 Documents loaded: {len(uploaded_files)}")