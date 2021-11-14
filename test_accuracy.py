from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from collections import Counter
from nltk.tokenize import word_tokenize
import warnings
import pickle
#from sklearn import metrics

news = pd.read_csv('data.csv')

x_train, x_test, y_train, y_test = train_test_split( 
    news['text'], news['label'], test_size=0.1)

tfidf = TfidfVectorizer(stop_words='english', max_df=0.8)
x_train = tfidf.fit_transform(x_train)
x_test = tfidf.transform(x_test)


model = PassiveAggressiveClassifier(max_iter=300)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print("Accuracy of  :", accuracy_score(y_test, y_pred))

