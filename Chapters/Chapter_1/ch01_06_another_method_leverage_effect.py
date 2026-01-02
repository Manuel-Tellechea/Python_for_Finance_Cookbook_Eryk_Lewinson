from tools.libs import *

# Download and preprocess the prices of the S&P 500 and VIX
df = yf.download(['^GSPC', '^VIX'],
start='1985-01-01',
end='2018-12-31',
progress=False)
df = df[['Close']]
df.columns = df.columns.droplevel(0)
df = df.rename(columns={'^GSPC': 'sp500', '^VIX': 'vix'})

# Calculate the log returns (we can just as well use percentage change-simple returns)
df['log_rtn'] = np.log(df.sp500 / df.sp500.shift(1))
df['vol_rtn'] = np.log(df.vix / df.vix.shift(1))
df.dropna(how='any', axis=0, inplace=True)

# Plot a scatterplot with the returns on the axes and fit a regression line to identify the trend
corr_coeff = df.log_rtn.corr(df.vol_rtn)
ax = sns.regplot(x='log_rtn', y='vol_rtn', data=df,
line_kws={'color': 'red'})
ax.set(title=f'S&P 500 vs. VIX ($\\rho$ = {corr_coeff:.2f})',
ylabel='VIX log returns',
xlabel='S&P 500 log returns')

plt.show()
