from tools.indicators import identify_outliers
from tools.libs import *

# ---------------------------------------------------------
# Download the data and keep the close prices only
# ---------------------------------------------------------
df = yf.download("AAPL", period="max", auto_adjust=True, progress=False)

df = df.loc[:, ["Close"]].rename(columns={"Close":"close"})

# Ensure the index is of datetime type
df.index = pd.to_datetime(df.index)

# yfinance returns a MultiIndex even for a single ticker in some setups.
# Example: MultiIndex([('adj_close','MSFT')], names=['Price','Ticker'])
# Extract the price series explicitly and rebuild a "flat" dataframe.
price = df[("close", "AAPL")].copy()
price.name = "Price"

df = pd.DataFrame({"Price": price})

# ---------------------------------------------------------
# 2) Compute returns (simple and log)
# ---------------------------------------------------------
df["simple_return"] = df["Price"].pct_change()
df["log_return"] = np.log(df["Price"] / df["Price"].shift(1))

# Optional: drop NaNs only for returns plotting (keeps price intact)
returns_df = df[["simple_return", "log_return"]].dropna()

# Identifying outliers
## Calculate the rolling mean and standard deviation
df_rolling = df[["simple_return"]].rolling(window=21).agg(["mean", "std"])
df_rolling.columns = df_rolling.columns.droplevel()

# Join the rolling metrics to the original data
df_outliers = df.join(df_rolling)

# Identify the outliers and extract their values for later use
df_outliers["outlier"] = df_outliers.apply(identify_outliers, axis=1)
outliers = df_outliers.loc[df_outliers["outlier"] == 1, ["simple_return"]]

# Plot the results
fig, ax = plt.subplots()
ax.plot(df_outliers.index, df_outliers.simple_return, color="blue", label="Normal")
ax.scatter(outliers.index, outliers.simple_return, color="red", label="Anomaly")
ax.set_title("Apple's stock returns")
ax.legend(loc="lower right")

plt.show()
