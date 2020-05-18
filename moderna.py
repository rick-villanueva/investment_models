#Import libraries
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
from matplotlib import style
from mpl_finance import candlestick_ohlc

style.use('fivethirtyeight')

start = dt.datetime(2020, 1, 1)
end = dt.datetime(2020, 5, 15)

df = web.DataReader('MRNA', 'yahoo', start, end)
print(df.head())

#Add the file path
df.to_csv('/Users/rickvillanueva/Documents/VIG/Models/moderna.csv')

#Import the created csv file
moderna_data = pd.read_csv('moderna.csv')
moderna_data = pd.read_csv('moderna.csv', parse_dates = False, index_col = 0)

#Check the behavior of the file
print(moderna_data.head())
moderna_data.info()

#Graph (from the dataframe and not the csv)
df.plot() #Add the columns to graph
plt.show()
plt.clf()
#Graph certain columns (from the dataframe and not the csv)
df['Open'].plot()
plt.show()
plt.clf()

df[['Low', 'High']].plot()
plt.show()
plt.clf()


#Creating a column for mean
df['100ma'] = df['Adj Close'].rolling(window = 100).mean()

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
plt.clf()

#Graph (Open-High-Low-Close Chart)
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

print(df_ohlc.head())

#Reindex dataframe 
df_ohlc.reset_index(inplace = True)
print(df_ohlc.head())

#Convert date to number
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head())


ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
