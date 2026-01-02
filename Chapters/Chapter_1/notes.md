## Chapter 1 – Data Handling & Visualization

- yfinance may return MultiIndex even for single tickers
- Always enforce datetime index
- Prefer log-returns for further chapters
- Plotly useful for exploratory analysis, not production
- Stylized facts are statistical properties that appear to be present in many empirical asset
returns (across time and markets). It is important to be aware of them because when we are
building models that are supposed to represent asset price dynamics, the models must be
able to capture/replicate these properties.
  - Non-Gaussian distribution of returns
  - Volatility clustering
  - Autocorrelation
  - Small and decreasing autocorrelation in squared/absolute returns
  - Leverage effect