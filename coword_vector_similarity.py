#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):

    numerator = 0
    denominator_t = 0
    denominator_c = 0

    for coword, t_score in t_vector.items():
        denominator_t += t_score ** 2
        if coword in c_vector:
            numerator += t_score * c_vector[coword]

    for coword, t_score in c_vector.items():
        denominator_c += t_score ** 2

    denominator_t = math.sqrt(denominator_t)
    denominator_c = math.sqrt(denominator_c)

    if denominator_t == 0 or denominator_c == 0:
        return 0

    return numerator / (denominator_t * denominator_c)

###############################################################################
def most_similar_words(word_vectors, target, topN=10):
    
    result = {}

    if target not in word_vectors:
        return []

    target_vector = word_vectors[target]

    candidates = set(target_vector.keys())
    for coword in target_vector.keys():
        if coword in word_vectors:
            candidates.update(word_vectors[coword].keys())

    for candidate in candidates:
        if candidate in target:
            continue
        
        if candidate in word_vectors:
            cos_sim = cosine_similarity(target_vector, word_vectors[candidate])
            if cos_sim > 0.001: 
                result[candidate] = cos_sim

    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)

    while True:

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    
        try:
            query = input()
            
        except EOFError:
            print('프로그램을 종료합니다.', file=sys.stderr)
            break
    
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN=30)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')
