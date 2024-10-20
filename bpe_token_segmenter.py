#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bpe_tokenizer.py

import sys
import pickle

def bpe_segment(tokens, vocab):
    word = ''.join(tokens)
    
    for pair in vocab:
    
        p_str = ''.join(pair)
        
        # pair가 단어에서 발견되면
        if p_str in word:
        
            i = 0
            while i < len(tokens)-1:
                if pair == (tokens[i], tokens[i+1]):
                    tokens.pop(i+1)
                    tokens[i] = p_str
                    
                i += 1
                
            if len(tokens) == 1:
                break

#########################################################

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f"{sys.argv[0]} file", file=sys.stderr)
        sys.exit()

    vocab = []
    
    with open('vocab.pickle', 'rb') as fin:
        vocab = pickle.load(fin)

    for file in sys.argv[1:]:
    
        print(f"processing {file} -> {file}.bpe", file=sys.stderr)
        
        with open(file, 'rt') as fin, open(file+".bpe", 'wt') as fout:
        
		        # 입력 파일 -> 단어 빈도 사전에 넣기
            for line in fin:
                words = line.split()
                
                for w in words:
		                # 문자 단위로 분해
                    tokens = list(w+"_")
                    
                    # 토큰화
                    bpe_segment(tokens, vocab)
                    
                    # special symbol '_' 제거
                    if tokens[-1] == '_':
                        tokens.pop()
                    else:
                        tokens[-1] = tokens[-1][:-1]
                    
                    # 출력
                    print(f"{w}\t{''.join(tokens)}", file=fout)
