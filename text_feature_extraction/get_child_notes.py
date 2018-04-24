import csv
import pandas as pd
import numpy as np
import enchant
import string
from get_text_feats import vectorize_text_feature
import math

d = enchant.Dict("en_US")


"""
Text concatenation without spell checking.
"""

def concat(series):
    as_list = series.tolist()
    #fix spelling
    new_list = []
    for note in as_list:
        words = note.translate(None, string.punctuation).lower().split()
        new_list.extend(words)
    result = " ".join(new_list)
    return result


"""
Text concatenation with spell checking. Not used in final iteration of classifier.
"""
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

"""
Gets child notes by icustay id.
Also saves just the text to a csv notes_by_icustay.csv
"""
def get_child_notes_by_icustay(spell_check):
    icustays_path = '../data/ICUSTAYS.csv'
    #"ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","DBSOURCE","FIRST_CAREUNIT","LAST_CAREUNIT","FIRST_WARDID","LAST_WARDID","INTIME","OUTTIME","LOS"
    noteevents_path = '../data/NOTEEVENTS.csv'
    #"ROW_ID","SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"
    patients_path = '../data/PATIENTS.csv'
    #"ROW_ID","SUBJECT_ID","GENDER","DOB","DOD","DOD_HOSP","DOD_SSN","EXPIRE_FLAG"

    SECONDS_IN_A_YEAR = 31536000.0
    DAYS_IN_A_YEAR = 365

    print("loading icustays")
    icustays = pd.read_csv(icustays_path)
    print("loading noteevents")
    noteevents = pd.read_csv(noteevents_path)
    print("loading patients")
    patients = pd.read_csv(patients_path)

    print("joining icustays and patients")
    icustays_and_patients = icustays.merge(patients, left_on='SUBJECT_ID', right_on='SUBJECT_ID')

    print("filtering for children")
    icustays_and_patients['INTIME'] = pd.to_datetime(icustays_and_patients['INTIME'])
    icustays_and_patients['DOB'] = pd.to_datetime(icustays_and_patients['DOB'])
    icustays_and_patients['AGE'] = (icustays_and_patients['INTIME'] - icustays_and_patients['DOB']).dt.days / DAYS_IN_A_YEAR
    icu_under_89 = icustays_and_patients[(icustays_and_patients['AGE'] >= 0)]

    icu_under_18 = icu_under_89[icu_under_89['AGE'] < 18]

    icu_notes = icu_under_18.merge(noteevents, left_on='SUBJECT_ID', right_on='SUBJECT_ID')
    icu_notes['CHARTTIME'] = pd.to_datetime(icu_notes['CHARTTIME'])
    icu_notes['OUTTIME'] = pd.to_datetime(icu_notes['OUTTIME'])
    print("icu_notes.shape before filtering charttime: ", icu_notes.shape)
    icu_notes = icu_notes[(icu_notes['CHARTTIME'] >= icu_notes['INTIME']) & (icu_notes['CHARTTIME'] <= icu_notes['OUTTIME'])]
    print("icu_notes.shape after filtering charttime: ", icu_notes.shape)


    if spell_check:
        icu_notes = icu_notes.groupby(['ICUSTAY_ID'], axis=0).agg({'TEXT':sc_concat}).reset_index()
    else:
        icu_notes = icu_notes.groupby(['ICUSTAY_ID'], axis=0).agg({'TEXT':concat}).reset_index()

    icu_note_text = icu_notes['TEXT'].tolist()
    icu_note_text = [" ".join(t.lower().translate(None, string.punctuation).replace('\n',' ').split()) for t in icu_note_text]

    icu_notes['TEXT'] = pd.Series(data=icu_note_text)

    # print "icu_notes['TEXT'].shape:",icu_notes['TEXT'].shape

    print("saving text to notes_by_icustay.csv")

    with open('notes_by_icustay.csv', 'w') as infile:
        writer = csv.writer(infile)
        for text in icu_note_text:
            writer.writerow([text])

    return icu_notes

if __name__ == '__main__':
    icu_notes = get_child_notes_by_icustay(spell_check=False)
    print('saving patients_icustays_noteevents.csv')
    icu_notes.to_csv('patients_icustays_noteevents.csv')
