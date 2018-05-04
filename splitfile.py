"""
Takes a large file and splits into smaller files
"""
import os


def split_file(filename, pattern, size):
    """
    Split a file into multiple output files.
    :param filename is the source file
    :param pattern is the pattern to be used to name the output files
    :param size is the max number of lines per file
    The first line of filename should be a header line that is copied to
    every output file.
    The remaining lines are split into blocks of at least 'size' lines and written to output files whose names
    are pattern.format(1), pattern.format(2), and so on.
    The last output file may be short.
    """
    with open(filename, 'r') as f:
        header = next(f)
        print(header)
        for index, line in enumerate(f, start=1):
            with open(pattern.format(index), 'w') as out:
                # out.write(header)
                n = 0
                for line in f:
                    if "GB" in line:
                        out.write(line)
                        n += 1
                    if n >= size:
                        break
            print(pattern.format(index))


if __name__ == '__main__':
    source_filename = 'map6points.csv'  # this is full list of subscribers from OpenEMM
    destination_filename = 'map6pointsgb'
    source_file = os.path.join('', source_filename)
    print('Source file is:', source_file)
    pattern = destination_filename + '_split_{0:03d}.csv'
    split_file(source_file, pattern, 1000000)