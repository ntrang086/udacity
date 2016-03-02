# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the stations
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file or below
"""
Station|Year|Month|Day|Hour|Max Load
COAST|2013|01|01|10|12345.6
EAST|2013|01|01|10|12345.6
FAR_WEST|2013|01|01|10|12345.6
NORTH|2013|01|01|10|12345.6
NORTH_C|2013|01|01|10|12345.6
SOUTHERN|2013|01|01|10|12345.6
SOUTH_C|2013|01|01|10|12345.6
WEST|2013|01|01|10|12345.6
"""


import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "../2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    data = {}
    i = 1
    while i < 9:
        station_vals = sheet.col_values(i, start_rowx=1, end_rowx=None) # Returns a slice of the values of the cells in the given column.
        station = sheet.cell_value(0, i)
        maxval = max(station_vals)
        maxpos = station_vals.index(maxval) + 1
        maxtime = xlrd.xldate_as_tuple(sheet.cell_value(maxpos, 0), 0)
        data[station] = {'Max Load': maxval, 'Year': maxtime[0], 'Month': maxtime[1], 'Day': maxtime[2], 'Hour': maxtime[3]}
        i += 1
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'w') as f:
        fields = ['Station','Year','Month','Day','Hour','Max Load']
        writer = csv.writer(f, delimiter="|") 
        writer .writerow(fields)
        for key in data:
            writer.writerow([key, data[key][fields[1]], data[key][fields[2]], data[key][fields[3]], \
                data[key][fields[4]], data[key][fields[5]]])
"""
    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)
"""
        
if __name__ == "__main__":
    data = parse_file(datafile)
    save_file(data, 'excel_csv.csv')
