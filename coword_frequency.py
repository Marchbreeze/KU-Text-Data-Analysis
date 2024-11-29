#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations 

###############################################################################
def print_word_freq(filename, word_freq):

    with open(filename, 'w') as fout:
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[0])
        
        if 'total_unigram_count' in word_freq:
            fout.write(f"#Total\t{word_freq['total_unigram_count']}\n")
            del word_freq['total_unigram_count']
        
        for word, freq in sorted_word_freq:
            fout.write(f"{word}\t{freq}\n")

###############################################################################
def print_coword_freq(filename, coword_freq):

    with open(filename, 'w') as fout:
        sorted_coword_freq = sorted(coword_freq.items(), key=lambda x: (x[0][0], x[0][1]))
        
        for (word1, word2), freq in sorted_coword_freq:
            fout.write(f"{word1}\t{word2}\t{freq}\n")

###############################################################################
def get_coword_freq(filename):
    
    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)
    word_freq = defaultdict(int)
    total_unigram_count = 0
    
    with open(filename, 'r') as fin:
        for line in fin:
            words = set(line.split())
            total_unigram_count += len(words)
            
            for word in words:
                word_freq[word] += 1
                word_context_size[word] += len(words)
            
            for w1, w2 in combinations(sorted(words), 2):
                coword_freq[(w1, w2)] += 1
    
    word_freq['total_unigram_count'] = total_unigram_count
    return word_freq, coword_freq, word_context_size

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print(f"processing {input_file}", file=sys.stderr)
        
        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "2017"
        
        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1gram", word_freq)
        
        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_context", word_context_size)
