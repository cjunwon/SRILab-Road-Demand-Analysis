import requests
import time
import gzip
import shutil

lodes_url_base = "https://lehd.ces.census.gov/data/lodes/LODES8/ca/od/ca_od_main_JT00_"

while True:
    # promt string input from user for year
    year = input("Enter year: ")
    # append year to base url
    lodes_url = lodes_url_base + year + ".csv.gz"
    
    # check if url exists, if so, download and unzip
    r = requests.head(lodes_url)
    if r.status_code == 200:
        print("LEHD Origin-Destination Employment Statistics (LODES) for " + year + " exists. To download, press enter.")
        input()
        # download file
        print("Downloading...")
        download_start = time.time()
        r = requests.get(lodes_url, allow_redirects=True)
        open('ca_od_main_JT00_' + year + '.csv.gz', 'wb').write(r.content)
        download_end = time.time()
        print("Downloaded in: " + str((download_end - download_start)/60) + " minutes")

        # unzip file
        print("Unzipping...")
        unzip_start = time.time()
        with gzip.open('ca_od_main_JT00_' + year + '.csv.gz', 'rb') as f_in:
            with open('../lodes_od_data/ca_od_main_JT00_' + year + '.csv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        unzip_end = time.time()
        print("Unzipped in: " + str((unzip_end - unzip_start)/60) + " minutes")
        print("CSV file saved to: ../lodes_od_data/ca_od_main_JT00_" + year + ".csv")
        break  # Exit the loop when the file is successfully downloaded and unzipped
    
    else:
        print("LEHD Origin-Destination Employment Statistics (LODES) for " + year + " does not exist. Please enter a valid year.")
        year = input("Enter year: ")