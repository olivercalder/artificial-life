import sys
import os
import random


def print_help_string():
    print('''
Usage: python3 {} [arguments]

Arguments:
    -h              Print help string
    -c count        Number of prior words upon which to base next word
    -w words        Number of words to generate
    -t filename(s)  Files from which to load sample text
    -p              Preserve punctuation and capitalization
    -f              Flow of words: No sentence breaks
    -s              Silent: Does not print generated words to console
    -o filename     Write output to specified filename
'''.format(sys.argv[0]))


def load_lines(filename):
    lines = []
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.rstrip('\n').rstrip(' ')
            if line:
                lines.append(line)
    return lines


def create_directory(directory):
    if not os.path.isdir(directory):
        path = directory.rstrip('/').split('/')
        for i in range(len(path)):
            path_chunk = '/'.join(path[:i+1])
            if not os.path.isdir(path_chunk):
                os.mkdir(path_chunk)


def write_text(text_string, filename):
    path = filename.split('/')
    if len(path) > 1:
        directory = '/'.join(path[:-1])
        create_directory(directory)
    with open(filename, 'w') as outfile:
        print(text_string, file=outfile)


def simplify_lines(lines, preserve=False, sentences=True):
    simplified = []
    for line in lines:
        line = line.rstrip(' ').rstrip('\n')
        if line and line[:4] != 'BOOK' and line[:3] != 'THE' and line[:4] != '----':
            if not preserve:
                line = line.lower().rstrip('\n')
                if not sentences:
                    line = line.replace('.', '')
                    line = line.replace('?', '')
                    line = line.replace('!', '')
                line = line.replace(',', '')
                line = line.replace(';', '')
                line = line.replace('"', '')
                line = line.replace(':', '')
                line = line.replace('-', ' ')
                line = line.replace('   ', ' ')
                line = line.replace('  ', ' ')
            simplified.append(line)
    return simplified


def get_words(lines, sentences=True):
    words = []
    for line in lines:
        words += line.rstrip(' ').split(' ')
    if sentences:
        new_words = []
        new_words.append(words[0].capitalize())
        for i in range(1, len(words)):
            if words[i].lower() == 'i' or words[i].lower() == 'o' or words[i-1][-1] == '.' or words[i-1][-1] == '?.' or words[i-1][-1] == '!':
                new_words.append(words[i].capitalize())
            else:
                new_words.append(words[i])
        words = new_words
    return words


def build_dictionary(words, count=3):
    dictionary = {}
    total_words = len(words)
    for i in range(count, total_words):
        current = words[i]
        previous = tuple([words[j] for j in range(i-count, i)])
        if previous not in dictionary:
            dictionary[previous] = []
        dictionary[previous].append(current)
    return dictionary


def create_words(dictionary, count=3, word_limit=1000):
    words = list(random.choice(list(dictionary.keys())))
    while len(words) <= word_limit:
        previous = tuple(words[-count:])
        next_word = random.choice(dictionary[previous])
        words.append(next_word)
    return words


def get_string(created_words):
    lines = []
    line = ''
    for i in range(len(created_words)):
        if len(line) + len(created_words[i]) < 80:
            line += ' ' + created_words[i]
        else:
            lines.append(line)
            line = ''
            line += ' ' + created_words[i]
    lines.append(line)
    text = '\n'.join(lines)
    return text


def main(count=3, word_limit=1000, corpus=['Iliad.txt', 'Odyssey.txt'], preserve=False, sentences=True, silent=False, outfile=''):
    words = []
    for book in corpus:
        lines = load_lines(book)
        lines = simplify_lines(lines, preserve, sentences)
        words += get_words(lines, sentences)
    dictionary = build_dictionary(words, count)
    created_words = create_words(dictionary, count, word_limit)
    text_string = get_string(created_words)

    if not silent:
        print(text_string)
    if outfile:
        write_text(text_string, outfile)


if __name__ == '__main__':
    count = 3
    word_limit = 1000
    corpus = []
    preserve = False
    sentences = True
    silent = False
    outfile = ''

    if len(sys.argv) == 1:
        print_help_string()
        quit()

    i = 1
    unrecognized = []
    while i < len(sys.argv):
        if sys.argv[i] == '-h':
            print_help_string()
            quit()
        elif sys.argv[i] == '-c':
            if i+1 < len(sys.argv) and sys.argv[i+1][0] != '-':
                i += 1
                count = int(sys.argv[i])
            else:
                unrecognized.append('-c: Missing Specifier')
        elif sys.argv[i] == '-w':
            if i+1 < len(sys.argv) and sys.argv[i+1][0] != '-':
                i += 1
                word_limit = int(sys.argv[i])
            else:
                unrecognized.append('-w: Missing Specifier')
        elif sys.argv[i] == '-t':
            while i+1 < len(sys.argv) and sys.argv[i+1][0] != '-':
                i += 1
                corpus.append(sys.argv[i])
        elif sys.argv[i] == '-p':
            preserve = True
        elif sys.argv[i] == '-f':
            sentences = False
        elif sys.argv[i] == '-s':
            silent = True
        elif sys.argv[i] == '-o':
            if i+1 < len(sys.argv) and sys.argv[i+1][0] != '-':
                i += 1
                outfile = sys.argv[i]
            else:
                unrecognized.append('-o: Missing Specifier')
        else:
            unrecognized.append(sys.argv[i])
        i += 1

    if not corpus:
        corpus = ['Iliad.txt', 'Odyssey.txt']

    if len(unrecognized) > 0:
        print('\nERROR: Unrecognized Arguments:')
        for arg in unrecognized:
            print(arg)
        print_help_string()

    else:
        main(count, word_limit, corpus, preserve, sentences, silent, outfile)
