#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle

###############################################################################

def learn_lm(filename):
    bigrams = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            
            # 문장을 읽어서 공백 기준으로 어절 분리 & 시작과 끝에 기호 추가
            words = ['<s>'] + line.strip().split() + ['</s>'] 
            
            # 2-gram 생성
            for i in range(len(words) - 1):
                w1, w2 = words[i], words[i + 1]
                
                # 2-gram의 카운트 증가 (기존에 없으면 1로 설정)
                if (w1, w2) in bigrams:
                    bigrams[(w1, w2)] += 1
                else:
                    bigrams[(w1, w2)] = 1
                
    return bigrams

###############################################################################

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print( "[Usage] %s in-file out-file(pickle)" %sys.argv[0], file=sys.stderr)
        sys.exit()

    filename = sys.argv[1]
    print("processing %s ..." %filename, file=sys.stderr)
    
    bigrams = learn_lm(filename)

    with open(sys.argv[2],"wb") as fout:
        print("saving %s" %sys.argv[2], file=sys.stderr)
        pickle.dump(bigrams, fout)
