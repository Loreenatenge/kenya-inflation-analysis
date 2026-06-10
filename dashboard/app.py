import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import statsmodels.api as sm

st.set_page_config(page_title="Kenya Inflation Analysis", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        background-color: #f7f5f0;
        color: #1a1a1a;
    }

    h1, h2, h3 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        color: #1a1a1a;
    }

    .metric-box {
        background-color: #1a1a1a;
        color: #f7f5f0;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
    }

    .metric-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #999;
        margin-bottom: 6px;
    }

    .metric-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 28px;
        font-weight: 600;
        color: #f7f5f0;
    }

    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 4px;
    }

    hr {
        border: none;
        border-top: 1px solid #ddd;
        margin: 32px 0;
    }

    .stDataFrame {
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/cleaned/kenya_final.csv")

with st.sidebar:
    st.markdown("### Kenya Inflation Analysis")
    st.markdown("---")
    st.markdown("Loreen Atenge")
    st.markdown("Economics & Statistics  \nUniversity of Nairobi")
    st.markdown("---")
    st.markdown("Data source  \nWorld Bank World Development Indicators")
    st.markdown("Period  \n1980 – 2024")
    st.markdown("Tools  \nPython, pandas, statsmodels, matplotlib, seaborn, Streamlit")
    st.markdown("---")
    st.markdown("Filter by year")
    year_range = st.slider("", int(df["year"].min()), int(df["year"].max()), (1980, 2024))
    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    st.markdown("---")
    st.markdown("Variable definitions")
    st.markdown("Inflation: annual CPI % change")
    st.markdown("Exchange rate: KES per USD")
    st.markdown("Broad money: M2 as % of GDP")
    st.markdown("GDP growth: annual real GDP % change")
    st.markdown("Food index: food production index (2014-2016 = 100)")

st.markdown('<p class="section-label">Portfolio Project — Macroeconomic Analysis</p>', unsafe_allow_html=True)
st.title("What drives inflation in Kenya?")
st.markdown("An empirical analysis using World Bank data, 1980–2024")

st.markdown("""
Inflation is one of the most direct ways macroeconomic conditions affect ordinary people.
When prices rise faster than incomes, households lose purchasing power, poverty deepens,
and planning becomes harder for both governments and businesses. Kenya has experienced
several severe inflation episodes over the past four decades, each with distinct causes
rooted in domestic policy failures, external shocks, and structural vulnerabilities.

This project uses annual World Bank data from 1980 to 2024 to identify the key statistical
drivers of inflation in Kenya. The variables examined are the exchange rate, GDP growth,
broad money supply, and a food production index. The analysis combines exploratory data
analysis with OLS regression modelling.
""")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">01 — The Data</p>', unsafe_allow_html=True)
st.markdown("### Dataset overview")
st.markdown("""
The table below shows the cleaned dataset. Each row is one year. Color shading reflects
the magnitude of each value within its column — darker means higher. This makes it easier
to spot trends and outliers across variables at a glance.
""")
st.dataframe(df.style.background_gradient(cmap="YlOrBr").format(precision=2), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">02 — Inflation History</p>', unsafe_allow_html=True)
st.markdown("### Kenya's inflation rate, 1980–2024")
st.markdown("""
Three major episodes dominate Kenya's inflation history.

In 1993, inflation hit nearly 46% ; the worst on record. This came at the peak of the
structural adjustment era, when Kenya was under IMF and World Bank pressure to liberalize
its economy. The government removed price controls, liberalized the exchange rate, and cut
subsidies, while continuing to print money to cover a large fiscal deficit. The result was
a sharp depreciation of the shilling combined with the sudden removal of price controls,
which together drove inflation to its highest level in Kenya's modern history.

In 2008, inflation reached 26%, driven by a global food and fuel price shock. Kenya, as a
net importer of oil and several food commodities, was directly exposed to these external
pressures. Post-election violence in early 2008 compounded the shock by disrupting domestic
food supply chains and agricultural production.

In 2011, a severe Horn of Africa drought pushed food prices up sharply, while the shilling
depreciated to around 107 KES per USD. The Central Bank responded by raising interest rates
aggressively, eventually bringing inflation under control but at a cost to growth.

More recently, the 2022 surge in global fuel and wheat prices following the Russia-Ukraine
war caused inflation to rise again, though better monetary policy management kept it more
contained than in earlier episodes.
""")

fig, ax = plt.subplots(figsize=(11, 4))
fig.patch.set_facecolor("#f7f5f0")
ax.set_facecolor("#f7f5f0")
ax.plot(df["year"], df["inflation"], color="#1a1a1a", linewidth=2)
ax.fill_between(df["year"], df["inflation"], alpha=0.06, color="#1a1a1a")
ax.axhline(y=5, color="#c0392b", linestyle="--", linewidth=1, label="5% reference line")
ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("Inflation (%)", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#ccc")
ax.spines["bottom"].set_color("#ccc")
ax.legend(fontsize=9)
plt.tight_layout()
st.pyplot(fig)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">03 — All Variables</p>', unsafe_allow_html=True)
st.markdown("How each variable moved over time")

variables = {
    "inflation": ("Inflation (%)", "#1a1a1a"),
    "exchange_rate": ("Exchange Rate (KES/USD)", "#2c3e7a"),
    "broad_money": ("Broad Money (% of GDP)", "#2a7a4b"),
    "gdp_growth": ("GDP Growth (%)", "#7a2c2c"),
    "food_index": ("Food Production Index", "#7a5c2c"),
}

fig2, axes = plt.subplots(3, 2, figsize=(12, 10))
fig2.patch.set_facecolor("#f7f5f0")

var_list = list(variables.items())
for i, (var, (label, color)) in enumerate(var_list):
    row, col = divmod(i, 2)
    ax = axes[row][col]
    ax.set_facecolor("#f7f5f0")
    ax.plot(df["year"], df[var], color=color, linewidth=1.8)
    ax.set_title(label, fontsize=10, fontweight="600")
    ax.set_xlabel("Year", fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#ccc")
    ax.spines["bottom"].set_color("#ccc")

axes[2][1].set_visible(False)
plt.tight_layout()
st.pyplot(fig2)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">04 — Correlation Analysis</p>', unsafe_allow_html=True)
st.markdown("### Pairwise correlations between variables")
st.markdown("""
Before running the regression, I examined the pairwise correlations between all variables.
Values close to 1 mean two variables move strongly together, values close to -1 mean they
move in opposite directions, and values near 0 suggest little linear relationship.

Two things stand out immediately. The exchange rate and food production index are correlated
at 0.93, and exchange rate and broad money are correlated at 0.81. This is multicollinearity
, when independent variables are too closely related to each other, including all of them in
one regression model distorts the coefficient estimates and makes it hard to isolate the
effect of any single variable.

GDP growth has the strongest negative correlation with inflation at -0.45, suggesting that
periods of stronger economic growth in Kenya tend to coincide with lower inflation.
""")

fig3, ax3 = plt.subplots(figsize=(7, 5))
fig3.patch.set_facecolor("#f7f5f0")
ax3.set_facecolor("#f7f5f0")
numeric_cols = ["inflation", "exchange_rate", "broad_money", "gdp_growth", "food_index"]
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", fmt=".2f", ax=ax3,
            linewidths=0.5, linecolor="#eee", cbar_kws={"shrink": 0.8})
ax3.set_title("Correlation Matrix", fontsize=11, fontweight="600")
plt.tight_layout()
st.pyplot(fig3)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">05 — Regression Analysis</p>', unsafe_allow_html=True)
st.markdown("OLS regression models")
st.markdown("""
I estimated two OLS (Ordinary Least Squares) regression models with inflation as the
dependent variable. OLS works by finding the linear combination of variables that minimizes
the sum of squared differences between actual and predicted inflation values.
""")

y = df["inflation"]

st.markdown("Model 1 — Full model")
st.markdown("""
The first model included exchange rate, GDP growth, and broad money. Only GDP growth was
statistically significant at the 5% level. Exchange rate and broad money were both
insignificant , largely because of the multicollinearity identified earlier, where they
were competing with each other to explain the same variation. The condition number of 1000
confirmed a serious multicollinearity problem in this specification.
""")

X1 = df[["exchange_rate", "gdp_growth", "broad_money"]]
X1 = sm.add_constant(X1)
model1 = sm.OLS(y, X1).fit()
st.text(model1.summary().as_text())

st.markdown("#### Model 2 — Reduced model (preferred)")
st.markdown("""
The second model dropped broad money, which had the weakest result in Model 1. Removing it
resolved most of the multicollinearity , the condition number dropped from 1000 to 190.
Both remaining variables became statistically significant and the R-squared stayed almost
unchanged at 0.277, confirming that broad money was not adding meaningful explanatory power.
This is the preferred specification.
""")

X2 = df[["exchange_rate", "gdp_growth"]]
X2 = sm.add_constant(X2)
model2 = sm.OLS(y, X2).fit()
st.text(model2.summary().as_text())

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">R-squared</div>
        <div class="metric-value">{model2.rsquared:.3f}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">F-statistic</div>
        <div class="metric-value">{model2.fvalue:.3f}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Observations</div>
        <div class="metric-value">{int(model2.nobs)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-label">06 — Findings and Policy Implications</p>', unsafe_allow_html=True)
st.markdown("What the results say:")
st.markdown("""
1.GDP growth is the strongest driver of inflation in Kenya. A one percentage point increase
in GDP growth is associated with a 1.49 percentage point reduction in inflation. This
suggests that stronger real economic activity helps keep prices in check, possibly through
improved domestic supply capacity and reduced pressure on imports.

2.The exchange rate also matters. A depreciation of the shilling is associated with higher
inflation, which is consistent with Kenya's structural dependence on imports. When the
shilling weakens, the cost of fuel, food commodities, and manufactured goods rises and
feeds directly into consumer prices. This points to exchange rate stability as an important
part of Kenya's inflation management strategy.

3.The model explains 28% of the variation in inflation. The remaining 72% reflects factors
not captured here ; weather shocks, global commodity price cycles, fiscal policy, and
supply chain disruptions. This is consistent with the broader literature on inflation in
sub-Saharan Africa, which finds that supply-side and external factors are major drivers
that are difficult to capture in simple time series models.

4.Broad money supply was not independently significant, suggesting that monetary transmission
in Kenya operates more through the exchange rate channel than directly through money supply.
Changes in money supply appear to affect inflation primarily by influencing the exchange
rate rather than by directly raising domestic demand.

From a policy standpoint, sustaining GDP growth through productive investment remains the
most reliable path to price stability in Kenya. Strengthening foreign exchange reserves and
diversifying the export base would also reduce Kenya's vulnerability to the exchange rate
shocks that have historically been a consistent source of inflationary pressure.
""")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p class="section-label">Data: World Bank World Development Indicators &nbsp;|&nbsp; Analysis: Loreen Atenge, University of Nairobi</p>', unsafe_allow_html=True)
