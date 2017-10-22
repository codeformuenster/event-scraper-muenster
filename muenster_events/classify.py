"""Classify events to be relevant for families, or not."""

import model
import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn import model_selection
from nltk.stem.snowball import GermanStemmer

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
# remove stopwords and stem
stop = stopwords.words('german')
gs = GermanStemmer()
df['text'] = df['text'].str.split()
df['text'] = df['text'].apply(lambda x:
                              [gs.stem(i) for i in x if i not in stop])

# extract feature matrix and label vector
X = df['text'].str.join('|').str.get_dummies().add_prefix('word_')
y = df['label_family']

# test ft-idf
# v = TfidfVectorizer()
# X = pd.DataFrame(data=v.fit_transform(df['text']).toarray(),
#              columns=v.get_feature_names())

# define models
mnb = MultinomialNB()

# evaluate models
folds = y.loc[y == 1.0].size
cv = model_selection.cross_val_score(mnb, X, y, cv=folds, scoring='f1')
print('F1 score from CV: ')
print(cv.mean())
precision = model_selection.cross_val_score(mnb, X, y, cv=folds,
                                            scoring='precision')
print('Precision from CV: ')
print(precision.mean())
recall = model_selection.cross_val_score(mnb, X, y, cv=folds, scoring='recall')
print('Recall scores from CV: ')
print(recall.mean())

# predict on training data
fit = mnb.fit(X, y)
y_predict = fit.predict(X)
cfm = metrics.confusion_matrix(y, y_predict, labels=[1, 0])
print('confusion matrix (on training data):')
print(cfm)
f1 = metrics.f1_score(y, y_predict)
print('f1 score (on training data):')
print(f1)

# inspect probabilities per feature
df_weights = pd.DataFrame(data=fit.coef_, columns=X.columns).transpose()
df_weights.columns = ['score']

print(df_weights.sort_values('score'))
