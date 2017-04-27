# $ python3 _classify.py model.pickle "This is an example."

import re
import argparse
import pickle

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def get_sentence(text):
    return text

def load_inputs(inputs):
    return map(get_sentence, inputs)

def pretty_show(data, predictions):
    for dt, pr in zip(data,predictions):
        print("%s\t%s"%(dt,pr))

def classify(to_predict):
    with open(args.model, 'rb') as f:
        model = pickle.load(f)
    predicted = model.predict(to_predict)
    pretty_show(args.inputs, predicted)

if __name__ == "__main__":

	#Get arguments
	parser = argparse.ArgumentParser(description='Files classification')
	parser.add_argument('model', metavar='M', type=str, help='Pickle file')
	parser.add_argument('inputs', metavar='F', nargs='+', type=str, help='Files to classify')
	args = parser.parse_args()

	to_predict = load_inputs(args.inputs)
	classify(to_predict)