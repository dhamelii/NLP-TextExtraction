Darren "Chas" Hamel

HOW TO RUN PROJECT 0:
    Access https://www.normanok.gov/public-safety/police-department/crime-prevention-data/daily-activity-reports
    Download a daily incident summary pdf, such as '2023-31-01_daily_incident_summary.pdf' and store it in the programs 'docs' folder.
    Note the file name, and using Pipenv, execute the following:
        pipenv run python main.py --incidents <filepath in docs folder>

    As an example, this program can be run using the following command:
        pipenv run python main.py --incidents ~/cs5293sp23-project0/docs/2023-01-31_daily_incident_summary.pdf



PROGRAM METHODOLOGY
    There are four methods stored in the naturecounter.py file.
        download_pdf -> This method extracts the downloaded file from the file path given, and queues it for use.

        extract_incidents -> This method takes the pdf from download_pdf method and extracts text from each page. After extraction, the program
                             will segregate each line element into its own element based on the '\n' separator. These single line incidents
                             are then stored into an array (single_line_array). To clean the data, the PDF Header, Footer, and Column names
                             are removed.
   
                             With the single_line_arry, we now create sub arrays for each columns of our database table (date, incident number,
                             location, nature, incident ORI). For each of these arrays, we use regular expressions on the single_line_array to extract
                             the specific data needed for each sub array. 

        create_db -> This method first looks if a database named "normanpd.db" exists in the project folder, if yes, it is removed. If not,
                     the method continues. By accessing SQLite3, we connect to the system and create a database titled "normanpd.db" with
                     a schema of columns for each column in the PDF (incident_time, incident_number, incident_location, nature, and incident_ori).
                     This schema is then executed into the database.

        populate_db -> This method functions to input incidents extract_incidents method into the database created in the create_db method.
                       Using the executemany() command, we push a zipped array containing elements from the sub arrays created in the
                       extract_incidents method into the normanpd.db. After all items have been pushed, we confirm success by printing the
                       database.   


TEST METHODS
    In our test file, we are testing the funtionality of the download_pdf, extract_incidents, and populate_db methods.

    test_download_pdf -> To confirm success, we pull the '2023-01-31_daily_incident_summary.pdf' from the project docs folder and use pypdf
                         to read the file. Using the len() command, we can confirm if the pdf is of the correct number of pages.

    test_extract_incidents -> This method returns a zipped list / array of the sub arrays described in the method methodology in the previous
                         section. To confirm that this method is sucessful, we return TRUE if the array is NOT empty, and FALSE if it IS EMPTY.

    test_populate_db -> This method returns a database that is populated with the list of extracted incidents. To confirm the method works, we 
                        return TRUE if the database is exectued and commited, or FALSE if it is not.


BUGS AND ASSUMPTIONS
    The main issue that I had in development was in  the extract_incidents method. I was able to successfully extract each line of incidents
    from the summary PDF. Each line was then able to be given its own list element, but, as I began to use regular expressions to separate
    the incident line to the independant categories (date/time, incident number, etc) I ran into significant issues.

    The first two columns were simple as they contained a constant scheme of digits and special characters. As I moved on to the address and
    nature columns, I could not establish a good regex scheme that would work consistently.

    In light of this, the only data that is pushed to the data base is the incident_time information.
