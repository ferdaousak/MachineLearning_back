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

warnings.filterwarnings('ignore')

#l'entrainement de model
def train_model():
    #our data for training
    data = pd.read_csv('data.csv')
    x_train, x_test, y_train, y_test = train_test_split(
        data['text'], data['label'], test_size=0.1)
    #pour vectorizer les donneés pour mieux entrainement
    tfidf = TfidfVectorizer(stop_words='english', max_df=0.8)
    x_train = tfidf.fit_transform(x_train)
    x_test = tfidf.transform(x_test)
    #l'appel de generation d'un fichier bin pour eviter la répetition d'appel de fonction
    with open("tfidf.bin", 'wb') as f_out:
        pickle.dump(tfidf, f_out)
        f_out.close()
    #notre model a choix de 70% accuracy
    model = PassiveAggressiveClassifier(max_iter=300)
    model.fit(x_train, y_train)
    return model

#la prediction des article ajouter par l'utilisateur
def predict_article(article):
    with open('fakenews_model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
    with open('tfidf.bin', 'rb') as f_in:
        tfidf = pickle.load(f_in)

    x = tfidf.transform([article])
    return model.predict(x)[0]
