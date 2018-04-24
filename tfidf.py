from sklearn.feature_extraction.text import TfidfVectorizer
import json
import csv
import operator
import sys
import locale
import pandas as pd
from nltk.corpus import stopwords
from numpy import transpose
from numpy import array
import string
import unicodedata
import nltk
from nltk.stem.porter import PorterStemmer

"""
custom_stop_stems is a list of stems that you don't want to include beyond the basic english words
"""
custom_stop_stems = []

stemmer = PorterStemmer()
tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

def num_with_commas(num):
    return locale.format("%d", num, grouping=True)

def get_top_n_tfidf(filename, n):
    list_of_top_n = []
    with open(filename) as infile:
        reader = csv.reader(infile)
        is_header = True
        row_counter = 0
        for row in reader:
            if (is_header):
                #skip
                is_header = False
            elif (row_counter < n + 1):
                word = row[0]
                tfidf = float(row[1])
                list_of_top_n.append((word, tfidf))
            else:
                break
            row_counter += 1
    return list_of_top_n

def get_list_of_comments(filename):
    result = []
    with open(filename) as inputfile:
        reader = csv.reader(inputfile)
        for row in reader:
            comment = row[0]
            result.append(comment)
    return result

def output_tf_idf(tfidf_matrix, output_name, feature_names, doc):
    print "open ", output_name
    with open(output_name, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Word", "TF-IDF"])

    feature_index = tfidf_matrix[doc,:].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])

    print "sorting ", output_name
    mapping = {}
    for word, score in [(feature_names[i].encode('utf-8'), s) for (i, s) in tfidf_scores]:
        mapping[word] = score

    sortedByValue = sorted(mapping.items(), key=operator.itemgetter(1), reverse=True)

    print "writing ", output_name
    with open(output_name, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(sortedByValue[:500])

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        item = item.translate(tbl)
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)

    stems = [s for s in stems if s not in custom_stop_stems and s] # not a custom stop word or empty string
    result = []
    for s in stems:
        can_add = True
        for rs in recovery_stems:
            if s.startswith(rs) or s.isspace():
                can_add = False
                break
        if can_add:
            result.append(s)
    return result


"""
This method takes in two lists: input paths and output paths.
The order of each input should correspond to its output.
See example in main method.

This TF-IDF method stems and removes english stop words.
"""

def tf_idf(corpus_filenames_list, output_paths_list):
    print "---------------- tf_idf ----------------"
    # print "corpus: ", corpus_filenames_list
    assert len(corpus_filenames_list) == len(output_paths_list), "corpus list and output paths list are of different lengths"
    # the TF-IDF values of all the documents in the corpus

    # tf = TfidfVectorizer(tokenizer=tokenize, lowercase=True, analyzer='word', stop_words='english', ngram_range=(1, 1))
    tf = TfidfVectorizer(lowercase=True, analyzer='word', stop_words='english', ngram_range=(1, 1))
    tfidf_matrix = tf.fit_transform(corpus_filenames_list)
    # list of all the tokens or n-grams or words
    feature_names = tf.get_feature_names()

    num_docs = len(corpus_filenames_list)

    for doc in xrange(num_docs):
        output_path = output_paths_list[doc]
        output_tf_idf(tfidf_matrix, output_path, feature_names, doc)

if __name__ == '__main__':
    corpus = pd.read_csv('notes_by_icustay.csv', header=0, names=['text'])['text'].values

    num_corpora = len(corpus)
    output_name = ['tfidf/tfidf-doc'+str(i)+'.csv' for i in xrange(num_corpora)]
    tf_idf(corpus, output_name)
