#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse
import glob
import operator
import os
from lxml import etree


def gettitles(infile, testfile, trainfile, k):
    abc = 1

def main():
    # Get the input and output filenames aswell as sample size from commandline
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
