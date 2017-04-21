# We Need to download full europarl at http://nltk.ldc.upenn.edu/packages/corpora/europarl_raw.zip

# ~$ python3 train.py europarl_raw

import os
import re
import argparse
import pickle

from os import listdir

from os.path import isfile, join

from tqdm import tqdm

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

## CLI definition
parser = argparse.ArgumentParser(description='Train model for document classification')
parser.add_argument('dataset', metavar='D', type=str, help='Folder containing the documents within the subfolders')
args = parser.parse_args()
##

def clean_new_line_if_exist(languages):
    result = list()
    for lang in languages:
        result.append(lang.rstrip())
    return tuple(result)

def find_files(data_path):
    files = dict()
    languages = [d for d in listdir(data_path) if not d.startswith('.')]
    for lang in languages:
        files[lang] = [f for f in listdir('%s/%s/'%(data_path,lang)) if not f.startswith('.')]
        print("%s : %i ficheros" %(lang,len(files[lang])))
    return files

def get_words(text):
    """
    Filter out words from text.
    Returns string with only words separated by spaces.
    """
    words = re.compile('\w+').findall(text)
    return ' '.join(words)

def parse_files(data_path):
    """
    Create list with only words string documents and another one
    with its languages.
    X_set: list of strings representing full documents.
    y_set: list of languages.
    """
    X_set = list()
    y_set = list()
    languages = [d for d in listdir(data_path) if not d.startswith('.')]
    for lang in languages:
        files = [f for f in listdir('%s/%s/'%(data_path,lang)) if not f.startswith('.')]
        for fil in tqdm(files):
            with open('%s/%s/%s'%(data_path, lang, fil)) as f:
                words = get_words(f.read())
                X_set.append(words)
                y_set.append(lang)
    return X_set,y_set

if __name__ == "__main__":

    #Find and Report
    languages = list(open('languages.txt','r'))[0].rstrip().split(',') #Remove \n
    
    files = find_files(args.dataset)

    #Get dataset
    X_train, y_train = parse_files(args.dataset)

    pipe = Pipeline([
        ('vectorizer', TfidfVectorizer(stop_words=stopwords.words('english'), min_df=0)),
        ('classifier', MultinomialNB(alpha=0.0005)),
    ])

    model = pipe.fit(X_train,y_train)

    with open('model.pickle', 'wb') as f:
        pickle.dump(pipe, f, protocol=3)