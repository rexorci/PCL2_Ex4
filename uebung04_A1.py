#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 4, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738
import argparse, glob
from lxml import etree


def getfreqwords(indir, outfile):
    # get all relevant files as a list
    pattern = indir + '/SAC-Jahrbuch_1946_mul.xml'
    # pattern = indir + '/SAC-Jahrbuch_[0-9][0-9][0-9][0-9]_mul.xml'
    print('bla')
    for file in glob.glob(pattern):
        tree = etree.parse(file)
        sentences = tree.xpath('/book/article/div/s')
        print(len(sentences))
        for sentence in sentences:
            __lemmatize_sentences(sentence)
            print('--------------')

        # code from lecture:
        # with open(file) as infile, open(outfile, 'w') as outfile:
        #     sentence_hashes = set()
        #     for sentence in infile:
        #         sentence_hash = hash(sentence)
        #         if sentence_hash not in sentence_hashes:
        #         sentence_hashes.add(sentence_hash)
        #         trg.write(sentence)


    # get 20 most frequent sentences (with >= 6 tokens)

    # write most frequent sentences to outfile


def __lemmatize_sentences(sentence):
    # create lemmatised sentences
    for lemma in sentence.xpath('w/@lemma'):
        print(lemma)
    #yield sentence

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
