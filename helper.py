'''
@author: wanzeyu

@contact: wan.zeyu@outlook.com

@file: helper.py

@time: 2017/12/4 2:19
'''

import nltk
import numpy as np
from keras.utils.np_utils import to_categorical
from numpy import array

np.set_printoptions(threshold=np.nan)
padding_len = 29

UNK_TOKEN = 2
END_TOKEN = 0

# line read limit in case of "Memory Error"
limit = 5


def get_vocab():
    print("generate vocab")
    words = []
    count_1 = 0
    count_2 = 0
    with open("train_source.txt", "r", encoding="utf8") as fp:
        for line in fp:
            if count_1 == limit:
                break
            count_1 += 1
            res = line.strip().split(" ")
            for i in res:
                words.append(i)
    with open("train_target.txt", "r", encoding="utf8") as fp:
        for line in fp:
            if count_2 == limit:
                break
            count_2 += 1
            res = line.strip().split(" ")
            for i in res:
                words.append(i)
    freq = nltk.FreqDist(words)
    with open("train_vocab.txt", "w", encoding="utf8") as fp:
        fp.write("</S>")
        fp.write("\n")
        fp.write("<S>")
        fp.write("\n")
        fp.write("<UNK>")
        fp.write("\n")
        for word in freq.most_common():
            fp.write(word[0])
            fp.write("\n")


def load_vocab(filename):
    vocab = {}
    with open(filename) as f:
        for idx, line in enumerate(f):
            vocab[line.strip()] = idx
    return vocab


# generate vocab
get_vocab()
vocab = load_vocab("train_vocab.txt")
id_vocab = {value: key for key, value in vocab.items()}
num_decoder_tokens = len(vocab)


def tokenize_and_map(line):
    return [vocab["<S>"]] + [vocab.get(token, UNK_TOKEN) for token in line.split(' ')]


def get_data_v2(file_name):
    res = []
    count = 0
    with open(file_name) as fp:
        for in_line in fp:
            if count == limit:
                break
            count += 1
            tmp = tokenize_and_map(in_line)[:(padding_len - 1)] + [END_TOKEN]
            res.append(tmp)
    return res


def get_data_v2_offset(file_name):
    res = []
    count = 0
    with open(file_name) as fp:
        for in_line in fp:
            if count == limit:
                break
            count += 1
            tmp = tokenize_and_map(in_line)[:(padding_len - 1)] + [END_TOKEN]
            tmp = tmp[1:]
            res.append(tmp)
    return res


def manual_one_hot(lines):
    res = []
    for line in lines:
        res.append(to_categorical(line, num_classes=num_decoder_tokens))
    return array(res)
