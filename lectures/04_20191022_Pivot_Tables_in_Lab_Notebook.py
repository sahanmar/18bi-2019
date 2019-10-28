
# coding: utf-8

# # Lecture #4: Pivot Tables in a Lab Notebook
# 
# _October 22 2019_

# ## Why the notebook format (`*.ipynb`)?
# 
# The most important reasons are listed here: http://www.nature.com/news/interactive-notebooks-sharing-the-code-1.16261
# 
# Open this file locally in Jupyter.

# ## Excel tutorial example
# 
# See previous lecture notes for the context. Let's the import the data set again, directly from the Excel file to [pandas](https://pandas.pydata.org/):

# In[1]:

import pandas as pd


# In[2]:

xlsx = pd.read_excel('files/excel2016_intropivottables_practice.xlsx')


# Review the data frame:

# In[3]:

xlsx.info()


# In[4]:

xlsx.head()


# Example analysis:

# In[5]:

xlsx.pivot_table(
    index=['Salesperson'],
    columns=['Month'],
    values=['Order Amount'],
    aggfunc=sum
)


# Fixing months:

# In[6]:

xlsx['Month'] = xlsx['Month'].apply(lambda m: '{}_{}'.format(1 if m == 'January' else 2 if m == 'February' else 3, m))
xlsx.head()


# In[7]:

xlsx.pivot_table(
    index=['Salesperson'],
    columns=['Month'],
    values=['Order Amount'],
    aggfunc=sum
)


# Better way would be to treat it is properly as datetime, we could use the [to_datetime()](http://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.to_datetime.html) function.
# 
# What about plots?

# In[8]:

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

get_ipython().magic('matplotlib notebook')


# In[9]:

xlsx.pivot_table(
    index=['Month'],
    columns=['Salesperson'],
    values=['Order Amount'],
    aggfunc=sum
)['Order Amount'].plot(style='.-');


# ## Car mpg data set example
# 
# Downloaded from https://archive.ics.uci.edu/ml/datasets/Auto+MPG.
# 
# File preview (in bash):

# In[10]:

get_ipython().system('head files/auto-mpg.data.txt')


# Import the fixed width format:

# In[11]:

mpg = pd.read_fwf('files/auto-mpg.data.txt', 
                  na_values='?',  # see documentation
                  header=0, 
                  names=['mpg', 'cylinders', 'displacement', 'horsepower',
                         'weight', 'acceleration', 'model year', 'origin', 'car name'])
                  
mpg.info()


# In[12]:

mpg.head()


# Basic description:

# In[13]:

mpg.describe()


# Useful for quick frequency calculation:

# In[14]:

mpg['origin'].value_counts()


# In[15]:

mpg['cylinders'].value_counts().sort_index()


# ### Displacement (bins) vs horse power?

# In[16]:

import numpy as np


# Prepare the bins, as in the Excel groping:

# In[17]:

bin_size = 50
disp_min = mpg['displacement'].min()
disp_max = mpg['displacement'].max()
bins = [disp_min + bin_size * s for s in np.arange(np.ceil((disp_max - disp_min) / bin_size))]


# In[18]:

bins


# **Mean horse power by displacement bins**:

# In[19]:

hp = mpg.groupby(np.digitize(mpg['displacement'], bins))['horsepower'].mean()
hp


# **Linear regression**:

# In[20]:

import statsmodels.api as sm


# In[21]:

y = hp.values
y


# In[22]:

X = hp.index.values
X


# In[23]:

X = sm.add_constant(X)
X


# In[24]:

model = sm.OLS(y, X)
results = model.fit()


# In[25]:

results.params


# In[26]:

print(results.summary())


# See more on [OLS](http://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html).

# ## Assignment
# 
# 1. Do similar analysis on your own data set
# 2. Use [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling) to inspect the data set
