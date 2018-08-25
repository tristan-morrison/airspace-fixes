import csv
import sys
import json

import os

cwd = os.getcwd()


def minsToDegrees (minsString, isLongitude):
    parts = minsString.split("-")

    parts[0] = float(parts[0])
    parts[1] = float(parts[1])
    parts[2] = float(parts[2][:parts[2].find(" ")])

    degrees = parts[0] + (parts[1] / 60) + (parts[2] / 3600)

    # If this is a longitude value, it is x degrees West, so it needs to be multiplied by negative one, since West values are negative
    # Note: automatically applying this multiplication on any longitude value only works because all of the values we are processing are in North America, so all values are West of the prime meridian. If we were processing values worldwide, we would have to actually read the "W" or "E" character and apply the multiplication only for if the char read is "W"
    if isLongitude:
        degrees *= -1

    return degrees

# for each directory in the cwd
for name in os.listdir(cwd):
    if os.path.isdir(name) and name != '.git':
        fixes = list()

        # for each file in this directory
        for filename in os.listdir(name):
            # open the file
            with open(cwd + '/' + name + '/' + filename, 'r+') as file:
                fixes = fixes + json.load(file)

        outfilename = name + ".csv"
        with open(outfilename, 'w') as csvFile:
            headers = ['name', 'latitude', 'longitude', 'state', 'artcc', 'type', 'updated']
            writer = csv.DictWriter(csvFile, fieldnames=headers)

            writer.writeheader()

            for row in fixes:
                # convert the lat and long coordinates to degrees
                row['latitude'] = minsToDegrees(row['latitude'], False)
                row['longitude'] = minsToDegrees(row['longitude'], True)

                writer.writerow(row)
