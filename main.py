import argparse
import naturecounter
import sqlite3

def main(url):
    # Download incident pdf from website, extract incident data, and store in blank array
    incident_data = naturecounter.download_pdf(url)

    # Extract Incident Data and store in blank array
    incidents = naturecounter.extract_incidents(incident_data)

    # Create new database
    db = naturecounter.create_db()

    naturecounter.populate_db(db,incidents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--incidents", type=str, required=True, help="Incident summary url."
    )

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
