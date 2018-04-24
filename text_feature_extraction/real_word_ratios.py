import csv
import pandas as pd
import numpy as np
from lda import load_terms, lda_component_terms

tfidf_dir = 'tfidf/spell-checked/'
terms = load_terms(tfidf_dir, check_spelling=True)
read_folder = 'lda/spell-checked/'

component_nums = range(5, 51, 5)
median_ratios = []
for n in component_nums:
    print("-----------------------------------------------")
    print("n:", n)
    lda_component_path = read_folder + 'lda'+str(n)+'-components.csv'
    component_terms = lda_component_terms(lda_component_path, terms, n_top_words=50)

    def lowercase_list(component):
        return [c.lower() for c in component]
    # print ("lowercasing component terms")
    lowercase_components = [lowercase_list(component) for component in component_terms]
    # print ("loading data")
    data = pd.read_csv('notes_by_icustay.csv', header=0, names=['text'])['text'].tolist()

    # print ("getting unique lowercase words from text")
    words_in_text = set()
    for text in data:
        words_in_text.update(text.lower().split())

    ratios = []
    # print ("counting words in spell checked components that exist")
    for lc in lowercase_components:
        real_words = sum([1 if word in words_in_text else 0 for word in lc])
        total = len(lc)
        if real_words == 0:
            ratios.append(0)
        else:
            ratio = float(real_words) / total
            # print ("---------------------------------------------")
            # print ("real_words:",real_words)
            # print ("total:", total)
            # print ("ratio:", ratio)
            ratios.append(ratio)

    mean_ratio = np.mean(ratios)
    median_ratio = np.median(ratios)
    std_ratio = np.std(ratios)
    print ("MEAN RATIO:", mean_ratio)
    print ("MEDIAN RATIO:", median_ratio)
    print ("STD RATIO:", std_ratio)

    median_ratios.append(median_ratio)

print (component_nums)
print (median_ratios)

print ("DONE!")
