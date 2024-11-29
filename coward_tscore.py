#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):

    freqs = {}

    with open(filename, 'r') as fin:
        for line in fin:
            if line.startswith("#Total"):
                parts = line.strip().split("\t")
                freqs['#Total'] = int(parts[1])
            else:
                parts = line.strip().split("\t")
                freqs[parts[0]] = int(parts[1])

    return freqs

###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    
    t_scores = {}
    
    with open(filename, 'r') as fin:
        for line in fin:
            parts = line.strip().split("\t")
            word1, word2, observed_freq = parts[0], parts[1], int(parts[2])
            
            if word2 in word1:
                continue

            if observed_freq < cutoff:
                continue

            expected_freq_1 = (unigram_context[word1] * unigrams[word2]) / uni_N
            t_score_1 = (observed_freq - expected_freq_1) / math.sqrt(observed_freq)

            if t_score_1 > 0:
                t_scores[(word1, word2)] = t_score_1

            expected_freq_2 = (unigram_context[word2] * unigrams[word1]) / uni_N
            t_score_2 = (observed_freq - expected_freq_2) / math.sqrt(observed_freq)

            if t_score_2 > 0:
                t_scores[(word2, word1)] = t_score_2

    t_scores = dict(sorted(t_scores.items(), key=lambda x: x[0]))

    return t_scores

###############################################################################
def print_tscore(filename, t_scores):

    with open(filename, 'w') as fout:
        for (word1, word2), t_score in sorted(t_scores.items()):
            fout.write(f"{word1}\t{word2}\t{t_score:.3f}\n")

###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print(f"processing {input_file}", file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print(f"\tLoading {file_stem}.1gram", file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print(f"\tLoading {file_stem}.1gram_context", file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        # key : (target, coword)
        # value : t-score
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscore", t_scores)
