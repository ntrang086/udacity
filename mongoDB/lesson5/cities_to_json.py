from pymongo import MongoClient
import csv
import json
import io
import re
import pprint

CITIES = '../cities.csv'


field_map = {
    "name" : "name",
    "elevation": "elevation",
    "country_label": "country",
    "wgs84_pos#long": "lon",
    "wgs84_pos#lat": "lat",
    "isPartOf_label": "isPartOf",
    "timeZone_label": "timeZone",
    "populationTotal": "population" 
}

"""
from audit.py
'name': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]),
'elevation': set([<type 'NoneType'>, <type 'list'>, <type 'float'>]),
'country_label': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]),
'wgs84_pos#lat': set([<type 'NoneType'>, <type 'list'>, <type 'float'>]),
'wgs84_pos#long': set([<type 'NoneType'>, <type 'list'>, <type 'float'>])}
'isPartOf_label': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]),
'timeZone_label': set([<type 'NoneType'>, <type 'list'>, <type 'str'>]), 
'populationTotal': set([<type 'NoneType'>, <type 'list'>, <type 'int'>]),

"""


fields = field_map.keys()


def skip_lines(input_file, skip):
    for i in range(0, skip):
        next(input_file)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return v

"""
def strip_automobile(v):
    return re.sub(r"\s*\(automobile\)\s*", " ", v)

def strip_city(v):
    return re.sub(r"\s*\(city\)\s*", " ", v)


def mm_to_meters(v):
    if v < 0.01:
        return v * 1000
    return v

def clean_dimension(d, field, v):
    if is_number(v):
        if field == "weight":
            d[field] = float(v) / 1000.0
        else:
            d[field] = mm_to_meters(float(v))
    
def clean_year(d, field, v):
    d[field] = v[0:4]

def parse_array2(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return (True, v_array)
    return (False, v)

def ensure_not_array(v):
    (is_array, v) = parse_array(v)
    if is_array:
        return v[0]
    return v

def ensure_array(v):
    (is_array, v) = parse_array2(v)
    if is_array:
        return v
    return [v]

def ensure_float(v):
    if is_number(v):
        return float(v)

def ensure_int(v):
    if is_number(v):
        return int(v)


def ensure_year_array(val):
    #print "val:", val
    vals = ensure_array(val)
    year_vals = []
    for v in vals:
        v = v[0:4]
        v = int(v)
        if v:
            year_vals.append(v)
    return year_vals


def empty_val(val):
    val = val.strip()
    return (val == "NULL") or (val == "")

def years(row, start_field, end_field):
    start_val = row[start_field]
    end_val = row[end_field]

    if empty_val(start_val) or empty_val(end_val):
        return []

    start_years = ensure_year_array(start_val)
    if start_years:
        start_years = sorted(start_years)
    end_years = ensure_year_array(end_val)
    if end_years:
        end_years = sorted(end_years)
    all_years = []
    if start_years and end_years:
        #print start_years
        #print end_years
        for i in range(0, min(len(start_years), len(end_years))):
            for y in range(start_years[i], end_years[i]+1):
                all_years.append(y)
    return all_years


def process_file(input_file):
    input_data = csv.DictReader(open(input_file))
    autos = []
    skip_lines(input_data, 3)
    for row in input_data:
        auto = {}
        model_years = {}
        production_years = {}
        dimensions = {}
        for field, val in row.iteritems():
            if field not in fields or empty_val(val):
                continue
            if field in ["bodyStyle_label", "class_label", "layout_label"]:
                val = val.lower()
            val = strip_automobile(val)
            val = strip_city(val)
            val = val.strip()
            val = parse_array(val)
            if field in ["length", "width", "height", "weight", "wheelbase"]:
                clean_dimension(dimensions, field_map[field], val)
            elif field in ["modelStartYear", "modelEndYear"]:
                clean_year(model_years, field_map[field], val)
            elif field in ["productionStartYear", "productionEndYear"]:
                clean_year(production_years, field_map[field], val)
            else:
                auto[field_map[field]] = val
        if dimensions:
            auto['dimensions'] = dimensions
        auto['modelYears'] = years(row, 'modelStartYear', 'modelEndYear')
        auto['productionYears'] = years(row, 'productionStartYear', 'productionEndYear')
        autos.append(auto)
    return autos
"""

"""
# example of city data from https://www.udacity.com/course/viewer#!/c-ud032/l-760758686/e-815118775/m-833088552
{
    "_id" : ObjectId("52fe1d364b5ab856eea75ebc"),
    "elevation" : 1855,
    "name" : "Kud",
    "country" : "India",
    "lon" : 75.28,
    "lat" : 33.08,
    "isPartOf" : [
        "Jammu and Kashmir",
        "Udhampur district"
    ],
    "timeZone" : [
        "Indian Standard Time"
    ],
    "population" : 1140
}

field_map = {
    "name" : "name",
    "elevation": "elevation",
    "country_label": "country",
    "wgs84_pos#long": "lon",
    "wgs84_pos#lat": "lat",
    "isPartOf_label": "isPartOf",
    "timeZone_label": "timeZone",
    "populationTotal": "population" 
}
"""


#https://discussions.udacity.com/t/local-databases-for-unit-5-quizzes-and-homework/19764
infile = '../cities.csv'
outfile = '../cities.json'

with open(infile, "r") as filein:
    cities = []
    reader = csv.DictReader(filein)
    #skipping the extra metadata
    skip_lines(filein, 3)
    with open(outfile, "w") as fileout:
        linecount=0
        for line in reader:
            linecount+=1
            output={}
            elevation=0
            if line["elevation"] != 'NULL':
                elevation=int(float(line["elevation"]))
            output["elevation"]=elevation
            output["name"]=line["rdf-schema#label"]
            output["country"]=line["country_label"]
            lat=line["wgs84_pos#long"]
            if lat.startswith("{"):
                lat=lat.replace("{","")
                lat=lat.split("|")[0]
            output["lat"]=float(lat)
            lon=line["wgs84_pos#long"]
            if lon.startswith("{"):
                lon=lon.replace("{","")
                lon=lon.split("|")[0]
            output["lon"]=float(lon)
            #output["lon"]=float(line["wgs84_pos#long"])
            #output["lat"]=float(line["wgs84_pos#lat"])
            isPartOf=[]
            regions=line["isPartOf"]
            if regions != 'NULL':
                regions=regions.strip("{")
                regions=regions.strip("}")
                regions=regions.split("|")
                for region in regions:
                    region=region.split("/")[-1]
                    isPartOf.append(region.strip())
            output["isPartOf"]=isPartOf
            timeZone=line["timeZone"]
            timeZone=timeZone.split("/")[-1]
            output["timeZone"]=timeZone
            population=0
            if line["populationTotal"] != 'NULL':
                population=int(float(line["populationTotal"]))
            output["population"]=population
            json.dump(output,fileout)
            #pprint.pprint(output)
            #fileout.write(output)
            if linecount == 425:
                print str(output)





