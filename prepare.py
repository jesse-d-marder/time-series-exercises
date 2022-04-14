import acquire
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

def prepare_store(df):
    """Takes in store data as pandas dataframe, prepares it, and returns cleaned dataframe"""
    
    # Convert sale date to datetime and set as index. Time portion not needed. Splitting like this and specifying format speeds it up.
    df.sale_date = pd.to_datetime(df.sale_date.str.split(' 00:00:00 GMT').str[0].str.split(', ').str[1],format='%d %b %Y')

    df= df.set_index('sale_date').sort_index()
    
    # Create month and day of week columns
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_of_week
    
    # Calculate total sale amount ($$), sale quantity(amount) * item price
    df['sales_total'] = df.sale_amount*df.item_price
    
    df = df.rename(columns = {'sale_amount':'quantity'})
    
    
    return df

def prepare_power(df):
    """Takes in OPS data as pandas dataframe, prepare it, and returns cleaned dataframe"""
    
    # Convert date to datetime and set as index
    df.index = pd.to_datetime(df.Date)

    df= df.sort_index()

    df['month'] = df.index.month
    df['year'] = df.index.year
    
    df.columns = [col.replace('+','_').lower() for col in df.columns]
    
    # Fill in null values with 0 - mostly from early years presumably when no alternative energy?
    df = df.fillna(0)
    
    return df