import numpy as np


def get_sector_points(sector_postcodes_full):
    sector_points = []
    for sector in sector_postcodes_full:
        sector_points.append((sector[1], sector[2]))
    print('Sector points are:', sector_points)
    return sector_points


def find_closest_sector(location, postcodes):
    """
    Adds the square of latitude difference to square of longitude difference and returns the index of the element with
    the smallest total distance
    """
    print('post code array: ', postcodes)
    print(' post codes array - location', postcodes - location)
    print(' distance squared:', (postcodes - location) ** 2)
    dist_2 = np.sum((postcodes - location) ** 2, axis=1)
    print('dist:', dist_2)
    print('argmin, dist:', np.argmin(dist_2), dist_2)
    return np.argmin(dist_2), dist_2


sector_postcodes_full = [('A', 1, 1), ('B', 2, 2), ('C', 3, 3)]
sector_points = get_sector_points(sector_postcodes_full)
locations = [(-12.3, 11.5), (4, 7), (1, 3), (3, 1)]
postcodes_array = np.asarray(sector_points)
for speedtest in locations:
    closest_sector = find_closest_sector(speedtest, postcodes_array)
    print(closest_sector, 'Type:', type(closest_sector), 'element:', closest_sector[0], 'postcode:', sector_points[closest_sector[0]])
    print('Your location is in sector:', sector_postcodes_full[closest_sector[0]][0])
    print('NEXT')


