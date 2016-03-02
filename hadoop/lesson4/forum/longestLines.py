#!/usr/bin/python
import sys
import csv


"""
Your mapper function should print out 10 lines containing longest posts, sorted in
ascending order from shortest to longest.
"""


def mapper(inputFile, outputFile):
    with open(inputFile,'rb') as tsvin, open(outputFile, 'wb') as csvout:
        reader = csv.reader(tsvin, delimiter='\t')
        writer = csv.writer(csvout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
        line_list = []
        first_line = True
        for line in reader:
            if first_line:  #skip first line
                first_line = False
                continue
            line_list.append(line)
        line_list.sort(key = lambda x: len(x[4]), reverse = True)
        for line in reversed(line_list[0:10]):
            writer.writerow(line)

       
# This function allows you to test the mapper with the provided test string
def main():
    print "start"
    mapper('forum_node.tsv', 'forum_longest_lines.csv')
    print "done"

if __name__ == "__main__":
    main()