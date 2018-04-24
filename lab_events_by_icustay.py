import csv
import pandas as pd
import numpy as np
from tfidf import tf_idf
import enchant
import string

d = enchant.Dict("en_US")

def concat(series):
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

icustays_path = '../data/ICUSTAYS.csv'
#"ROW_ID","SUBJECT_ID","HADM_ID","ICUSTAY_ID","DBSOURCE","FIRST_CAREUNIT","LAST_CAREUNIT","FIRST_WARDID","LAST_WARDID","INTIME","OUTTIME","LOS"
labevents_path = '../data/LABEVENTS.csv'
#"ROW_ID","SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"
patients_path = '../data/PATIENTS.csv'
#"ROW_ID","SUBJECT_ID","GENDER","DOB","DOD","DOD_HOSP","DOD_SSN","EXPIRE_FLAG"

SECONDS_IN_A_YEAR = 31536000.0
DAYS_IN_A_YEAR = 365

print "loading icustays"
icustays = pd.read_csv(icustays_path)
print "loading labevents"
labevents = pd.read_csv(labevents_path)
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

icu_lab = icu_under_18.merge(labevents, left_on='SUBJECT_ID', right_on='SUBJECT_ID')
icu_lab['CHARTTIME'] = pd.to_datetime(icu_lab['CHARTTIME'])
icu_lab['OUTTIME'] = pd.to_datetime(icu_lab['OUTTIME'])
print "icu_lab.shape before filtering charttime: ", icu_lab.shape
icu_lab = icu_lab[(icu_lab['CHARTTIME'] >= icu_lab['INTIME']) & (icu_lab['CHARTTIME'] <= icu_lab['OUTTIME'])]
print "icu_lab.shape after filtering charttime: ", icu_lab.shape
print list(icu_lab)

icu_lab.to_csv('patients_icustays_labevents.csv')
