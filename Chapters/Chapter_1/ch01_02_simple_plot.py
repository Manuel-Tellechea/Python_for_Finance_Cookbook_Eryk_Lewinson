from IPython.core.pylabtools import figsize
from matplotlib.pyplot import title, xlabel

from tools.libs import *

# ---------------------------------------------------------
# Download the data and keep the adjusted close prices only
# ---------------------------------------------------------
df = yf.download('MSFT', start='1950-01-01', end='2025-12-28', progress=False)

# NOTE:
# In recent versions of yfinance, prices are auto-adjusted by default.
# Therefore, the 'Close' column already represents adjusted close prices
# (equivalent to 'Adj Close' in older versions and in the book).
df = df.loc[:, ["Close"]].rename(columns={"Close": "close"})

# Ensure the index is of datetime type
df.index = pd.to_datetime(df.index)

# ---------------------------------------------------------
# Calculate simple and log returns using adjusted close prices
# ---------------------------------------------------------
df['simple_rtn'] = df['close'].pct_change()
df["log_rtn"] = np.log(df["close"] / df["close"].shift(1))
df = df.dropna()

# The plot method of pandas
fig, ax = plt.subplots(3, 1, figsize=(24, 20), sharex=True)

df.close.plot(ax=ax[0])
ax[0].set(title='MSFT time series', ylabel='Stock price ($)')

df.simple_rtn.plot(ax=ax[1])
ax[1].set(ylabel='Simple returns (%)')

df.log_rtn.plot(ax=ax[2])
ax[2].set(xlabel='Date', ylabel='Log returns (%)')

plt.tight_layout()
plt.show()