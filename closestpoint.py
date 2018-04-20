import numpy as np


def find_closest_sector(location, postcodes):
    postcodes = np.asarray(postcodes)
    dist_2 = np.sum((postcodes - location) ** 2, axis=1)
    return np.argmin(dist_2), dist_2

postcode_sectors = [(1,1), (2,2), (3,3)]
print(postcode_sectors[2])
location = [(2.3, 1.5)]

closest_sector = find_closest_sector(location, postcode_sectors)
print(closest_sector, 'Type:', type(closest_sector), 'element:', closest_sector[0], 'postcode:', postcode_sectors[closest_sector[0]])

