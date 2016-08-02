"""
MC1-P2: Optimize a portfolio.
http://quantsoftware.gatech.edu/MC1-Project-2
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    num_stocks = len(syms)
    initial_guess = [1.0 / num_stocks] * num_stocks # initially evenly split
    bounds = [(0.0, 1.0)] * num_stocks
    constraints = {'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs)}
    allocs = sp.minimize(min_sharpe_ratio, initial_guess, \
    args=prices, bounds=bounds, constraints=constraints).x
    # print(allocs + "\n\n\n")

    port_val, cr, adr, sddr, sr = assess_portfolio(allocs, prices)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_val / port_val.ix[0,:], prices_SPY / prices_SPY.ix[0,:]], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot()
        ax.set_title('Daily Portfolio Value and SPY')
        ax.set_ylabel('Price')
        ax.set_xlabel('Date')
        plt.grid(True)
        plt.show()

    return allocs, cr, adr, sddr, sr

def min_sharpe_ratio(allocs, prices):
    return -assess_portfolio(allocs, prices)[4]

def assess_portfolio(allocs, prices):
    # Get daily portfolio value
    normed = prices / prices.ix[0,:]
    alloced = normed * allocs
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

    # Sharpe Ratio, risk adjusted (0%) return
    sr = (adr - 0) / sddr
    sr *= 252**0.5 # adjustment for daily sampling (for annual measure)

    return port_val, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2004,12,1)
    end_date = dt.datetime(2006,5,31)
    symbols = ['YHOO', 'XOM', 'GLD', 'HNZ']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
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
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
