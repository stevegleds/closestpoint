import csv
'''
Filters our results file by sector postcode and adds ward (sector) name to results using 'Unknown' for where no ward is found
'''
RESULTS_FILE = 'updated_resultsfull_003.csv'  # this is the source file
UPDATED_RESULTS_FILE = 'updated_results_full_hg_003.csv'  # this is the output file with sector info
WARD_INFO_FILE = 'sectorwardinfo.csv'
POSTCODE = "HG"
# Display information about which information is being used
print('Input file used is:', RESULTS_FILE)
print('Output file will be:', UPDATED_RESULTS_FILE)
print('We are looking for sectors with postcodes beginning with: ', POSTCODE)


def parse(raw_file, delimiter=','):
    """
    :Parses a raw CSV file to a JSON-line object.
    :param raw_file: probably csv file
    :param delimiter: specify delimiter but use '.' if none specified
    :return: parsed data
    """
    #  open csv file
    opened_file = open(raw_file)
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    #  csv_data object is now an iterator meaning we can get each element one at a time
    #  build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    print(fields)
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
    Saves the required data from the processed results
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
                             item['Download Speed'], item['Upload Speed'],
                             item['Sector'], item['Ward']])
    f.close()
    return


def is_good_speed(speed):
    '''
    We don't want negative or zero speeds because these have no meaning and must be errors
    :param speed: the speed from the results file (download or upload)
    :return: boolean. True if speed is non-zero
    '''
    return speed > 0


def filter_by_postcode(speedtest_results_data, postcode, ward_info):
    '''
    Filter the results file by postcode of sector and add ward_info to dictionaries
    :param speedtest_results_data: our results file
    :param postcode: the postcode of the sector we are  interested in
    :param ward_info: dictionary of wasds with postcode as keys
    :return: dictionary of filtered results including ward names
    '''

    new_results = []
    for speedtest in speedtest_results_data:
        speedtest['Download Speed'] = float(speedtest['Download Speed'])
        speedtest['Upload Speed'] = float(speedtest['Upload Speed'])
        if speedtest['Country Code'] == 'GB' and is_good_speed(speedtest['Download Speed']) and speedtest['Sector'].startswith(postcode):
            ward = ward_info[speedtest['Sector']]
            if ward == '0':
                ward = 'Unknown'
            speedtest['Ward'] = ward
            new_results.append(speedtest)
    return new_results


def create_ward_dict(ward_data, delimiter=','):
    '''
    Create dictionary of ward info so we can add to filtered results
    :param ward_data: file containing ward data
    :param delimiter: comma delimited by default
    :return: dictionary mapping postcode to ward
    '''
    opened_file = open(ward_data)
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    ward_dict = {}
    for row in csv_data:
        k = row[0]
        v = row[1]
        ward_dict[k] = v
    return ward_dict


def main():
    # Get speedtest results data from the speedtest results file:
    speedtest_results_data = parse(RESULTS_FILE, ',')
    # create dictionary of ward names
    ward_dict = create_ward_dict(WARD_INFO_FILE)
    # filter results by postcode and add ward name
    filtered_results = filter_by_postcode(speedtest_results_data, POSTCODE, ward_dict)
    # create csv file with processed results
    save_results(UPDATED_RESULTS_FILE, filtered_results)


if __name__ == "__main__":
    main()
