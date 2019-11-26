#!/usr/bin/env python
# coding: utf-8

# # Prediction of The Tempriture With Respect to Time Series

# ### Libraries Import 

# In[1]:


import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np

from fbprophet import Prophet


# ### Path to an Excel Document With Data

# In[2]:


path = "/Users/mark/Documents/Datasets/Time_series/mean-daily-temperature-fisher-river.xlsx"


# ### Data Reformatting and Plotting

# In[3]:


df = pd.read_excel(path)


# In[4]:


df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values('Date', ascending=True)


# In[5]:


df


# ### Plotting

# In[6]:


py.iplot([go.Scatter(
    x=df['Date'], 
    y=df['Mean_Temperature']
)])


# ## Modelling Time Series

# ### Splitting the Data on Training and Testing

# In[7]:


df_prophet = pd.DataFrame(df)
df_prophet.columns = ['ds', 'y']

splitting_index = int(np.floor(len(df_prophet)*0.7))

train_df_prophet = df_prophet[:splitting_index]
testing_df_prophet = df_prophet[splitting_index:]


# ### Crearing a Model, Testing and Predicting 

# In[8]:


model = Prophet()
model.fit(train_df_prophet)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(testing_df_prophet)
forecast


# ## Plot the Predicted Results

# In[9]:


py.iplot([
    go.Scatter(x=testing_df_prophet['ds'], y=testing_df_prophet['y'], name='y'),
    go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='yhat'),
    go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='none', name='upper'),
    go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='none', name='lower'),
    go.Scatter(x=forecast['ds'], y=forecast['trend'], name='Trend')
])


# In[ ]:




