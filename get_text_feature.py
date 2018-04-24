from collections import Counter
import csv

"""
spell checked
"""
def vectorize_text_feature_sc(text):
    with open('spellchecked-categories.csv', 'r') as infile:
        reader = csv.reader(infile)
        list_of_categories = [[word.strip().replace('\'', '') for word in row] for row in reader]

    result = []
    c = Counter(text.split())
    for category in list_of_categories:
        total = sum([c[word] for word in category])
        category_size = len(category)
        result.append(float(total) / category_size)
    return result

"""
not spell checked
"""

def vectorize_text_feature(text):
    with open('categories.csv', 'r') as infile:
        reader = csv.reader(infile)
        list_of_categories = [[word.strip().replace('\'', '') for word in row] for row in reader]

    result = []
    c = Counter(text.split())
    for category in list_of_categories:
        total = sum([c[word] for word in category])
        category_size = len(category)
        result.append(float(total) / category_size)
    return result
