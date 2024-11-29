#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle

###############################################################################
def vector_indexing(filename):

    word_vectors = {}

    with open(filename, 'r') as fin:
        for line in fin:
            parts = line.strip().split()
            target_word, context_word, value = parts[0], parts[1], float(parts[2])
            
            if target_word not in word_vectors:
                word_vectors[target_word] = {}
            
            word_vectors[target_word][context_word] = value

    return word_vectors
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"[Usage] {sys.argv[0]} in-file out-file(pickle)", file=sys.stderr)
        sys.exit()

    filename = sys.argv[1]
    print(f"processing {filename} ...", file=sys.stderr)
    
    # 공기어 벡터 저장 (dictionary of dictionary)
    word_vectors = vector_indexing(filename)

    print(f"# of entries = {len(word_vectors)}", file=sys.stderr)

    with open(sys.argv[2],"wb") as fout:
        print(f"saving {sys.argv[2]}", file=sys.stderr)
        pickle.dump(word_vectors, fout)
