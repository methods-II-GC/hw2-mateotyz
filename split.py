#!/usr/bin/env python3
"""The program takes input corpus data and (pseudo)randomly splits it into an 80% training set, 10% development set, and 10% test set."""


import argparse
import random

def main(args: argparse.Namespace) -> None:
    
    from typing import Iterator, List

    def read_tags(path) -> Iterator[List[List[str]]]:
        with open(path, "r") as source:
            lines = []
            for line in source:
                line = line.rstrip()
                if line:  # Line is contentful.
                    lines.append(line.split())
                else:  # Line is blank.
                    yield lines.copy()
                    lines.clear()
        # Just in case someone forgets to put a blank line at the end...
        if lines:
            yield lines
    
    def write_tags (source, path, n_start, n_finish):
        with open (path, "w") as sink:
            #from the starting line in the data to the finishing line
            for n in range(n_start, n_finish):
                #reverting the format from list to string, as the original
                for i in source[n]:
                    listToStr = ' '.join([str(s) for s in i])
                    print (listToStr, file=sink)
    
    corpus = list(read_tags(args.input))
    n_80 = int(len(corpus)*0.8) #the 80th per cent of the input
    n_90 = int(len(corpus)*0.9) #the 90th per cent of the input
    random.Random(args.seed).shuffle(corpus)
    
    #write the first 80% to train set
    write_tags(corpus, args.train, 0, n_80)
    
    #write the 80%-90% of data to dev set
    write_tags(corpus, args.dev, n_80, n_90)
    
    #write the rest 10% of data to dev set
    write_tags(corpus, args.test, n_90, len(corpus))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, required=True, help='Seed value')
    parser.add_argument('input', help='Path of input data')
    parser.add_argument('train', help='Path of training set')
    parser.add_argument('dev', help='Path of dev set')
    parser.add_argument('test', help='Path of test set')
    main(parser.parse_args())
