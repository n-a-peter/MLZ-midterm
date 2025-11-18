#!/usr/bin/env python
# coding: utf-8



# load important libraries

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.model_selection import train_test_split
#from sklearn.model_selection import KFold
from sklearn.feature_extraction import DictVectorizer
#from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier 
#from sklearn.tree import export_text
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import roc_auc_score
#from sklearn.metrics import mutual_info_score
from sklearn.pipeline import make_pipeline

#get_ipython().system('pip install tqdm')
from tqdm.auto import tqdm

import pickle

# Read the data from the csv file into a dataframe
df = pd.read_csv('loan_approval_dataset.csv')

# Edit column names to remove the spaces before the column names

df.columns = df.columns.str.lower().str.replace(' ','')

# loan_id is redundant and can be deleted
df.tail()

# loan_id is a redudntant column so we can delete it

del df['loan_id']

# Get the names of the numerical features and the categorical features

categorical = list(df.dtypes[df.dtypes=='object'].index)
categorical

numerical = list(df.dtypes[df.dtypes!='object'].index)
numerical

# Examine the values of the categorical

# First remove the spaces in 'Not Graduate'
df['education'] = df['education'].str.replace(' Not ', ' Not_')

# Continue editing the values of the categorical to remove the remaining extra spaces
for value in categorical:
    df[value] = df[value].str.lower().str.replace(' ','')

for value in categorical:
    print(df[value].value_counts().index)

# Convert the target variable to numerical

df['loan_status'] = (df['loan_status'] == 'approved').astype(int)

# Update the new categorical variables to exclude the target variable
categorical = categorical[:-1]

# Split the data into train, validation and test sets (60%, 20%, 20%)

df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

df_train, df_val = train_test_split(df_full_train, test_size=0.25, shuffle=False)

# Retreive the values of the target variable
y_full_train = df_full_train.loan_status.values
y_train = df_train.loan_status.values
y_val = df_val.loan_status.values
y_test = df_test.loan_status.values

# Delete the target variable from the dataframes
#del df_full_train['loan_status']
del df_train['loan_status']
del df_val['loan_status']
del df_test['loan_status']

# Training the model
# One-hot encoding
dv = DictVectorizer(sparse=False)

train_dict = df_train.to_dict(orient='records')
X_train = dv.fit_transform(train_dict)

val_dict = df_val.to_dict(orient='records')
X_val = dv.transform(val_dict)

test_dict = df_test.to_dict(orient='records')
X_test = dv.transform(test_dict)

# MODEL TRAINING
### Decision Tree Classifier

del df_full_train['loan_status']

# Final model
# Best model is the Decision Tree classifier with max_depth=4, resulting in roc_auc_score=0.997 and rmse=0.14

full_train_dict = df_full_train.to_dict(orient='records')
X_full_train = dv.fit_transform(full_train_dict)

pipeline = make_pipeline(
    DictVectorizer(),
    DecisionTreeClassifier(max_depth = 4, random_state=1)
)

pipeline.fit(full_train_dict, y_full_train)

y_pred = pipeline.predict_proba(test_dict)[:,1]

#auc = roc_auc_score(y_test, y_pred)
#rmse(y_test, y_pred)

with open('model.bin', 'wb') as f_out:
    pickle.dump(pipeline, f_out)

