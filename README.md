# mimic-child-mortality
Final project for CSE 6250: Big Data for Healthcare with Prof. Jimeng Sun. Relies on data from MIMIC-III.

## Generating Features
Our code assumes that there is a `data` folder stored at the same directory as `mimic-child-mortality` that contains raw CSV's from the MIMIC website: https://physionet.org/works/MIMICIIIClinicalDatabase/files/.

### Getting Child LABEVENTS Data by ICUSTAY_ID
Run `python lab_events_by_icustay.py`.

## Graphs
To generate the graphs used in our paper, run `python graphs.py`.
