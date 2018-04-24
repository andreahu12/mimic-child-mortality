# mimic-child-mortality
Final project for CSE 6250: Big Data for Healthcare with Prof. Jimeng Sun. Relies on data from MIMIC-III.

## Generating Features
Our code assumes that there is a `data` folder stored at the same directory as `mimic-child-mortality` that contains raw CSV's from the MIMIC website: https://physionet.org/works/MIMICIIIClinicalDatabase/files/.

The following will be passed into PySpark to generate features:

### Getting Child NOTEEVENTS Text by ICUSTAY_ID
Run `python get_child_notes.py`. Outputs 2 CSVs:
1. `patients_icustays_noteevents.csv`: child noteevent rows by ICUSTAY_ID. Each row contains the text for all notes belonging to that child during that ICU stay.
2. `notes_by_icustay.csv`: just the text from the noteevents so that we can run TFIDF and LDA on it.

### Getting Child LABEVENTS Data by ICUSTAY_ID
Run `python lab_events_by_icustay.py`. Outputs CSV called `patients_icustays_labevents.csv` that contains child labevent rows by ICUSTAY_ID. Contains labevents belonging to each child the ICU stay pertains to.

### Get TFIDF terms
Run `python tfidf.py`. Uses `notes_by_icustay.csv` as input. Sorted TFIDF terms per note will be saved at `tfidf/tfidf-doc*.`

### Run LDA and save components
Run `python lda.py`. Parameters (to reduce runtime overhead) are in the main method: `check_spelling`, `generate_vects`, `run_lda`. If running for the first time, set generate_vects and run_lda to True. Saves categories to `categories.csv`.

### Get LDA Features for input into the classifier
Run `get_topic_features.py`. Text generated features by `ICUSTAY_ID` saved in `icustay_id_to_features.csv`.

## Graphs
To generate the graphs used in our paper, run `python graphs.py`.
