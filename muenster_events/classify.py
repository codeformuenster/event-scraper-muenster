"""Classify events to be relevant for families, or not."""

import model
import re
import nltk
from nltk.corpus import stopwords

# load data
df = model.read_events_df()
df = df.dropna()

# PREPROCESSING
# all text in one column
df['text'] = df['title'] \
    + ' - ' + df['subtitle'] \
    + ' - ' + df['details']
df = df[['id', 'text', 'label_family']]
# process text
df['text'] = df['text'].map(lambda x: re.sub(r'\W+', ' ', x))
df['text'] = df['text'].str.lower()
# remove stopwords
stop = stopwords.words('german')
df['text'] = df['text'].str.split()
df['text'] = df['text'].apply(lambda x: [i for i in x if i not in stop])

# extract feature matrix and label vector
# TODO

# train model
# TODO

# evaluate metrics
# TODO
