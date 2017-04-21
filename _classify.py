# $ python3 classify.py model.pickle ./wikipedia/spanish/Spain.es

import re
import argparse
import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

## CLI definition
parser = argparse.ArgumentParser(description='Files classification')
parser.add_argument('model', metavar='M', type=str, help='Pickle file')
parser.add_argument('inputs', metavar='F', nargs='+', type=str, help='Files to classify')
args = parser.parse_args()
##

def get_sentence(text):
    """
    Filter out words from text.
    Returns string with only words separated by spaces.
    """
    return text

def load_inputs(inputs):
    """
    Loads into objects the files passed as input.
    """
    return map(get_sentence, inputs)

def pretty_show(data, predictions):
    """
    Print results as the format:
    File category
    """
    for dt, pr in zip(data,predictions):
        print("%s\t%s"%(dt,pr))

def classify(to_predict):
    """
    Returns the classification of the given inputs
    """
    with open(args.model, 'rb') as f:
        model = pickle.load(f)
    predicted = model.predict(to_predict)
    pretty_show(args.inputs, predicted)

if __name__ == "__main__":

	to_predict = load_inputs(args.inputs)
	classify(to_predict)