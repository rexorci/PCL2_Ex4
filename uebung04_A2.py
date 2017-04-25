#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse
import random

from itertools import islice

import sys
from lxml import etree
from tempfile import mkstemp
from shutil import move
from os import remove, close


class BufferedFileWriter:

    def __init__(self, file_path, max_buffer_size, k):
        self.file_path = file_path
        self.max_buffer_size = max_buffer_size
        self.buffer = dict()
        file = open(self.file_path, 'a')
        for i in range(0,k):
            file.write("\n")
        file.close()

    def add(self, index, string):
        self.buffer[index] = string

        if sys.getsizeof(self.buffer) > self.max_buffer_size:
            self.writebuffer()

    def writebuffer(self):

        # Create temp file
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(self.file_path) as old_file:
                i = 0
                for line in old_file:
                    s = self.buffer.pop(i, None)
                    if s is None:
                        new_file.write(line)
                    else:
                        new_file.write(s + "\n")
                    i += 1

        close(fh)
        # Remove original file
        remove(self.file_path)
        # Move new file
        move(abs_path, self.file_path)


def clear_all(elem):
    """
    Clears an element and all empty references, adapted from source:
    Source: https://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    """
    # It's safe to call clear() here because no descendants will be accessed
    elem.clear()

    # Also eliminate now-empty references from the root node to our element
    for ancestor in elem.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]


def gettitles(infile_path, testfile_path, trainfile_path, k):
    """
    Gets a random sample of titles from the xml infile and writes it to the testfile,
    The remaining titles are written to the trainfile.
    Using an adapted version of Algorithm R as described in:
    Source: Vitter, Jeffrey S. (1 March 1985).
            Random sampling with a reservoir.
            ACM Transactions on Mathematical Software.
    """

    context = etree.iterparse(infile_path, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.10/}title')

    # For extremely large k, the list of random titles will get huge, so we write them to
    # the testfile file as soon as the list gets to big. (>4GB)
    writer = BufferedFileWriter(testfile_path, 4294967296, k)

    # The first k title elements are initially added to the list of random titles.
    # We discard the elements as soon as they were processed to reduce memory usage.
    i = 0
    for event, elem in islice(context, k):
        writer.add(i,elem.text)
        i += 1
        clear_all(elem)

    trainfile = open(trainfile_path,'a')

    # For the remaining elements, randomly replace an element of the testfile
    # with decreasing probability. If no element is replaced, the title is written
    # to the trainfile.
    for event, elem in context:
        j = random.randint(0, i)
        if j < k:
            writer.add(j, elem.text)
        else:
            trainfile.write(elem.text)
        i += 1
        clear_all(elem)

    trainfile.close()

    writer.writebuffer()

def main():
    # Get the input and output filenames as well as sample size from commandline
    parser = argparse.ArgumentParser(description='Choose k random titles from dump')
    parser.add_argument('--infile', '-i',
                        dest='infile',
                        help='input xml file')

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
