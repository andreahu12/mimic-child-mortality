import csv
import pandas as pd
import numpy as np
from tfidf import tf_idf
import enchant
import string
from get_text_feature import vectorize_text_feature
import math
from get_child_notes import get_child_notes_by_icustay

icu_notes = get_child_notes_by_icustay(spell_check=True)

icustay_id_to_notes = icu_notes[['ICUSTAY_ID', 'TEXT']]
icustay_id_to_notes['FEATURES'] = icustay_id_to_notes['TEXT'].apply(vectorize_text_feature_sc)
icustay_id_to_notes = icustay_id_to_notes[['ICUSTAY_ID', 'FEATURES']]

def get_topic0(feats):
    result = feats[0]
    return result

def get_topic1(feats):
    result = feats[1]
    return result

def get_topic2(feats):
    result = feats[2]
    return result

def get_topic3(feats):
    result = feats[3]
    return result

def get_topic4(feats):
    result = feats[4]
    return result

def get_topic5(feats):
    result = feats[5]
    return result

def get_topic6(feats):
    result = feats[6]
    return result

def get_topic7(feats):
    result = feats[7]
    return result

def get_topic8(feats):
    result = feats[8]
    return result

def get_topic9(feats):
    result = feats[9]
    return result


icustay_id_to_notes['TOPIC0'] = icustay_id_to_notes['FEATURES'].apply(get_topic0)
icustay_id_to_notes['TOPIC1'] = icustay_id_to_notes['FEATURES'].apply(get_topic1)
icustay_id_to_notes['TOPIC2'] = icustay_id_to_notes['FEATURES'].apply(get_topic2)
icustay_id_to_notes['TOPIC3'] = icustay_id_to_notes['FEATURES'].apply(get_topic3)
icustay_id_to_notes['TOPIC4'] = icustay_id_to_notes['FEATURES'].apply(get_topic4)
icustay_id_to_notes['TOPIC5'] = icustay_id_to_notes['FEATURES'].apply(get_topic5)
icustay_id_to_notes['TOPIC6'] = icustay_id_to_notes['FEATURES'].apply(get_topic6)
icustay_id_to_notes['TOPIC7'] = icustay_id_to_notes['FEATURES'].apply(get_topic7)
icustay_id_to_notes['TOPIC8'] = icustay_id_to_notes['FEATURES'].apply(get_topic8)
icustay_id_to_notes['TOPIC9'] = icustay_id_to_notes['FEATURES'].apply(get_topic9)


icustay_id_to_notes = icustay_id_to_notes[['ICUSTAY_ID', 'TOPIC0', 'TOPIC1', 'TOPIC2', \
    'TOPIC3', 'TOPIC4', 'TOPIC5', 'TOPIC6', 'TOPIC7', 'TOPIC8', 'TOPIC9']]

print icustay_id_to_notes.describe()

icustay_id_to_notes.to_csv('sc-icustay_id_to_features.csv')

# "print saving"
# with open('sc-notes_by_icustay2.csv', 'w') as infile:
#     writer = csv.writer(infile)
#     writer.writerows(icu_note_text)
