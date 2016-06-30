"""
MC1-P1: Analyze a portfolio.
http://quantsoftware.gatech.edu/MC1-Project-1
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    normed = prices / prices.ix[0,:]
    alloced = normed * allocs * sv
    port_val = alloced.sum(axis=1)
    # .values to avoid alignment on index
    daily_rets = port_val[1:].values / port_val[:-1] - 1
    daily_rets = daily_rets[1:] # exclude day 1

    # Cumulative return
    cr = port_val[-1] / port_val[0] - 1

    # Average daily return
    adr = daily_rets.mean()

    # Standard deviation of daily return
    sddr = daily_rets.std()

    # Sharpe Ratio, risk adjusted return
    sr = (adr - rfr) / sddr
    sr *= sf**0.5 # adjustment for sampling (for annual measure)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_val / port_val.ix[0,:], prices_SPY / prices_SPY.ix[0,:]], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot()
        ax.set_ylabel('Normalised price')
        ax.set_xlabel('Date')
        plt.grid(True)
        plt.show()

    ev = port_val[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
