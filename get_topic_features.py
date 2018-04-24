import csv
import pandas as pd
import numpy as np
from tfidf import tf_idf
import enchant
import string
from get_text_feature import vectorize_text_feature
import math
from get_child_notes import get_child_notes_by_icustay

icu_notes = get_child_notes_by_icustay(spell_check=False)

icustay_id_to_notes = icu_notes[['ICUSTAY_ID', 'TEXT']]
icustay_id_to_notes['FEATURES'] = icustay_id_to_notes['TEXT'].apply(vectorize_text_feature)
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

def get_topic10(feats):
    result = feats[10]
    return result

def get_topic11(feats):
    result = feats[11]
    return result

def get_topic12(feats):
    result = feats[12]
    return result

def get_topic13(feats):
    result = feats[13]
    return result

def get_topic14(feats):
    result = feats[14]
    return result

def get_topic15(feats):
    result = feats[15]
    return result

def get_topic16(feats):
    result = feats[16]
    return result

def get_topic17(feats):
    result = feats[17]
    return result

def get_topic18(feats):
    result = feats[18]
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
icustay_id_to_notes['TOPIC10'] = icustay_id_to_notes['FEATURES'].apply(get_topic10)
icustay_id_to_notes['TOPIC11'] = icustay_id_to_notes['FEATURES'].apply(get_topic11)
icustay_id_to_notes['TOPIC12'] = icustay_id_to_notes['FEATURES'].apply(get_topic12)
icustay_id_to_notes['TOPIC13'] = icustay_id_to_notes['FEATURES'].apply(get_topic13)
icustay_id_to_notes['TOPIC14'] = icustay_id_to_notes['FEATURES'].apply(get_topic14)
icustay_id_to_notes['TOPIC15'] = icustay_id_to_notes['FEATURES'].apply(get_topic15)
icustay_id_to_notes['TOPIC16'] = icustay_id_to_notes['FEATURES'].apply(get_topic16)
icustay_id_to_notes['TOPIC17'] = icustay_id_to_notes['FEATURES'].apply(get_topic17)

icustay_id_to_notes = icustay_id_to_notes[['ICUSTAY_ID', 'TOPIC0', 'TOPIC1', 'TOPIC2', \
    'TOPIC3', 'TOPIC4', 'TOPIC5', 'TOPIC6', 'TOPIC7', 'TOPIC8', 'TOPIC9', 'TOPIC10', \
    'TOPIC11', 'TOPIC12', 'TOPIC13', 'TOPIC14', 'TOPIC15', 'TOPIC16', 'TOPIC17']]

print icustay_id_to_notes.describe()

icustay_id_to_notes.to_csv('icustay_id_to_features.csv')

# "print saving"
# with open('notes_by_icustay2.csv', 'w') as infile:
#     writer = csv.writer(infile)
#     writer.writerows(icu_note_text)
