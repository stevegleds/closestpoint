import numpy as np
import csv
import time  # todo : remove when code complete, only used to time the code for testing

SECTOR_FILE = 'sector_points.csv'  # this is used to map lat / long to sectors
CONSTITUENCY_FILE = 'constituency_points.csv'  # this is used to map lat / long of data points to constituency
RESULTS_FILE = 'updated_resultsfull_003.csv'  # this is the source file
UPDATED_RESULTS_FILE = 'updated_results_full_hg_003.csv'  # this is the output file with sector info
POSTCODE = "HG"

print('Sector Data file used is: ', SECTOR_FILE)
print('Input file used is:', RESULTS_FILE)
print('Output file will be:', UPDATED_RESULTS_FILE)


def parse(raw_file, delimiter=','):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    #  open csv file
    opened_file = open(raw_file)
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    #  csv_data object is now an iterator meaning we can get each element one at a time
    #  build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    for row in csv_data:
        if row[1] == "":  # there is no text in the field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))
            # Creates a new dict item for each row with col header as key and stores in a list
        #  city_count += 1
    # close csv file
    opened_file.close()
    return parsed_data


def save_results(raw_file, results):
    """
    :param raw_file: file to be created or updated with results
    :param results: the data to be saved to raw_file
    :return: nothing. File is saved and closed within the function
    """
    with open(raw_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Country Code', 'Date', 'Time', 'IpAddress', 'Latitude', 'Longitude',
                         'Download Speed', 'Upload Speed', 'Sector'])
        for item in results:
            writer.writerow([item['Country Code'], item['Date'], item['Date'], item['IpAddress'],
                             item['Latitude'], item['Longitude'],
                             item['Download Speed'] / 1024, item['Upload Speed'] / 1024,
                             item['Sector']])
    f.close()
    return


def is_good_speed(speed):
    return speed > 0


def filter_by_postcode(speedtest_results_data, postcode):
    """

    """
    new_results = []
    for speedtest in speedtest_results_data:
        speedtest['Download Speed'] = float(speedtest['Download Speed'])
        speedtest['Upload Speed'] = float(speedtest['Upload Speed'])
        if speedtest['Country Code'] == 'GB' and is_good_speed(speedtest['Download Speed']) and speedtest['Sector'].startswith(postcode):
            new_results.append(speedtest)
    return new_results


def main():
    # Get speedtest results data from the speedtest results file:
    speedtest_results_data = parse(RESULTS_FILE, ',')
    print(type(speedtest_results_data))
    filtered_results = filter_by_postcode(speedtest_results_data, POSTCODE)
    save_results(UPDATED_RESULTS_FILE, filtered_results)


if __name__ == "__main__":
    main()
