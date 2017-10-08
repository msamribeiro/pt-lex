#!/usr/bin/python

"""
Validates lexicon.
Checks for valid phones, syllable structure, stress absense,
stress position or empty lines.
"""

import yaml
import logging
import argparse
import codecs

def validate_lexicon(lexicon, phoneset, top=None):

    # read phoneset
    handler = open(phoneset, 'r')
    data = handler.read()
    data = yaml.load(data)
    handler.close()
    phoneset = data['phoneset'].keys()
    vowels = []
    for phone in phoneset:
        if data['phoneset'][phone]['type'] == 'vowel':
            vowels.append(phone)

    entries = 0
    errors = 0
    lineno = 0
    words = set([])

    fid = codecs.open(lexicon, encoding='utf-8')
    for line in fid:
        line = line.rstrip()
        entries += 1
        lineno += 1

        # check for empty line
        if not line:
            logging.info('Line %i. Found empty line' % (lineno))
            errors += 1
            continue

        # check for valid word:value format
        line = line.split()
        word, value = line[0], ' '.join(line[1:])
        if len(word) == 0 or len(value) == 0:
            logging.info('Line %i. Invalid word:value pair' %  (lineno))
            errors += 1
            continue

        # check for repeated entries
        if word in words:
            logging.info('Line %i. Repeated word: %s' % (lineno, word))
            errors += 1
        else:
            words.add(word)

        # check for stress presence
        stress = value.count('1')
        if stress == 0:
            logging.info('Line %i. No stress found' %  (lineno))
            errors += 1
        elif stress > 1:
            logging.info('Line %i. More than one stress found' %  (lineno))
            errors += 1

        # check for valid phones
        phones = value.replace('1', '')
        phones = phones.replace('2', '')
        phones = phones.replace('-', '')
        phones = phones.split()
        for phone in phones:
            if phone not in phoneset:
                logging.info('Line %i. Invalid phone found: %s' % (lineno, phone))
                errors += 1

        # check for syllable structure
        syllables = value.split('-')
        for syl in syllables:
            syl_phones = syl.split()
            nuclei = sum([v in syl_phones for v in vowels])
            if nuclei > 1:
                logging.info('Line %i. More than one nucleus in syllable %s' % (lineno, syl))
                errors += 1
            elif nuclei < 1:
                logging.info('Line %i. No nucleus in syllable %s' % (lineno, syl))
                errors += 1

        # check for valid stress position
        for syl in syllables:
            if '1' in syl:
                if syl.split()[-1] != '1':
                    logging.info('Line %i. Stress does not occur at end of syllable %s' % (lineno, syl))
                    errors += 1

        # check for extra spaces
        if '  ' in value:
            logging.info('Line %i. Found extra spaces' %  (lineno))
            errors += 1

        # check for other sytax errors
        if '1-' in value:
            logging.info('Line %i. Invalid stress position' % (lineno))
            errors += 1

        if top:
            if entries > top:
                break
    fid.close()
    logging.info('Found %i entries and %i errors' % (entries, errors))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lexicon", help="lexicon to validate", required=True)
    parser.add_argument("-p", "--phoneset", help="phoneset in YAML format", required=True)
    parser.add_argument("-t", "--top", help="Validate top N entries only", type=int, required=False)
    
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    validate_lexicon(args.lexicon, args.phoneset, args.top)
