import naturecounter
import docs
import sqlite3

def test_download_pdf(filename = 'docs/2023-01-31_daily_incident_summary.pdf'):

    file = naturecounter.download_pdf(filename)
    assert len(file.pages) == 18

def test_extract_incidents(filename = 'docs/2023-01-31_daily_incident_summary.pdf', term = '1/31/2023 0:12'):

    file = naturecounter.download_pdf(filename)
    nature = naturecounter.extract_incidents(file)

    if nature:
        assert True
    else: False

def test_populate_db(db = 'normanpd.db'):

    test_db = sqlite3.connect(db)
    test_cursor = test_db.cursor()

    if test_cursor.execute("SELECT * FROM incidents") == 1:
        True
    else:
        False
