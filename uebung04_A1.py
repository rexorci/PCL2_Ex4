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


def getfreqwords(indir, outfile, break_condition):
    """    
    :param indir: directory that contains the SAC-Xmls
    :param outfile: file to write in the most frequent sentences
    :param break_condition: (conditional) number of sentences to process
    :return: None
    """
    do_break = False
    try:
        do_break = type(int(break_condition)) is int
    except TypeError:
        pass
    break_counter = 0

    # we save the hash/string pairs in a file so we don't keep all the strings in memory
    tmp_file_hash_plus_string = 'TMP_hash_plus_string.txt'
    # dict contains the hashes of all sentences and the number of occurences
    sentence_hashes = {}

    with open(tmp_file_hash_plus_string, 'wb') as tmp_file:
        tmp_file.write(b'<?xml version="1.0" encoding="UTF-8"?><root>')
        # pattern to get all relevant files as a list
        pattern = indir + '/SAC-Jahrbuch_[0-9][0-9][0-9][0-9]_mul.xml'

        try:
            for file in glob.glob(pattern):
                tree = etree.parse(file)
                # this xpath gets all sentence-elements
                sentences = tree.xpath('/book/article/div/s')

                for sentence in sentences:
                    hash_count_sentence(sentence, sentence_hashes, tmp_file)
                    if do_break:
                        break_counter += 1
                        if break_counter > int(break_condition):
                            # we raise an exception because we need to break 2 for-loops
                            raise BreakCondition
        except BreakCondition:
            pass
        tmp_file.write(b'</root>')

    count = 0
    with open(outfile, 'w', encoding="utf-8") as result_file:
        # parse the temp file to find the most frequent strings by hash
        hashed_sentences = etree.parse(tmp_file_hash_plus_string)

        # sort the hashes by occurence (e.g. value)
        for hash_sentence in sorted(sentence_hashes.items(), key=operator.itemgetter(1), reverse=True):
            count += 1
            if count > 20:
                break
            else:
                # write most frequent sentences to outfile
                result_file.writelines(
                    hashed_sentences.xpath('(/root/sentence[@hash=%d]/@value)[1]' % hash_sentence[0])[0]
                    + '\n')

    # remove the tmp file
    if os.path.exists(tmp_file_hash_plus_string):
        os.remove(tmp_file_hash_plus_string)


def hash_count_sentence(sentence, sentence_hashes, tmp_file):
    """ 
    :param sentence: XML element representing a sentence
    :param sentence_hashes: dict that contains key-value-pairs with the hash of a sentence and the number of occurencies
    :param tmp_file: File to write in the sentence with the respective hash
    :return: None
    """
    # only sentences with minimum 6 tokens are relevant
    if len(sentence.xpath('w/@lemma')) >= 6:
        # concatenate the lemmata of the sentence and then return the hash value
        sentence_string = ' '.join(sentence.xpath('w/@lemma'))

        hash_sentence = hash(sentence_string)
        if hash_sentence not in sentence_hashes:
            sentence_hashes[hash_sentence] = 1
            # write the sentence into a temporary xml file to find the value later via hash
            el = etree.Element('sentence', hash=str(hash_sentence), value=sentence_string)
            tmp_file.write(etree.tostring(el))
        else:
            sentence_hashes[hash_sentence] += 1


class BreakCondition(Exception):
    """
    Helper exception, used to jump out of multiple loops
    """
    pass


def main():
    # Get the input and output filenames and encoding as commandline arguments
    parser = argparse.ArgumentParser(description='Find most frequent sentences.')
    parser.add_argument('--indir', '-i',
                        dest='indir',
                        help='directory that contains the XML files')

    parser.add_argument('--outfile', '-o',
                        dest="outfile",
                        help='output file')

    parser.add_argument('--breakcondition', '-b',
                        dest="break_condition",
                        required=False,
                        help='If a number is assigned, the program will stop analyzing after n-number of sentences')

    args = parser.parse_args()

    getfreqwords(args.indir, args.outfile, args.break_condition)

if __name__ == '__main__':
    main()
