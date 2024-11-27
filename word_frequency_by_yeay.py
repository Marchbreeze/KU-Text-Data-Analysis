#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

###############################################################################
def word_count(file_name, file_index, word_freq):

    with open(file_name, mode="r", encoding="utf-8") as fin:
        for word in fin.read().split():
            if word not in word_freq:
                word_freq[word] = [0] * 20
            word_freq[word][file_index] += 1

    return word_freq

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    word_freq = defaultdict(list)

    for index, input_file in enumerate(sys.argv[1:]):
        print(f"processing {input_file}", file=sys.stderr)
        word_freq = word_count(input_file, index, word_freq)

    for word, freq_list in sorted(word_freq.items()):
        print(word+'\t'+str(freq_list))
