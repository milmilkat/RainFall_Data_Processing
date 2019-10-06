import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from prettytable import PrettyTable
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams["figure.figsize"] = (30, 9)

def load_data(address):
   """Gets a string address and loads the data"""
   if(address.endswith('.csv')):
      return pd.read_csv(address)
   else:
      raise Exception("data type is not defined yet")
   
def de_accumulate(data):
   """De-accumulates the data. In other words, fills in the not inserted rows with value zero"""
   for i in range(1, len(data)):
      diff = data.iloc[i][0] - data.iloc[i-1][0]
      if diff > 86400:
         for j in range(1, (diff/86400).astype(int)):
            row = pd.DataFrame({'unixdatetime':int(data.iloc[i-1][0] + 86400 * j),'value':0,'normaltime':__time_converter(int(data.iloc[i-1][0] + 86400 * j))}, index=[i-0.5+0.0001*j])
            data = data.append(row, ignore_index=False)
   data = data.sort_index().reset_index(drop=True)
   return data
   
def __time_converter(timestamp):
   """Converts unix datetime to human datetime"""
   return datetime.fromtimestamp(timestamp)

def __add_normal_datetime(data):
   """Adds a new column to the DataFrame representing the human datetime"""
   mapped_data = list(map(__time_converter, data.unixdatetime))
   data['normaltime'] = mapped_data
   return data
   
def plot_size(x, y):
   """Changing the size of the plots"""
   plt.rcParams["figure.figsize"] = (x, y)
   
def show_data(data, show_table= True, show_plot= True, plt_size= (30,10), with_top= False, top= 0.5):
   """plots and prints the data"""
   data = __add_normal_datetime(data)
   t_data = pd.DataFrame()
   if with_top:
      t_data = top_data(data, 1-top)
   if show_table:
      pt = PrettyTable()
      pt.field_names = ["time(datetime)","rainfall(inch)"]
      if with_top:
         for i in range(len(t_data)):
            pt.add_row([t_data.iloc[i][2],t_data.iloc[i][1]])
         print(pt)
      else:
         for i in range(len(data)):
            pt.add_row([data.iloc[i][2],data.iloc[i][1]])
         print(pt)
   if show_plot:
      plot_size = plt_size
      plt.bar(data.normaltime, data.value)
      if with_top:
         plt.bar(t_data.normaltime, t_data.value, color= 'r')
      plt.xlabel("time (datetime)", fontsize=18)
      plt.ylabel("rainfall (inch)",fontsize=16)
      plt.show()
   
def top_data(data, top= 0.5):
   return data[data.value >= data.value.quantile(1-top)]
   
def save_data(data, peak= 0.5, address= "output.csv"):
   data = top_data(data, top= peak)
   data = data.drop('normaltime', axis= 1)
   if(address.endswith('.csv')):
      data.to_csv(address)
   else:
      Exception("name of the file does not have .csv")
   
