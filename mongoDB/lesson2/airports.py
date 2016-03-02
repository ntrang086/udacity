#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        airports = soup.find(id="AirportList").find_all("option")  # find the tag with AirportList and then find the option list
        count = 0
        for airport in airports:
            if len(airport['value']) == 3 and airport['value'] != 'All':
                data.append(airport['value'])
                count += 1
    print count
    data.sort()
    print data
    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 1167
    assert "ATL" in data
    assert "ABR" in data

test()