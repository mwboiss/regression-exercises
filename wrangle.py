import pandas as pd
from env import get_db_url
import os
import warnings
warnings.filterwarnings('ignore')

def get_zillow_data(use_cache=True):
    # Assign filename
    filename = 'zillow.csv'
    
    # Check if file exists
    if os.path.exists(filename) and use_cache:
        print('Using cached csv file...')
        return pd.read_csv(filename)
    
    # Notify user of next step
    print('Getting a fresh copy from the database...')
    
    # Assign url
    url = get_db_url('zillow_db')
    
    # Run query for data
    zillow_data = pd.read_sql('''
    SELECT bedroomcnt,\
    bathroomcnt,\
    calculatedfinishedsquarefeet,\
    taxvaluedollarcnt,\
    yearbuilt,\
    taxamount,\
    fips
    FROM properties_2017
    LEFT JOIN propertylandusetype
    USING(propertylandusetypeid)
    WHERE propertylandusetypeid = 261 OR propertylandusetypeid = 279
    ''', url)
    
    # Notify user of next step
    print('Saving to csv...')
    
    # Create csv
    zillow_data.to_csv(filename, index=False)
    
    # Return DataFrame
    return zillow_data

def wrangle_zillow():
    '''
    function used to wrangle zillow data
    '''
    # Get Zillow data
    zillow = get_zillow_data()
        
    # Rename columns
    zillow = zillow.rename(columns={'bedroomcnt' : 'bedrooms',\
                                'bathroomcnt' : 'bathrooms',\
                                'finishedsquareft' : 'area',\
                                'taxvaluedollarcnt' : 'taxable_value',\
                                'yearbuilt' : 'year_built',\
                                'taxamount' : 'tax_amount',\
                                'fips' : 'county'})
    
    # Drop Nulls
    zillow = zillow.dropna()
    
    # Map county values to name of county
    zillow.county = zillow.county.map({6037.0 : 'los_angeles_ca',\
                                       6059.0 : 'orange_ca',\
                                       6111.0 : 'ventura_ca'})
    
    
    # One hot encode county 

    # Get dummy variables
    dummy_name = pd.get_dummies(zillow[['county']])

    # Concat dummy_name to dataframe
    zillow = pd.concat([zillow,dummy_name],axis=1)
    
    return zillow

def scale_data(train, validate, test, return_scaler=False):
    '''
    This function scales the split data and returns a scaled version of the dataset.
    
    If return_scaler is true, the scaler will be returned as well.
    '''
    
    col = x_train_scaled.columns[x_train_scaled.dtypes == 'float']

    train_scaled = train
    validate_scaled = validate
    test_scaled = test

    scaler = sklearn.preprocessing.MinMaxScaler()
    scaler.fit(train[col])
    
    train_scaled[col] = scaler.transform(train[col])
    validate_scaled[col] = scaler.transform(validate[col])
    test_scaled[col] = scaler.transform(test[col])
    
    if return_scaler:
        return train_scaled, validate_scaled, test_scaled, scaler
    else:
        return train_scaled, validate_scaled, test_scaled