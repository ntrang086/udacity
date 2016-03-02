import xlrd
import sys
datafile = "2013_ERCOT_Hourly_Load_Data.xls"



def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    maxvalue = 0
    maxrow = 0
    minvalue = sys.maxint
    minrow = 0
    totalCoast = 0

    
    data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)]
    print data[0]
    """
    print "\nList Comprehension"
    print "data[3][2]:",
    print data[3][2]

    print "\nCells in a nested loop:"    
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if row == 50:
                print sheet.cell_value(row, col),


    ### other useful methods:
    print "\nROWS, COLUMNS, and CELLS:"
    print "Number of rows in the sheet:", 
    print sheet.nrows
    print "Type of data in cell (row 3, col 2):", 
    print sheet.cell_type(3, 2)
    print "Value in cell (row 3, col 2):", 
    print sheet.cell_value(3, 2)
    print "Get a slice of values in column 3, from rows 1-3:"
    print sheet.col_values(3, start_rowx=1, end_rowx=4)

    print "\nDATES:"
    print "Type of data in cell (row 1, col 0):", 
    print sheet.cell_type(1, 0)
    exceltime = sheet.cell_value(1, 0)
    print "Time in Excel format:",
    print exceltime
    print "Convert time to a Python datetime tuple, from the Excel float:",
    print xlrd.xldate_as_tuple(exceltime, 0)

    """
    for r in range(1, sheet.nrows): # don't read the header
        if maxvalue < sheet.cell_value(r, 1):
            maxvalue = sheet.cell_value(r, 1)
            maxrow = r
        if minvalue > sheet.cell_value(r, 1):
            minvalue = sheet.cell_value(r, 1)
            minrow = r
        totalCoast += sheet.cell_value(r, 1)
    
    data = {
            'maxtime': xlrd.xldate_as_tuple(sheet.cell_value(maxrow, 0), 0),
            'maxvalue': maxvalue,
            'mintime': xlrd.xldate_as_tuple(sheet.cell_value(minrow, 0), 0),
            'minvalue': minvalue,
            'avgcoast': totalCoast/(sheet.nrows-1)
    }
    return data


def test():
    data = parse_file(datafile)
    print data

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18770.166858114, 10)


test()