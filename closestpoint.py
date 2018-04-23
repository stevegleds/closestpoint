import numpy as np
import csv
import time #todo : remove when code complete, only used to time the code for testing

SECTOR_FILE = 'sector_points.csv'  # this is a test file
RESULTS_FILE = 'mappointsample1000.csv'
print('Data file used is: ', SECTOR_FILE)


def parse(raw_file, delimiter=','):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter #TODO add default arg : ','
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    #  open csv file
    opened_file = open(raw_file)
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    #  csv_data object is now an iterator meaning we can get each element one at a time
    print(csv_data)
    #  build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    for row in csv_data:
        if row[1] == "":  # there is no text in the field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))  # Creates a new dict item for each row with col header as key and stores in a list
        #  city_count += 1
    #  print("data list is: ", parsed_data)
    #  print("Type of parsed_data is: ", type(parsed_data))
    # close csv file
    opened_file.close()
    return parsed_data


def save_results(raw_file, results):
    '''
    :param raw_file: file to be created or updated with results
    :param results: the data to be saved to raw_file
    :return: nothing. File is saved and closed within the function
    '''
    #  results_file = open(raw_file, 'w')
    with open(raw_file, "w") as f:
        writer = csv.writer(f)
        writer.writerows(results)
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
    There is no need to take the sqrt because we only need to identify which sector is closest and therefore don't need the actual distance
    :param postcodes: a numpy array of lat and lon of all postcode sectors
    :return: the position of the 'winning' postcode sector in the postcodes array
    This will be used as the lookup value in the full sector data to get the postcode
    """
    dist_2 = np.sum((postcodes - location) ** 2, axis=1)
    print("Your points are:", postcodes[np.argmin(dist_2)], 'in position:', np.argmin(dist_2), type(np.argmin(dist_2)))
    return int(np.argmin(dist_2))


def get_closest_points(locations, postcodes_array, sector_points_data):
    """
    Loops through the speedtest results and uses find_closest_sector() to find closest sector
    :param locations: the lat and lon of the speedtest results that need sector postcodes
    :param postcodes_array: array of lat and lon of postcode sectors
    :param sector_points_data:
    :return:
    """
    for speedtest in locations:
        closest_sector = find_closest_sector(speedtest, postcodes_array)
        print('Index from array:', type(closest_sector))
        print('Your location is in Sector:', sector_points_data[closest_sector]['Postcode'])
        print('Your location:', speedtest)
        print('Your sector location:', sector_points_data[closest_sector])
        print('NEXT')

def main():
    # Get postcode sector data from the postcode sector csv file:
    sector_data = parse(SECTOR_FILE, ',')
    # Get speedtest results data from the speedtest results file:
    speedtest_results_data = parse(RESULTS_FILE, ',')
    speedtest_results_coordinates = get_coordinates(speedtest_results_data)
    locations = [(57.11, -2.1), (57.1579, -2.09048), (57.13, -2.13), (3, 1)]
    start = time.time()  # todo for testing only
    sector_coordinates = get_coordinates(sector_data)
    sector_coordinates_array = np.asarray(sector_coordinates)
    get_closest_points(speedtest_results_coordinates, sector_coordinates_array, sector_data)
    end = time.time()
    print("the code took ", start - end, "seconds")
    print(speedtest_results_coordinates)


if __name__ == "__main__":
    main()
