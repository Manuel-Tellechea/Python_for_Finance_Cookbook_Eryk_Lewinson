from tools.libs import *
from tools.indicators import realized_volatility

# ---------------------------------------------------------
# Download the data and keep the adjusted close prices only
# ---------------------------------------------------------
df = yf.download(
    "AAPL",
    start="2000-01-01",
    end="2010-12-31",
    progress=False
)

# NOTE:
# In recent versions of yfinance, prices are auto-adjusted by default.
# Therefore, the 'Close' column already represents adjusted close prices
# (equivalent to 'Adj Close' in older versions and in the book).
df = df.loc[:, ["Close"]].rename(columns={"Close": "adj_close"})

# Ensure the index is of datetime type
df.index = pd.to_datetime(df.index)

# ---------------------------------------------------------
# Calculate simple and log returns using adjusted close prices
# ---------------------------------------------------------
df["simple_rtn"] = df["adj_close"].pct_change()
df["log_rtn"] = np.log(df["adj_close"] / df["adj_close"].shift(1))
df = df.dropna()

# ---------------------------------------------------------
# Calculate the monthly realized volatility
# ---------------------------------------------------------
df_rv = (
    df["log_rtn"]
    .groupby(pd.Grouper(freq="ME"))   # Month-End (pandas recommendation)
    .agg(realized_volatility)         # ensures one value per month
    .to_frame(name="rv")
)

# ---------------------------------------------------------
# Annualize the realized volatility
# ---------------------------------------------------------
df_rv["rv"] = df_rv["rv"] * np.sqrt(12)

# ---------------------------------------------------------
# Plot the results
# ---------------------------------------------------------
fig, ax = plt.subplots(2, 1, sharex=True)

ax[0].plot(df.index, df["log_rtn"])
ax[0].set_title("Log Returns")

ax[1].plot(df_rv.index, df_rv["rv"])
ax[1].set_title("Annualized Monthly Realized Volatility")

plt.tight_layout()
plt.show()