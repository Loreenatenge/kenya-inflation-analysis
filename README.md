# Kenya Inflation Drivers Analysis (1980–2024)

This project looks at what has been driving inflation in Kenya over the past four decades using annual World Bank data. It combines data cleaning, exploratory analysis, correlation analysis, and OLS regression modelling to identify the key statistical drivers of Kenya's inflation rate.

Live dashboard: https://kenya-inflation-analysis-cujeayhpgc8z69srsnpfwh.streamlit.app/

## What the project covers

The analysis examines five variables: inflation, exchange rate, broad money supply, GDP growth, and a food production index. Two OLS regression models are estimated and compared, with attention to multicollinearity between the explanatory variables.

## Tools

Python, pandas, matplotlib, seaborn, statsmodels, Streamlit

## Data source

World Bank - World Development Indicators

## Project structure

data/ - raw and cleaned datasets  
notebooks/ - exploratory data analysis  
src/ - data cleaning and fetching scripts  
dashboard/ - Streamlit app