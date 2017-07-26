import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(200,'ecece9102a06a5925eab8542ca26a02ec74fca53f31672f58dd0aaad')

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d200/ecece9102a06a5925eab8542ca26a02ec74fca53f31672f58dd0aaad.csv')

df.sort(['Date']).head()

df['Year'], df['Month-Date'] = zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))
df = df[df['Month-Date'] != '02-29']

df['Year'].unique()

import numpy as np
temp_min_day = df.loc[df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Date')["Data_Value"].idxmin()]
temp_max_day = df.loc[df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Date')["Data_Value"].idxmax()]

temp_min_record_05_to_14 = df.loc[df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-Date')["Data_Value"].idxmin()]
temp_max_record_05_to_14 = df.loc[df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-Date')["Data_Value"].idxmax()]

temp_min_15 = df.loc[df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-Date')["Data_Value"].idxmin()]
temp_max_15 = df.loc[df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-Date')["Data_Value"].idxmax()]

temp_min_record_05_to_14 = temp_min_record_05_to_14.reset_index(drop=True)
temp_min_15 = temp_min_15.reset_index(drop=True)
temp_min_record_05_to_14['2015'] = temp_min_15['Data_Value']
temp_max_record_05_to_14 = temp_max_record_05_to_14.reset_index(drop=True)
temp_max_15 = temp_max_15.reset_index(drop=True)
temp_max_record_05_to_14['2015'] = temp_max_15['Data_Value']

record_min = temp_min_record_05_to_14[temp_min_record_05_to_14['Data_Value'] > temp_min_record_05_to_14['2015']]
record_max = temp_max_record_05_to_14[temp_max_record_05_to_14['Data_Value'] < temp_max_record_05_to_14['2015']]

plt.figure()
fig, ax = plt.subplots()
fig = plt.gcf()
fig.set_size_inches(10.5, 6.5)
plt.plot(temp_max_record_05_to_14['Data_Value'], '#e89278', label = 'record high between 2005-2014')
plt.plot(temp_min_record_05_to_14['Data_Value'], '#479ee0', label = 'record low between 2005-2014')
plt.scatter(record_max.index.values, record_max['Data_Value'].values, s = 15, c = '#0f381c', label = 'broken record from year 2015')
plt.scatter(record_min.index.values, record_min['Data_Value'].values, s = 15, c = '#0f381c')
plt.gca().axis([-5, 370, -200, 450])
plt.xticks(range(0, len(temp_min_record_05_to_14), 20), temp_min_record_05_to_14.index[range(0, len(temp_min_record_05_to_14), 20)], rotation = '45')
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
ax.xaxis.labelpad = 20
plt.title('Temperature Summary Plot near Grez-Doiceau')
plt.legend(loc = 2, frameon = False)
plt.gca().fill_between(range(len(temp_min_record_05_to_14)), temp_min_record_05_to_14['Data_Value'], temp_max_record_05_to_14['Data_Value'], facecolor = '#d2d7db', alpha = 0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()