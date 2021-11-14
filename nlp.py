import nltk
from nltk import pos_tag as pos_tag_
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')


def tokenize(text):
    # This function takes a text and returns a list of tokens.
    return word_tokenize(text)


def pos_tag(tokens):
    # This functions takes a list of tokens and pos_tags each of them
    return pos_tag_(tokens)


def rm_stop_words(text):
    # this function removes the stop words from a text and return a list of tokens
    tokens = word_tokenize(text)
    tokens_without_sw = [word for word in tokens if not word in stopwords.words()]
    return tokens_without_sw


def bag_of_words(texts_arr):
    texts = texts_arr.split(';')
    words = []
    for i in range(len(texts)):
        for word in texts[i].split():
            if word.lower() not in words:
                words.append(word.lower())

    bow = [dict().fromkeys(words, 0) for x in range(len(texts))]
    for i, sentence in enumerate(texts):
        sentence_words = word_tokenize(sentence.lower())
        # frequency word count
        bag = bow[i]
        for sw in sentence_words:
            for word in words:
                if word == sw:
                    bag[word] += 1
    return bow

def lemmatization(texts):
    word_list = nltk.word_tokenize(texts)
    lemmatizer = WordNetLemmatizer()
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    
    return lemmatized_output

def stemming(sentence):
    ps = PorterStemmer()
    words = word_tokenize(sentence)
    stem_sentence =[]
    for word in words:
        stem_sentence.append(ps.stem(word))
        stem_sentence.append(" ")
        
    return "".join(stem_sentence)

def TfId(document):
    vectorizer = TfidfVectorizer()
    analyze = vectorizer.build_analyzer()
    analyze(document)
    res = vectorizer.get_feature_names()

    return res

# Term Frequency (TF) The number of times a word appears 
#in a document divded by the total number of words in the document.
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

#Inverse Data Frequency (IDF)
#The log of the number of documents divided 
#by the number of documents that contain the word w.
def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

def tfidf(documents):
    bagOfWords = documents.split(' ')
    uniqueWords = set(bagOfWords)
    numOfWords = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWords:
        numOfWords[word] += 1
    stopwords.words('english')
    tf = computeTF(numOfWords, bagOfWords)
    idfs = computeIDF([numOfWords])
    tfidf = computeTFIDF(tf, idfs)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([documents])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    return df.to_dict(orient='records')[0]


    

