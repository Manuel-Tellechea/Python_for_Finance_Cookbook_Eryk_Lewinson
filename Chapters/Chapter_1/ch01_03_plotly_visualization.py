from tools.libs import *

# ---------------------------------------------------------
# Download the data and keep the adjusted close prices only
# ---------------------------------------------------------
df = yf.download(tickers="MSFT", period='max', auto_adjust=False, progress=False)

df = df.loc[:, ["Adj Close"]].rename(columns={"Adj Close": "adj_close"})

# Ensure the index is of datetime type
df.index = pd.to_datetime(df.index)

# yfinance returns a MultiIndex even for a single ticker in some setups.
# Example: MultiIndex([('adj_close','MSFT')], names=['Price','Ticker'])
# Extract the price series explicitly and rebuild a "flat" dataframe.
price = df[("adj_close", "MSFT")].copy()
price.name = "Price"

df = pd.DataFrame({"Price": price})

# ---------------------------------------------------------
# 2) Compute returns (simple and log)
# ---------------------------------------------------------
df["simple_return"] = df["Price"].pct_change()
df["log_return"] = np.log(df["Price"] / df["Price"].shift(1))

# Optional: drop NaNs only for returns plotting (keeps price intact)
returns_df = df[["simple_return", "log_return"]].dropna()

# Plotly
# ---------------------------------------------------------
# 3) Plot: Price + Returns (3 rows, shared x-axis)
# ---------------------------------------------------------
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.07,
    subplot_titles=("Price", "Simple Returns", "Log Returns")
)

# Row 1: Price
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Price"],
        mode="lines",
        name="Price"
    ),
    row=1, col=1
)

# Row 2: Simple returns
fig.add_trace(
    go.Scatter(
        x=returns_df.index,
        y=returns_df["simple_return"],
        mode="lines",
        name="Simple Return"
    ),
    row=2, col=1
)

# Row 3: Log returns
fig.add_trace(
    go.Scatter(
        x=returns_df.index,
        y=returns_df["log_return"],
        mode="lines",
        name="Log Return"
    ),
    row=3, col=1
)

# Layout tweaks
fig.update_layout(
    title="MSFT Time Series",
    height=800,
    showlegend=True
)

# Axis labels (optional)
fig.update_yaxes(title_text="USD", row=1, col=1)
fig.update_yaxes(title_text="Return", row=2, col=1)
fig.update_yaxes(title_text="Return", row=3, col=1)
fig.update_xaxes(title_text="Date", row=3, col=1)

fig.show()