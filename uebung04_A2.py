#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse
import random

from itertools import islice
from lxml import etree
from tempfile import mkstemp
from shutil import move
from os import remove, close


def write_to_line(file_path, n, string):
    """
    Writes to a specific line of a file.
    Source:
    http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
    """

    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            i = 0
            for line in old_file:
                if i == n:
                    new_file.write(string+"\n")
                else:
                    new_file.write(line)
                i += 1
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def write_to_newline(file_path, string):
    file = open(file_path, 'w')
    file.write(string + "\n")
    file.close()

def gettitles(infile_path, testfile_path, trainfile_path, k):
    """
    Gets a random sample of titles from the xml infile and writes it to the testfile,
    The remaining titles are written to the trainfile.
    Using an adapted version of Algorithm R as described in:
    Source: Vitter, Jeffrey S. (1 March 1985).
            Random sampling with a reservoir.
            ACM Transactions on Mathematical Software.
    """

    # We are only interested in elements that have the title tag.
    # Ugly ass python 3
    titles = filter(
        lambda tuple: tuple[1].tag == '{http://www.mediawiki.org/xml/export-0.10/}title',
        etree.iterparse(infile_path))


    # The first k title elements are initially written to the testfile.
    # We discard the elements as soon as they were processed to reduce memory usage.
    i = 0
    for event, elem in islice(titles, k):
        write_to_newline(testfile_path, elem.text)
        i += 1
        elem.clear()  # discard the element


    # For the remaining elements, randomly replace an element of the testfile
    # with decreasing probability. If no element is replaced, the title is written
    # to the trainfile.
    for event, elem in islice(titles, k+1, None):
        j = random.randint(0, i)
        if j < k:
            write_to_line(testfile_path, j, elem.text)
        else:
            write_to_newline(trainfile_path, elem.text)
        i += 1
        elem.clear()  # discard the element



def main():
    # Get the input and output filenames as well as sample size from commandline
    parser = argparse.ArgumentParser(description='Find most frequent sentences.')
    parser.add_argument('--infile', '-i',
                        dest='infile',
                        help='directory that contains the XML files')

    parser.add_argument('--testfile', '-o',
                        dest="testfile",
                        help='output testfile containing k random titles')

    parser.add_argument('--trainfile', '-t',
                        dest="trainfile",
                        help='output trainfile containing the rest of the titles')

    parser.add_argument('--samplesize', '-k',
                        dest="k",
                        help='Number of random titles to choose from all xml elements')

    args = parser.parse_args()

    gettitles(args.infile, args.testfile, args.trainfile, int(args.k))

if __name__ == '__main__':
    main()
