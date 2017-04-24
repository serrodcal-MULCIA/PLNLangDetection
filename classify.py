# ~$ python3 classify.py model.pickle languages.txt ./wikipedia/

import os
import re
import argparse
import pickle
import random
import nltk

from os import listdir

from tqdm import tqdm

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from nltk.metrics import ConfusionMatrix

def get_directories(data_path, languages):
    directories = [d for d in listdir(data_path) if not d.startswith('.')]
    for language in languages:
        if language not in directories:
            print("Cannot find '" + language + "'' directory into filesystem.")
            print("Please, check if exists '" + language + "'' into europarl_raw directory or remove from languages.txt.")
            languages = list()
            break
    return languages

def find_files(data_path, languages_for_training):
    files = dict()
    languages = get_directories(data_path, languages_for_training) 
    for lang in languages:
        files[lang] = [f for f in listdir('%s/%s/'%(data_path,lang)) if not f.startswith('.')]
        print("%s : %i ficheros" %(lang,len(files[lang])))
    return files

"""def get_words(text):
    with open(text) as f:
        words = re.compile('\w+').findall(f.read())
    return ' '.join(words)"""

"""def load_inputs(inputs):
    return map(get_words, inputs)"""

def get_chunks(words):
    sentences = list()

    offset = 0
    chunk_len = random.randint(1,20)
    rest = len(words) - chunk_len
    
    while rest > 0:
        chunk = words[offset:offset+chunk_len]
        sentences.append(' '.join(chunk))
        offset += chunk_len
        chunk_len = random.randint(1,20)
        rest -= chunk_len

    return sentences

def get_sentences(text):
    words = re.compile('\w+').findall(text)
    return get_chunks(words) 

def parse_files(data_path):
    X_set = list()
    y_set = list()
    languages = [d for d in listdir(data_path) if not d.startswith('.')]
    for lang in languages:
        files = [f for f in listdir('%s/%s/'%(data_path,lang)) if not f.startswith('.')]
        for fil in tqdm(files):
            with open('%s/%s/%s'%(data_path, lang, fil)) as f:
                sentences = get_sentences(f.read())
                for sentence in sentences:
                    X_set.append(sentence)
                    y_set.append(lang)
    return X_set,y_set

"""def pretty_show(data, predictions):
    for dt, pr in zip(data,predictions):
        print("%s\t%s"%(dt,pr))"""

def classify(to_predict):
    """
    Returns the classification of the given inputs
    """
    with open(args.model, 'rb') as f:
        model = pickle.load(f)
    return model.predict(to_predict)
    #pretty_show(args.dataset, predicted)

def confusion_matrix(predicted, test):
    cm = nltk.ConfusionMatrix(predicted, test)
    print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))

if __name__ == "__main__":

    #Get arguments
    parser = argparse.ArgumentParser(description='Files classification')
    parser.add_argument('model', metavar='M', type=str, help='Pickle file')
    parser.add_argument('languages', metavar='M', type=str, help='Languages for training')
    parser.add_argument('dataset', metavar='D', type=str, help='Folder containing the documents within the subfolders')
    args = parser.parse_args()

    languages_for_classify = list(open(args.languages,'r'))[0].rstrip().split(',') #Remove \n

    files = find_files(args.dataset, languages_for_classify)

    to_predict,test = parse_files(args.dataset)

    predicted = classify(to_predict)
    
    #TODO: Hay que hacer tags con los datos, los de entrada y los que salen de la red bayesiana.

    confusion_matrix(predicted, test)

