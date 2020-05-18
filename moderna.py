
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('fivethirtyeight')

start = dt.datetime(2020, 1, 1)
end = dt.datetime(2020, 5, 15)

df = web.DataReader('MRNA', 'yahoo', start, end)
print(df.head())

#Add the file path
df.to_csv('/Users/rickvillanueva/Documents/VIG/Models/moderna.csv')

#Import the created csv file
moderna_data = pd.read_csv('moderna.csv')
moderna_data = pd.read_csv('moderna.csv', parse_dates = True, index_col = 0)

#Check the behavior of the file
plt.head(moderna_data)

#Graph
df.plot() #Add the columns to graph
plt.show()

# Si quisieramos graficar solo una o varias columnas
df['Open'].plot()
plt.show()

df[['Low', 'High']].plot()
plt.show()

"""
Ejercicio 3:

    Manipulación básica de datos de los datos de stock.

"""

# Crear una columna para medias móviles:

df['100ma'] = df['Adj Close'].rolling(window = 100).mean()

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()

# Dibujar un OHLC (Open-High-Low-Close Chart)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

print(df_ohlc.head()) # veamos como queda la serie y el dataframe

# reindexar el dataframe:
df_ohlc.reset_index(inplace = True)
print(df_ohlc.head()) # veamos la diferencia en la numeración a la izquierda del DF con la reindexación

# hay que importar nuevas bibliotecas:
import matplotlib.dates as mdates

# convertir las fechas a números
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head()) # veamos la diferencia en la columna fecha, ahora sale como un número secuencial

# el módulo finance de matplotlib ya fue depreciado, en la consola hay que instalar: pip install mpl_finance
from mpl_finance import candlestick_ohlc

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
