"""
MC2-P1: Market simulator.
http://quantsoftware.gatech.edu/MC2-Project-1
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders = orders.sort_index() # Not all orders ordered by date

    syms = orders['Symbol'].drop_duplicates()
    dates = pd.date_range(orders.index.values[0], orders.index.values[-1])
    # Only SPX trading days (for the empty portfolio DataFrame)
    dates = get_data(['$SPX'], dates).index
    prices = get_data(syms, dates, False)

    cash = start_val

    # Build portfolio DataFrame
    cols = syms
    cols['Cash'] = 'Cash'
    cols['Value'] = 'Value'
    portfolio = pd.DataFrame(index=dates, columns=cols).fillna(value=0.0)
    portfolio['Cash'].iloc[0] = cash

    o = 0 # Current order index
    # For each date in the portfolio tracking range
    for p in range(0, len(portfolio.index)):
        if p > 0: # Forward fill
            portfolio.iloc[p] = portfolio.iloc[p-1]

        date = portfolio.index[p]

        # Process orders
        while o < len(orders.index) and orders.index[o] == date:
            sym = orders['Symbol'][o]
            q = orders['Shares'][o]
            if orders['Order'][o] == 'SELL':
                q = -q
            cash_spent = q * prices[sym].loc[date]
            """
            200% leverage limit check goes here
            leverage = (sum(longs) + sum(abs(shorts))) / (sum(longs) - sum(abs(shorts)) + cash)
            Skipped extra credit section
            """
            # Update portfolio with order quantity
            portfolio[sym][p] += q
            cash -= cash_spent
            o += 1

        # Update portfolio value
        value = cash
        # For each stock symbol (last 2 rows are 'Cash' and 'Value')
        for sym, q in portfolio.ix[p, 0:-2].iteritems():
            value += prices[sym].loc[date] * q
        portfolio['Cash'][p] = cash
        portfolio['Value'][p] = value

    # portfolio.to_csv('out.csv')
    # print(portfolio)
    return portfolio['Value']

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/mc2p2.csv"
    sv = 10000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    start_date = portvals.index[0]
    end_date = portvals.index[-1]

    dates = pd.date_range(start_date, end_date)
    spx = get_data(['$SPX'], dates).ix[:,'$SPX']

    """
    # Plot for MC2-Project-2
    ax = (portvals/portvals[0]).plot()
    ax = (spx/spx[0]).plot()
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalised price")
    ax.legend(['Portfolio', '$SPX'])
    ax.set_title("Simple Bollinger Bands strategy vs. SPX")
    plt.show()
    """

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_portfolio(portvals)
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = assess_portfolio(spx)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX : {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX : {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX : {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

def assess_portfolio(port_val):
    # .values to avoid alignment on index
    daily_rets = port_val[1:].values / port_val[:-1] - 1
    # Line below commented out to match test case answers
    # daily_rets = daily_rets[1:] # exclude day 1

    # Cumulative return
    cr = port_val[-1] / port_val[0] - 1

    # Average daily return
    adr = daily_rets.mean()

    # Standard deviation of daily return
    sddr = daily_rets.std()

    # Sharpe Ratio, risk adjusted (0%) return
    sr = (adr - 0) / sddr
    sr *= 252**0.5 # adjustment for daily sampling (for annual measure)

    return cr, adr, sddr, sr

if __name__ == "__main__":
    test_code()
