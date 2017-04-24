#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse
import random

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
            i=0
            for line in old_file:
                if i == n:
                    new_file.write(string+"\n")
                else:
                    new_file.write(line)
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def gettitles(infile_path, testfile_path, trainfile_path, k):
    """
    Gets a random sample of titles from the xml infile and writes it to the testfile,
    The remaining titles are written to the trainfile. Using Algorithm R as described in:
    Source: Vitter, Jeffrey S. (1 March 1985).
            Random sampling with a reservoir.
            ACM Transactions on Mathematical Software.
    """

    # We are only interested in elements that have the title tag.
    titles = filter(
        lambda event,elem: elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title',
        etree.iterparse(infile_path))

    testfile = testfile_path.open()

    # The first k title elements are initially written to the testfile
    i = 0
    for event, elem in titles[:k]:
        testfile.write(elem.text + "\n")
        i += 1
        elem.clear()  # discard the element

    close(testfile)

    trainfile = open(trainfile_path)

    # For the remaining elements, randomly replace an element of the testfile
    # with decreasing probability. If no element is replaced, the title is written
    # to the trainfile.
    for event, elem in titles[k+1:]:
        j = random.random(0, i)
        i += 1
        if j<k:
            write_to_line(testfile_path, j, elem.text)
        else:
            trainfile.write(elem.text + "\n")
        elem.clear()  # discard the element

    trainfile.close()


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

    gettitles(args.infile, args.testfile, args.trainfile, args.k)

if __name__ == '__main__':
    main()
