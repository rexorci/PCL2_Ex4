#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse

def getfreqwords(indir, outfile):
    pass


def main():
    #Get the input and output filenames and encoding as commandline agruments
    parser = argparse.ArgumentParser(description='Find most frequent sentences.')
    parser.add_argument('--indir','-i',
                        dest='indir',
                        help='directory that contains the XML files')

    parser.add_argument('--outfile','-o',
                        dest="outfile",
                        default='analysis_output.txt',
                        help='output file')

    args = parser.parse_args()

    getfreqwords(args.indir, args.outfile)

if __name__ == '__main__':
    main()
