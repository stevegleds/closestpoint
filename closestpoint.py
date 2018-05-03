import numpy as np
import csv
import time  # todo : remove when code complete, only used to time the code for testing

SECTOR_FILE = 'sector_points.csv'  # this is used to map lat / long to sectors
RESULTS_FILE = 'map6pointsgb_edit_003.csv'  # this is the source file
UPDATED_RESULTS_FILE = 'updated_results_003_positive.csv'  # this is the output file with sector info

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
            writer.writerow([item['CountryCode'], item['Date'], item['DateTimeStamp'], item['IpAddress'],
                             item['Latitude'], item['Longitude'],
                             item['DownloadSpeed'] / 1024, item['UploadSpeed'] / 1024, item['Sector']])
    f.close()
    return


def get_coordinates(data):
    """
    :param data: full data on either postcode sector or speedtest result
    :return: list of only lat and lon needed for np arrays.
    These are in same order as the full data so that the 'winning' postcode can be found
    """
    coordinates = []
    for point in data:
            coordinates.append((float(point['Latitude']), float(point['Longitude'])))
    return coordinates


def find_closest_sector(location, postcodes):
    """
    Takes a single location and finds closest sector using postcodes np array
    dist_2 is an array containing the square of the distances to each sector postcode
    There is no need to take the sqrt because we only need to identify which sector is closest and
    therefore don't need the actual distance
    :param postcodes: a numpy array of lat and lon of all postcode sectors
    :param location: the lat / long of the result
    :return: the position of the 'winning' postcode sector in the postcodes array
    This will be used as the lookup value in the full sector data to get the postcode
    """
    dist_2 = np.sum((postcodes - location) ** 2, axis=1)
    return int(np.argmin(dist_2))


def has_a_postcode(lat, long):
    gb_north = 59
    gb_south = 49
    gb_east = 2
    gb_west = -7
    ni_north = 55
    ni_south = 54
    ni_east = -5.5
    ni_west = -8.5
    is_in_gb = (gb_south <= lat <= gb_north) and (gb_west <= long <= gb_east)
    is_in_ni = (ni_south <= lat <= ni_north) and (ni_west <= long <= ni_east)
    return is_in_gb and not is_in_ni


def is_good_speed(speed):
    return speed > 0


def get_closest_points(speedtest_results_data, sector_coordinates_array, sector_points_data):
    """
    Loops through the speedtest results and uses find_closest_sector() to find closest sector
    :param locations: the lat and lon of the speedtest results that need sector postcodes
    :param postcodes_array: array of lat and lon of postcode sectors
    :param sector_points_data:
    :return:
    """
    sectors = ['Sector']
    new_results = []
    for speedtest in speedtest_results_data:
        speedtest['Latitude'] = float(speedtest['Latitude'])
        speedtest['Longitude'] = float(speedtest['Longitude'])
        speedtest['DownloadSpeed'] = float(speedtest['DownloadSpeed'])
        speedtest['UploadSpeed'] = float(speedtest['UploadSpeed'])
        if speedtest['CountryCode'] == 'GB' and \
                has_a_postcode(speedtest['Latitude'], speedtest['Longitude']) and is_good_speed(speedtest['DownloadSpeed']):
            closest_sector = find_closest_sector((speedtest['Latitude'], speedtest['Longitude']),
                                                 sector_coordinates_array)
            sector_name = sector_points_data[closest_sector]['Postcode']
            sectors.append(sector_name)
            speedtest['Sector'] = sector_name
            new_results.append(speedtest)
    return sectors, new_results


def main():
    start = time.time()  # todo for testing only
    # Get postcode sector data from the postcode sector csv file:
    sector_data = parse(SECTOR_FILE, ',')
    print('Sector data prepared after ', time.time() - start, 'seconds')
    # Get speedtest results data from the speedtest results file:
    speedtest_results_data = parse(RESULTS_FILE, ',')
    print('Speedtest data prepared after ', time.time() - start, 'seconds')
    sector_coordinates = get_coordinates(sector_data)
    sector_coordinates_array = np.asarray(sector_coordinates)
    print('Sector array prepared after ', time.time() - start, 'seconds')
    sectors, results = get_closest_points(speedtest_results_data, sector_coordinates_array, sector_data)
    print('Results found after ', time.time() - start, 'seconds')
    save_results(UPDATED_RESULTS_FILE, results)
    end = time.time()
    print("the whole script took ", end - start, "seconds")


if __name__ == "__main__":
    main()
