# ClinicFlow

A simple desktop clinic management app with a Tkinter GUI which can register 
patients, add doctors, and book/cancel/complete appointments. Built by a 
complete beginner, so don't expect anything fancy.


<img width="950" height="488" alt="GUI screenshot" src="https://github.com/user-attachments/assets/18be32e9-767f-409c-a8d2-3d5791d8e1a1" />



## Requirements
- It has no external packages, everything used in here (`tkinter`, `json`, 
  `os`, `datetime`) is part of the Python standard library

## How to run
1. Clone the repo (keep the folder structure intact — `clinicflow/` needs 
   to stay as a subfolder for the imports to work)
2. From the project root, run:
```
   	python3 main.py
```


## What it CAN do
- Register patients / doctors
- Book, cancel, and complete appointments
- View a patient's appointments or a doctor's schedule
- Search for patients by name
- Data persists to JSON files in `data/`

## What it CAN'T do
- Do a total database wipe
- Do login (I think it should be there for a database wipe since you can't 
  just allow anyone to wipe it all)

These will be added in the next commit.


