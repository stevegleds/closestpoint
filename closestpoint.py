import numpy as np
import csv

RUN_FILE = 'sector_points_100.csv'  # this is a test file
RESULTS_FILE = 'results.csv'
print('Data file used is: ', RUN_FILE)


def parse(raw_file, delimiter):
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
        if row[0] == "":  # there is no text in the field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))  # Creates a new dict item for each row with col header as key and stores in a list
        #  city_count += 1
    #  print("data list is: ", parsed_data)
    #  print("Type of parsed_data is: ", type(parsed_data))
    # close csv file
    opened_file.close()
    return parsed_data

def get_sector_points(sector_postcodes_full, source_type):
    sector_points = []
    if source_type == 'csv':
        pass
    else:
        for sector in sector_postcodes_full:
            sector_points.append((sector[1], sector[2]))
        # print('Sector points are:', sector_points)
        return sector_points


def find_closest_sector(location, postcodes):
    """
    Adds the square of latitude difference to square of longitude difference and returns the index of the element with
    the smallest total distance
    """
    # print('post code array: ', postcodes)
    # print(' post codes array - location', postcodes - location)
    # print(' distance squared:', (postcodes - location) ** 2)
    dist_2 = np.sum((postcodes - location) ** 2, axis=1)
    # print('dist:', dist_2)
    # print('argmin, dist:', np.argmin(dist_2), dist_2)
    return np.argmin(dist_2), dist_2


def main():
    # Call our parse function with required file an delimiter
    sector_points_data = parse(RUN_FILE, ',')
    print(sector_points_data)
    print("keys are:", sector_points_data[0].keys())
    sector_postcodes_full = [('A', 1, 1), ('B', 2, 2), ('C', 3, 3)]
    sector_points = get_sector_points(sector_postcodes_full, 'list')
    # sector_points = get_sector_points(sector_postcodes_full, 'csv')
    locations = [(-12.3, 11.5), (4, 7), (1, 3), (3, 1)]
    postcodes_array = np.asarray(sector_points)
    for speedtest in locations:
        closest_sector = find_closest_sector(speedtest, postcodes_array)
        # print(closest_sector, 'Type:', type(closest_sector), 'element:', closest_sector[0], 'postcode:', sector_points[closest_sector[0]])
        print('Your location is in Sector:', sector_postcodes_full[closest_sector[0]][0])
        print('NEXT')


if __name__ == "__main__":
    main()
