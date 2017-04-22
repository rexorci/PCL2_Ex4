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


def getfreqwords(indir, outfile):
    # get all relevant files as a list
    pattern = indir + '/SAC-Jahrbuch_1864_mul.xml'
    # pattern = indir + '/SAC-Jahrbuch_[0-9][0-9][0-9][0-9]_mul.xml'

    # we save the hash/string pairs in a file so we don't keep all the strings in memory
    tmp_file_hash_plus_string = 'TMP_hash_plus_string.txt'

    sentence_hashes = {}
    for file in glob.glob(pattern):
        tree = etree.parse(file)
        sentences = tree.xpath('/book/article/div/s')

        for sentence in sentences:
            __hash_sentence(sentence, sentence_hashes, tmp_file_hash_plus_string)


    # sort the hashes by occurence (e.g. value)
    count = 0
    with open(outfile, 'w') as result_file:
        for hash_sentence in sorted(sentence_hashes.items(), key=operator.itemgetter(1), reverse=True):
            count += 1
            if count > 20:
                break
            else:
                result_file.writelines(str(hash_sentence[0]) + '\n')


    # write most frequent sentences to outfile

    # remove the tmp file
    if os.path.exists(tmp_file_hash_plus_string):
        os.remove(tmp_file_hash_plus_string)


def __hash_sentence(sentence, sentence_hashes, tmp_file_hash_plus_string):
    # concatenate the lemmata of the sentence and then return the hash value
    sentence_string = ''
    with open(tmp_file_hash_plus_string, 'ab') as tmp_file:
        for lemma in sentence.xpath('w/@lemma'):
            sentence_string += ' ' + lemma

        # only sentences with minimum 6 tokens are relevant
        if len(sentence.xpath('w/@lemma')) >= 6:
            hash_sentence = hash(sentence_string)
            if hash_sentence not in sentence_hashes:
                sentence_hashes[hash_sentence] = 1
                el = etree.Element('sentence', hash=str(hash_sentence), sentence=sentence_string)

                tmp_file.write(etree.tostring(el))
            else:
                sentence_hashes[hash_sentence] += 1


def main():
    # Get the input and output filenames and encoding as commandline arguments
    parser = argparse.ArgumentParser(description='Find most frequent sentences.')
    parser.add_argument('--indir', '-i',
                        dest='indir',
                        help='directory that contains the XML files')

    parser.add_argument('--outfile', '-o',
                        dest="outfile",
                        default='analysis_output.txt',
                        help='output file')

    args = parser.parse_args()

    getfreqwords(args.indir, args.outfile)

if __name__ == '__main__':
    main()
