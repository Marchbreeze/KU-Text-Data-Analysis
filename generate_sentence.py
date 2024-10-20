#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import random # choice

def generate_sentence(bigrams, start_with = '<s>'):
    sentence = []
    
    # 시작 어절을 설정
    current_word = start_with
    
    # 시작 어절을 문장에 추가
    if current_word != '<s>':
        sentence.append(current_word)

    # 끝 어절이 나올때까지 while문으로 반복
    while current_word != '</s>':
        
        # 현재 어절에 해당하는 다음 어절 후보를 찾음
        candidates = [w2 for (w1, w2) in bigrams if w1 == current_word]
        
        # 후보가 없으면 종료
        if not candidates:
            break

        # 다음 어절 후보 중에서 확률에 기반해 선택
        next_word = random.choice(candidates)
        
        # 끝 어절이 아닌 경우에만 문장에 추가
        if next_word != '</s>':
            sentence.append(next_word)
        
        # 다음 어절을 현재 어절로 업데이트
        current_word = next_word 

    return ' '.join(sentence)
    
###############################################################################

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage] %s in-file(pickle)" %sys.argv[0], file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fp:
        bigrams = pickle.load(fp)

    while True:
        
        key = input("문장 생성: Enter, 종료: Q:")
        
        if key == 'q' or key == 'Q':
            break
            
        for i in range(10): # 생성할 문장 수
            
            # generate a random sentence 
            sentence = generate_sentence(bigrams, '<s>')
            
            print(i+1, ':', sentence, '\n')
