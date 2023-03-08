import urllib
import os
import re
import sqlite3
import pandas as pd
import numpy as np
import pypdf

def download_pdf(url):
    #open file from url or path, read binary
    file = open(url, "rb")
    read_file = pypdf.PdfReader(file)

    return read_file


def extract_incidents(read_file):
    # Create variable for total page length of PDF, initialize blank array
    total_pages = len(read_file.pages)
    single_line_array = []

    # For Loop to read table from each PDF page, extract each line from the page, and append to initialized array
    for pages in range(total_pages):
        page = read_file.pages[pages]
        page_text = page.extract_text()
        single_line = page_text.split('\n')

        for lines in single_line:
            single_line_array.append(lines)
    single_line_array.remove('Daily Incident Summary (Public)')
    del single_line_array[-1]
    del single_line_array[0]

    array_length = len(single_line_array)
    date_array = []
    incident_num_array = []
    location_array = []
    nature_array = []
    incident_ori_array = []

    for dates in range(array_length):
        date = single_line_array[dates]
        date_pattern = re.findall(r'\d/\d\d/\d\d\d\d\s\d:\d\d',date)
        date_pattern2 = re.findall(r'\d/\d\d/\d\d\d\d\s\d\d:\d\d',date)
        if (date_pattern != "") or (date_pattern2 != ""):
            date_array.append(date_pattern)
            date_array.append(date_pattern2)
    while [] in date_array:
        date_array.remove([])

    for incidentnum in range(array_length):
        incident_num = single_line_array[incidentnum]
        incident_num_pattern = re.findall(r'\d\d\d\d-\d\d\d\d\d\d\d\d',incident_num)
        incident_num_array.append(incident_num_pattern)

    # for location in range(array_length):
    #     location_txt = single_line_array[location]
    #     location_txt_pattern = re.findall(r'',location_txt)
    #     location_array.append(location_txt_pattern)

    for nature in range(array_length):
        nature_txt = single_line_array[nature]
        nature_txt_pattern = re.findall(r'[^ST\s][A-Za-z]+\s[A-Za-z]+\s',nature_txt)
        nature_array.append(nature_txt_pattern)

    # for incidentori in range(array_length):
        # incident_ori = single_line_array[incidentori]
        # incident_ori_pattern = re.findall(r'',incident_ori)
        # incident_ori_array.append(incident_ori_pattern)

    return(date_array)

def create_db():
    if os.path.exists("normanpd.db"):
        os.remove("normanpd.db")
    else:
        pass

    db = sqlite3.connect("normanpd.db")
    cursor_db = db.cursor()
    create_db_table = """CREATE TABLE incidents(
                         incident_time TEXT,
                         incident_number TEXT,
                         incident_location TEXT,
                         nature TEXT,
                         incident_ori TEXT
                         );"""
    cursor_db.execute(create_db_table)
    return(cursor_db)

def populate_db(cursor_db ,date_array):
    insert_incidents = "INSERT INTO incidents (incident_time) VALUES (?)"

    cursor_db.executemany(insert_incidents, date_array)

    cursor_db.execute("Select * FROM incidents")
    rows = cursor_db.fetchall()

    for r in rows:
        print(r)
