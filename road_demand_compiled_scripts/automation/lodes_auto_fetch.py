import requests
import time
import gzip
import shutil

# function to download and unzip lodes data
def download_and_unzip(year, lodes_url_base):
    lodes_url = lodes_url_base + str(year) + ".csv.gz"
    r = requests.head(lodes_url)
    if r.status_code == 200:
        print("LEHD Origin-Destination Employment Statistics (LODES) for " + str(year) + " exists. To download, press enter.")
        input()
        # download file
        print("Downloading...")
        download_start = time.time()
        r = requests.get(lodes_url, allow_redirects=True)
        open('ca_od_main_JT00_' + str(year) + '.csv.gz', 'wb').write(r.content)
        download_end = time.time()
        print("Downloaded in: " + str((download_end - download_start)/60) + " minutes")

        # unzip file
        print("Unzipping...")
        unzip_start = time.time()
        with gzip.open('ca_od_main_JT00_' + str(year) + '.csv.gz', 'rb') as f_in:
            with open('../lodes_od_data/ca_od_main_JT00_' + str(year) + '.csv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        unzip_end = time.time()
        print("Unzipped in: " + str((unzip_end - unzip_start)/60) + " minutes")
        print("CSV file saved to: ../lodes_od_data/ca_od_main_JT00_" + str(year) + ".csv")
        return True
    else:
        return False

# base url for lodes data
lodes_url_base = "https://lehd.ces.census.gov/data/lodes/LODES8/ca/od/ca_od_main_JT00_"

# fetch current year
year = time.localtime().tm_year

# check if current year exists and download if it does
while True:
    if download_and_unzip(year, lodes_url_base):
        break
    else:
        print("LEHD Origin-Destination Employment Statistics (LODES) for " + str(year) + " does not exist. Checking for " + str(year - 1) + "...")
        year -= 1