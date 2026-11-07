from bs4 import BeautifulSoup
from datetime import datetime
import logging
import os
import zipfile

# Function to read and parse the HTML file
def extract_values_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    specified_tags = soup.find_all('td', {'width': '55%', 'bgcolor': '#FFFFFF'})
    values = []
    
    for tag in specified_tags:
        font_tag = tag.find('font', {'color': '#550000', 'size': '3', 'face': "'Segoe UI', Verdana, sans-serif"})
        if font_tag:
            values.append(font_tag.text)
    
    return values

# Function to get the next available log file number
def get_next_log_number():
    log_number = 1
    while os.path.exists(f"extracted_values_log_{datetime.now().strftime('%Y%m%d')}_{log_number}.txt"):
        log_number += 1
    return log_number

# Build the path stored inside the ZIP, keeping the folder structure so files
# with the same name in different folders don't overwrite each other.
# e.g. C:\Data\Reports\a.txt -> C/Data/Reports/a.txt
#      \\server\share\a.txt  -> server/share/a.txt
def archive_name_for(file_path):
    drive, rest = os.path.splitdrive(os.path.abspath(file_path))
    drive = drive.replace(':', '').strip('\\/')
    parts = [p for p in drive.replace('\\', '/').split('/') + rest.replace('\\', '/').split('/') if p]
    return '/'.join(parts)

# Function to zip files from the latest log file
def zip_files_from_latest_log(log_filename):
    missing_files = []
    zipped_count = 0
    try:
        with open(log_filename, 'r', encoding='utf-8') as f:
            file_paths = f.readlines()

        # Strip whitespace, drop blank lines and repeated paths (keep order)
        file_paths = list(dict.fromkeys(path.strip() for path in file_paths if path.strip()))

        zip_filename = f"log_files_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                if os.path.isfile(file_path):
                    zipf.write(file_path, archive_name_for(file_path))
                    zipped_count += 1
                else:
                    missing_files.append(file_path)

        if missing_files:
            logging.warning(f"{len(missing_files)} files were missing and not added to the ZIP.")
            with open('not_found.txt', 'w', encoding='utf-8') as nf:
                for path in missing_files:
                    nf.write(f"{path}\n")

        # An empty ZIP is still ~22 bytes, so check what was added, not the file size
        if zipped_count == 0:
            os.remove(zip_filename)
            logging.warning("No files were zipped. ZIP file has not been created.")
        else:
            logging.info(f"{zipped_count} files zipped as {zip_filename}")

    except FileNotFoundError:
        logging.error(f"Log file {log_filename} not found.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    file_path = input("Please enter the path to the HTML file to be parsed: ").strip()
    extracted_values = extract_values_from_html(file_path)
    
    print(f"Number of lines found: {len(extracted_values)}")
    
    log_number = get_next_log_number()
    log_filename = f"extracted_values_log_{datetime.now().strftime('%Y%m%d')}_{log_number}.txt"
    
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        for line in extracted_values:
            log_file.write(f"{line}\n")
    
    logging.info(f"Output saved to {log_filename}")

    zip_choice = input("Do you want to zip the files listed in the latest log file? (yes/no): ").strip().lower()
    if zip_choice == 'yes':
        zip_files_from_latest_log(log_filename)
