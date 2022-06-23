#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 14:47:21 2018

@author: dmitrijsokolov
"""


import pandas as pd
import numpy as np

df = pd.read_excel('Dataset_out5.xlsx')


df.dropna(subset=['Review clean'])

from sklearn.model_selection import train_test_split

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['Review clean'], 
                                                    df['Stars Positive'], 
                                                    random_state=0)


from sklearn.feature_extraction.text import CountVectorizer

# Fit the CountVectorizer to the training data
vect = CountVectorizer(stop_words=None, ngram_range=(1,2), analyzer='word').fit(X_train.values.astype('U'))

print(len(vect.get_feature_names()))

# transform the documents in the training data to a document-term matrix
X_train_vectorized = vect.transform(X_train.values.astype('U'))

X_train_vectorized

from sklearn.linear_model import LogisticRegression

# Train the model
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

from sklearn.metrics import roc_auc_score

# Predict the transformed test documents
predictions = model.predict(vect.transform(X_test.values.astype('U')))

print('AUC: ', roc_auc_score(y_test, predictions))


# get the feature names as numpy array
feature_names = np.array(vect.get_feature_names())

# Sort the coefficients from the model
sorted_coef_index = model.coef_[0].argsort()

# Find the 10 smallest and 10 largest coefficients
# The 10 largest coefficients are being indexed using [:-11:-1] 
# so the list returned is in order of largest to smallest
print('Smallest Coefs:\n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Largest Coefs: \n{}'.format(feature_names[sorted_coef_index[:-11:-1]]))

for num, pos in enumerate(model.predict(vect.transform(df.iloc[0:10]['Review']))):
    print(pos, num, df.iloc[num]['Review'])
#print(model.predict(vect.transform(df.iloc[0:10]['Review'])), df.iloc[0:10]['Review'])
