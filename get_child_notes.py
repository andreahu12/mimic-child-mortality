import csv
import pandas as pd
import numpy as np
import enchant
import string
from get_text_feature import vectorize_text_feature
import math

d = enchant.Dict("en_US")

def concat(series):
    as_list = series.tolist()
    #fix spelling
    new_list = []
    for note in as_list:
        words = note.translate(None, string.punctuation).lower().split()
        new_list.extend(words)
    result = " ".join(new_list)
    return result

def sc_concat(series):
    as_list = series.tolist()
    #fix spelling
    new_list = []
    for note in as_list:
        words = note.translate(None, string.punctuation).lower().split()
        words = [d.suggest(word)[0] if not d.check(word) and len(d.suggest(word)) > 0 else word for word in words]
        new_note = " ".join(words)
        new_list.append(new_note)
    result = " ".join(new_list)
    return result

def get_child_notes_by_icustay(spell_check):
    icustays_path = '../data/ICUSTAYS.csv'
    #"ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","DBSOURCE","FIRST_CAREUNIT","LAST_CAREUNIT","FIRST_WARDID","LAST_WARDID","INTIME","OUTTIME","LOS"
    noteevents_path = '../data/NOTEEVENTS.csv'
    #"ROW_ID","SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"
    patients_path = '../data/PATIENTS.csv'
    #"ROW_ID","SUBJECT_ID","GENDER","DOB","DOD","DOD_HOSP","DOD_SSN","EXPIRE_FLAG"

    SECONDS_IN_A_YEAR = 31536000.0
    DAYS_IN_A_YEAR = 365

    print "loading icustays"
    icustays = pd.read_csv(icustays_path)
    print "loading noteevents"
    noteevents = pd.read_csv(noteevents_path)
    print "loading patients"
    patients = pd.read_csv(patients_path)

    print "joining icustays and patients"
    icustays_and_patients = icustays.merge(patients, left_on='SUBJECT_ID', right_on='SUBJECT_ID')

    print "filtering for children"
    icustays_and_patients['INTIME'] = pd.to_datetime(icustays_and_patients['INTIME'])
    icustays_and_patients['DOB'] = pd.to_datetime(icustays_and_patients['DOB'])
    icustays_and_patients['AGE'] = (icustays_and_patients['INTIME'] - icustays_and_patients['DOB']).dt.days / DAYS_IN_A_YEAR
    icu_under_89 = icustays_and_patients[(icustays_and_patients['AGE'] >= 0)]


    icu_under_18 = icu_under_89[icu_under_89['AGE'] < 18]

    icu_notes = icu_under_18.merge(noteevents, left_on='SUBJECT_ID', right_on='SUBJECT_ID')
    icu_notes['CHARTTIME'] = pd.to_datetime(icu_notes['CHARTTIME'])
    icu_notes['OUTTIME'] = pd.to_datetime(icu_notes['OUTTIME'])
    print "icu_lab.shape before filtering charttime: ", icu_notes.shape
    icu_notes = icu_notes[(icu_notes['CHARTTIME'] >= icu_notes['INTIME']) & (icu_notes['CHARTTIME'] <= icu_notes['OUTTIME'])]
    print "icu_notes.shape after filtering charttime: ", icu_notes.shape
    print list(icu_notes)

    print "shape:", icu_notes.shape
    print "aggregating"

    if spell_check:
        icu_notes = icu_notes.groupby(['ICUSTAY_ID'], axis=0).agg({'TEXT':sc_concat}).reset_index()
    else:
        icu_notes = icu_notes.groupby(['ICUSTAY_ID'], axis=0).agg({'TEXT':concat}).reset_index()

    icu_note_text = icu_notes['TEXT'].tolist()
    icu_note_text = [" ".join(t.lower().translate(None, string.punctuation).replace('\n',' ').split()) for t in icu_note_text]

    icu_notes['TEXT'] = pd.Series(data=icu_note_text)

    return icu_notes

if __name__ == '__main__':
    icu_notes = get_child_notes_by_icustay(spell_check=False)
    print 'saving patients_icustays_noteevents.csv'
    icu_notes.to_csv('patients_icustays_noteevents.csv')


#
# print "shape:", icu_notes.shape
# print "aggregating"
# icu_notes = icu_notes.groupby(['ICUSTAY_ID'], axis=0).agg({'TEXT':concat}).reset_index()
# # print list(icu_notes)
#
# # print "shape:", icu_notes.shape
#
# # print icu_notes['TEXT']
#
# icu_note_text = icu_notes['TEXT'].tolist()
# icu_note_text = [" ".join(t.lower().translate(None, string.punctuation).replace('\n',' ').split()) for t in icu_note_text]
#
# icu_notes['TEXT'] = pd.Series(data=icu_note_text)
#
# # icu_notes = icu_notes[icu_notes['ICUSTAY_ID'] >= 0]
#
# icustay_id_to_notes = icu_notes[['ICUSTAY_ID', 'TEXT']]
# icustay_id_to_notes['FEATURES'] = icustay_id_to_notes['TEXT'].apply(vectorize_text_feature)
# icustay_id_to_notes = icustay_id_to_notes[['ICUSTAY_ID', 'FEATURES']]
#
# def get_topic0(feats):
#     result = feats[0]
#     return result
#
# def get_topic1(feats):
#     result = feats[1]
#     return result
#
# def get_topic2(feats):
#     result = feats[2]
#     return result
#
# def get_topic3(feats):
#     result = feats[3]
#     return result
#
# def get_topic4(feats):
#     result = feats[4]
#     return result
#
# def get_topic5(feats):
#     result = feats[5]
#     return result
#
# def get_topic6(feats):
#     result = feats[6]
#     return result
#
# def get_topic7(feats):
#     result = feats[7]
#     return result
#
# def get_topic8(feats):
#     result = feats[8]
#     return result
#
# def get_topic9(feats):
#     result = feats[9]
#     return result
#
# def get_topic10(feats):
#     result = feats[10]
#     return result
#
# def get_topic11(feats):
#     result = feats[11]
#     return result
#
# def get_topic12(feats):
#     result = feats[12]
#     return result
#
# def get_topic13(feats):
#     result = feats[13]
#     return result
#
# def get_topic14(feats):
#     result = feats[14]
#     return result
#
# def get_topic15(feats):
#     result = feats[15]
#     return result
#
# def get_topic16(feats):
#     result = feats[16]
#     return result
#
# def get_topic17(feats):
#     result = feats[17]
#     return result
#
# def get_topic18(feats):
#     result = feats[18]
#     return result
#
# icustay_id_to_notes['TOPIC0'] = icustay_id_to_notes['FEATURES'].apply(get_topic0)
# icustay_id_to_notes['TOPIC1'] = icustay_id_to_notes['FEATURES'].apply(get_topic1)
# icustay_id_to_notes['TOPIC2'] = icustay_id_to_notes['FEATURES'].apply(get_topic2)
# icustay_id_to_notes['TOPIC3'] = icustay_id_to_notes['FEATURES'].apply(get_topic3)
# icustay_id_to_notes['TOPIC4'] = icustay_id_to_notes['FEATURES'].apply(get_topic4)
# icustay_id_to_notes['TOPIC5'] = icustay_id_to_notes['FEATURES'].apply(get_topic5)
# icustay_id_to_notes['TOPIC6'] = icustay_id_to_notes['FEATURES'].apply(get_topic6)
# icustay_id_to_notes['TOPIC7'] = icustay_id_to_notes['FEATURES'].apply(get_topic7)
# icustay_id_to_notes['TOPIC8'] = icustay_id_to_notes['FEATURES'].apply(get_topic8)
# icustay_id_to_notes['TOPIC9'] = icustay_id_to_notes['FEATURES'].apply(get_topic9)
# icustay_id_to_notes['TOPIC10'] = icustay_id_to_notes['FEATURES'].apply(get_topic10)
# icustay_id_to_notes['TOPIC11'] = icustay_id_to_notes['FEATURES'].apply(get_topic11)
# icustay_id_to_notes['TOPIC12'] = icustay_id_to_notes['FEATURES'].apply(get_topic12)
# icustay_id_to_notes['TOPIC13'] = icustay_id_to_notes['FEATURES'].apply(get_topic13)
# icustay_id_to_notes['TOPIC14'] = icustay_id_to_notes['FEATURES'].apply(get_topic14)
# icustay_id_to_notes['TOPIC15'] = icustay_id_to_notes['FEATURES'].apply(get_topic15)
# icustay_id_to_notes['TOPIC16'] = icustay_id_to_notes['FEATURES'].apply(get_topic16)
# icustay_id_to_notes['TOPIC17'] = icustay_id_to_notes['FEATURES'].apply(get_topic17)
#
# icustay_id_to_notes = icustay_id_to_notes[['ICUSTAY_ID', 'TOPIC0', 'TOPIC1', 'TOPIC2', \
#     'TOPIC3', 'TOPIC4', 'TOPIC5', 'TOPIC6', 'TOPIC7', 'TOPIC8', 'TOPIC9', 'TOPIC10', \
#     'TOPIC11', 'TOPIC12', 'TOPIC13', 'TOPIC14', 'TOPIC15', 'TOPIC16', 'TOPIC17']]
#
# print icustay_id_to_notes.describe()
#
# icustay_id_to_notes.to_csv('icustay_id_to_features.csv')
