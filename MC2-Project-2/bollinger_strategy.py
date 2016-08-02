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
import csv

def chart():
	# Print bands, and entry/exit points

	dates = pd.date_range(dt.datetime(2007, 12, 31), dt.datetime(2009, 12, 31))
	syms = ['IBM']
	# Drop non-trading days
	df = get_data(syms, dates, addSPY = False).dropna()

	df['SMA'] = pd.rolling_mean(df['IBM'], window=20)
	df['Upper'] = df['SMA'] + pd.rolling_std(arg=df['IBM'], window=20)*2
	df['Lower'] = df['SMA'] - pd.rolling_std(arg=df['IBM'], window=20)*2

	# Generate plot first so we can add vertical lines below
	ax = df.plot(color=["Blue", "Gold", "Cyan", "Cyan"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	lines, labels = ax.get_legend_handles_labels()
	ax.legend([lines[0], lines[1], lines[2]], ["IBM", "SMA", "Bollinger Bands"])

	# Generate orders CSV to put in market simulator
	csvfile = open('order.csv', 'a+')
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(('Date', 'Symbol', 'Order', 'Shares'))

	# Max one position at a time
	longPosition = False
	shortPosition = False

	last_row = pd.Series()	
	for i, row in df.iterrows():
		if last_row.empty == False:
			# Long exit when prive moves from below SMA to above
			if last_row['IBM'] < last_row['SMA'] and row['IBM'] > row['SMA']:
				if longPosition == True:
					ax.axvline(x=row.name, color='Black')
					writer.writerow((row.name, 'IBM', 'SELL', 100))
					longPosition = False
			# Short exit when price moves from above SMA to below
			elif last_row['IBM'] > last_row['SMA'] and row['IBM'] < row['SMA']:
				if shortPosition == True:
					ax.axvline(x=row.name, color='Black')
					writer.writerow((row.name, 'IBM', 'BUY', 100))
					shortPosition = False

			# Long entry when price moves from below lower band to above lower band
			if last_row['IBM'] < last_row['Lower'] and row['IBM'] > row['Lower']:
				if longPosition == False and shortPosition == False:
					ax.axvline(x=row.name, color='Green')
					writer.writerow((row.name, 'IBM', 'BUY', 100))
					longPosition = True
			# Short entry when prices moves from above upper band below upper band
			elif last_row['IBM'] > last_row['Upper'] and row['IBM'] < row['Upper']:
				if longPosition == False and shortPosition == False:
					ax.axvline(x=row.name, color='Red')
					writer.writerow((row.name, 'IBM', 'SELL', 100))
					shortPosition = True
			
		last_row = row

	csvfile.flush() # Finish writing to disk
	csvfile.close()
	plt.show()

if __name__ == "__main__":
	chart()