from tools.libs import *
from tools.indicators import print_descriptive_stats

# ---------------------------------------------------------
# Download the data and keep the close prices only
# ---------------------------------------------------------
df = yf.download("MSFT", period="max", auto_adjust=True, progress=False)
df = df.loc[:, ["Close"]].rename(columns={"Close": "close"})

# Ensure the index is of datetime type
df.index = pd.to_datetime(df.index)

# yfinance returns a MultiIndex even for a single ticker in some setups.
# Example: MultiIndex([('adj_close','MSFT')], names=['Price','Ticker'])
# Extract the price series explicitly and rebuild a "flat" dataframe.
price = df[("close", "MSFT")].copy()
price.name = "Price"

df = pd.DataFrame({"Price": price})

# ---------------------------------------------------------
# 2) Compute returns (simple and log)
# ---------------------------------------------------------
df["simple_return"] = df["Price"].pct_change()
df["log_return"] = np.log(df["Price"] / df["Price"].shift(1))

# Optional: drop NaNs only for returns plotting (keeps price intact)
returns_df = df[["simple_return", "log_return"]].dropna()
log_ret = returns_df["log_return"]

# ---------------------------------------------------------
# 1) Non-Gaussian distribution of returns
# ---------------------------------------------------------
# Calculate the normal Probability Density Function (PDF) using the mean and \\
# standard deviation of the observed returns
r_range = np.linspace(log_ret.min(), log_ret.max(), num=1000)
mu = log_ret.mean()
sigma = log_ret.std()
norm_pdf = scs.norm.pdf(r_range, loc=mu, scale=sigma)

# Plot the histogram and the Q-Q plot
fig, ax = plt.subplots(1, 3, figsize=(16, 8))

# histogram
sns.histplot(
    log_ret,
    stat="density",
    bins=100,
    ax=ax[0]
)
ax[0].set_title("Distribution of MSFT returns", fontsize=16)
ax[0].plot(
    r_range,
    norm_pdf,
    "g",
    lw=2,
    label=f"N({mu:.4f}, {sigma**2:.6f})"
)
ax[0].legend(loc="upper left")

# Q-Q plot
sm.qqplot(log_ret.values, line="s", ax=ax[1])
ax[1].set_title("Q-Q plot", fontsize=16)

# ---------------------------------------------------------
# 2) Volatility clustering
# ---------------------------------------------------------
# Visualize the log returns series
log_ret.plot(title='Daily MSFT returns')

# ---------------------------------------------------------
# 3) Absence of autocorrelation in returns
# ---------------------------------------------------------
# Define the parameters for creating the autocorrelation plots
N_LAGS = 50
SIGNIFICANCE_LEVEL = 0.05

# create the autocorrelation function (ACF) plot of log returns
acf = smt.graphics.plot_acf(log_ret,
lags=N_LAGS,
alpha=SIGNIFICANCE_LEVEL)

# ---------------------------------------------------------
# 4) Small and decreasing autocorrelation in squared/absolute returns
# ---------------------------------------------------------
# Create the ACF plots
fig1, ax = plt.subplots(2, 1, figsize=(12, 10))
smt.graphics.plot_acf(log_ret ** 2, lags=N_LAGS,
alpha=SIGNIFICANCE_LEVEL, ax = ax[0])
ax[0].set(title='Autocorrelation Plots',
ylabel='Squared Returns')
smt.graphics.plot_acf(np.abs(log_ret), lags=N_LAGS,
alpha=SIGNIFICANCE_LEVEL, ax = ax[1])
ax[1].set(ylabel='Absolute Returns',
xlabel='Lag')

# ---------------------------------------------------------
# 5) Leverage effect
# ---------------------------------------------------------
# Calculate volatility measures as rolling standard deviations
moving_std_252 = log_ret.rolling(window=252).std()
moving_std_21 = log_ret.rolling(window=21).std()

fig2, ax = plt.subplots(3, 1, figsize=(18, 15), sharex=True)

df.Price.plot(ax=ax[0])
ax[0].set(title='MSFT time series', ylabel='Stock price ($)')

log_ret.plot(ax=ax[1])
ax[1].set(ylabel='Log returns (%)')

moving_std_252.plot(ax=ax[2], color='r',
label='Moving Volatility 252d')

moving_std_21.plot(ax=ax[2], color='g',
label='Moving Volatility 21d')

ax[2].set(ylabel='Moving Volatility',
xlabel='Date')

ax[2].legend()

# Summary Statistics
print_descriptive_stats(log_ret)

plt.tight_layout()
plt.show()