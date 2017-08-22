import numpy as np
import re
import itertools
from collections import Counter
import os

dir = os.path.dirname(os.path.realpath(__file__))
dir += "\\data\\"

# Taken from https://github.com/dennybritz/cnn-text-classification-tf/blob/master/data_helpers.py


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(categories):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.

    Modified for different number of labels
    """
    # Load data from files
    examples = []
    x_text = []
    for cat in categories:
        examples.append(list(open(dir+cat+".txt", "r").readlines()))
        examples[-1] = [s.strip() for s in examples[-1]]

        x_text += examples[-1]

    # Split by words
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    labels = []
    id = []
    pos = 0
    for _ in examples:
        ref = [0,0,0,0,0,0,0,0]
        ref[pos] = 1
        id.append(ref[:])
        ref[pos] = 0
        pos += 1
    pos = 0
    for data in examples:
        labels.append([id[pos] for _ in data])
        pos += 1
    y = np.concatenate(labels, 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]