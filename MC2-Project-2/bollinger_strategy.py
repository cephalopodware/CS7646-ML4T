# http://quantsoftware.gatech.edu/MC2-Project-2
"""
Bollinger Bands are two standard deviations from a moving average
Overbought when moving closer to upper band
Oversold when lower band
Using 20 days here
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

def chart():
	# Print bands, and entry/exit points

	dates = pd.date_range(dt.datetime(2007, 12, 31), dt.datetime(2009, 12, 31))
	syms = ['IBM']
	# Drop non-trading days
	df = get_data(syms, dates, addSPY = False).dropna()

	# Drop first 19 days
	df['SMA'] = pd.rolling_mean(df['IBM'], window=20)

	df['Upper'] = df['SMA'] + pd.rolling_std(arg=df['IBM'], window=20)*2
	df['Lower'] = df['SMA'] - pd.rolling_std(arg=df['IBM'], window=20)*2


	# TODO: long entries as a vertical green line
	long_entries = pd.Series()

	last_row = None
	# for i, row in df.iterrows():

	"""

	TODO: long exits as a vertical black line

	TODO: short entries as a vertical red line

	TODO: short exits as a vertical black line

	Single asset portfolio, 100 shares

	"""
	ax = df.plot(title="Bollinger Bands", fontsize=12)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	plt.show()

if __name__ == "__main__":
	chart()