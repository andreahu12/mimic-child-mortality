# mimic-child-mortality
Final project for CSE 6250: Big Data for Healthcare with Prof. Jimeng Sun. Relies on data from MIMIC-III.

## Setup
This project uses a python virtual environment. To setup this environment, run:

`source bdh/bin/activate`

`pip install -r requirements.txt`

## Getting Data
Our code assumes that there is a `data` folder stored at the same directory as `mimic-child-mortality` that contains raw CSV's from the MIMIC website: https://physionet.org/works/MIMICIIIClinicalDatabase/files/.

The files necessary for the pipeline include:
* ADMISSIONS.csv
* CPTEVENTS.csv
* ICUSTAYS.csv
* LABEVENTS.csv
* LDAEVENTS.csv
* NOTEEVENTS.csv
* PATIENTS.csv
* categories.csv

### Getting Child NOTEEVENTS Text by ICUSTAY_ID
In the text_feature_extraction directory, run `python get_child_notes.py`. Outputs 2 CSVs:
1. `patients_icustays_noteevents.csv`: child noteevent rows by ICUSTAY_ID. Each row contains the text for all notes belonging to that child during that ICU stay.
2. `notes_by_icustay.csv`: just the text from the noteevents so that we can run TFIDF and LDA on it.

### Getting Child LABEVENTS Data by ICUSTAY_ID
In the data_compression directory,run `python lab_events_by_icustay.py`. Outputs CSV called `patients_icustays_labevents.csv` that contains child labevent rows by ICUSTAY_ID. Contains labevents belonging to each child the ICU stay pertains to.

### Get TFIDF terms
In the text_feature_extraction directory, run `python tfidf.py`. Uses `notes_by_icustay.csv` as input. Sorted TFIDF terms per note will be saved at `tfidf/tfidf-doc*.`

### Run LDA and save components
In the text_feature_extraction directory, run `python lda.py`. Parameters (to reduce runtime overhead) are in the main method: `check_spelling`, `generate_vects`, `run_lda`. If running for the first time, set generate_vects and run_lda to True. Saves categories to `categories.csv`.

### Get LDA Features for input into the classifier
In the text_feature_extraction directory, run `get_topic_features.py`. Text generated features by `ICUSTAY_ID` saved in `icustay_id_to_features.csv`.

## Graphs
To generate the graphs used in our paper, in the text_feature_extraction directory, run `python graphs.py`.

## Aggregating Features
To generate aggregate features and features split by age group, run `python extract_features.py`
run `cat * > features.txt', 'cat * > newborn.txt', 'cat * > teen.txt' to merge the txt file, move the txt file to the folder of code. 

## Parameter tuning
To tuning the parameter for each classifiers, run 'python tuning_parameters.py'

## Classification
To run classifiers on under sampling data (all ages under 18), run `python undersample_all.py`

To run classifiers on under sampling data from newborns, run `python undersample_newborn.py` 

To run claasifiers on over sampling data from newborns, run `python oversample_newborn.py`
