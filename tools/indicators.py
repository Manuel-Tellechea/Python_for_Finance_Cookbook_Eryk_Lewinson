from tools.libs import *

def realized_volatility(x):
    """
    Compute realized volatility as sqrt(sum(r_t^2)).
    Accepts a pandas Series or a 1-column DataFrame.
    Returns a single float.
    """
    if isinstance(x, pd.DataFrame):
        x = x.iloc[:, 0]
    x = pd.to_numeric(x, errors="coerce").dropna()
    return float(np.sqrt(np.sum(np.square(x.to_numpy()))))

def identify_outliers (row, n_sigmas=3):
    """
    Identifies outliers in a return distribution based on the sigma rule.

    An observation is classified as an outlier if its return exceeds
    the mean of the distribution by more than `n_sigmas` standard deviations,
    assuming an approximately normal distribution of returns.

    Parameters
    ----------
    row : pandas.Series
        A row containing the return value and its corresponding
        distribution statistics (mean and standard deviation).

    n_sigmas : int, optional
        The sigma threshold used to define an outlier.
        Default is 3.

    Returns
    -------
    int
        Binary flag indicating whether the observation is an outlier
        (1 = outlier, 0 = non-outlier).
    """
    x = row["simple_return"]
    mu = row["mean"]
    sigma = row["std"]
    if (x > mu + n_sigmas * sigma) or (x < mu - n_sigmas * sigma):
        return 1
    else:
        return 0

def print_descriptive_stats(series):
    """
        Displays descriptive statistics for a return time series.

        The summary includes measures of central tendency, dispersion,
        skewness, excess kurtosis, and the Jarque–Bera test for normality,
        providing a concise overview of the distributional characteristics
        of financial returns.

        Parameters
        ----------
        series : pandas.Series
            A datetime-indexed series of asset returns.

        Returns
        -------
        None
            The function outputs the statistics to standard output.
    """
    jb_stat, jb_pvalue = scs.jarque_bera(series)

    print(
        f"""
        ------------ Descriptive Statistics ------------
        Range of dates: {series.index.min().date()} - {series.index.max().date()}
        Number of observations: {series.count()}
        
        Mean: {series.mean(): .4f}
        Median: {series.median(): .4f}
        Min: {series.min(): .4f}
        Max: {series.max(): .4f}
        Standard Deviation: {series.std(): .4f}
        
        Skewness: {series.skew(): .4f}
        Kurtosis: {series.kurtosis(): .4f}
        
        Jarque-Bera statistic: {jb_stat: .2f} with p-value: {jb_pvalue: .2f}
        """
    )