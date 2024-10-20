#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bpe_learn.py

from collections import defaultdict
import sys
import pickle

def get_pair_frequency(corpus):
    pair_freqs = defaultdict(int)
    
    for wt, freq in corpus.items():
        for i in range(len(wt)-1):
            pair_freqs[(wt[i], wt[i+1])] += freq
            
    return pair_freqs

########################################

def replace_corpus(corpus, pair):
    p_str = ''.join(pair)
    to_delete = []
    to_add = defaultdict(int)
    
    for wt, freq in corpus.items():
        # pair가 부분문자열 중 발견되면
        if p_str in ''.join(wt):
            new_wt = []
            
            i = 0
            while i < len(wt)-1:
                if pair == (wt[i], wt[i+1]):
                    new_wt.append(wt[i]+wt[i+1])
                    i += 1
                else:
                    new_wt.append(wt[i])
                i += 1
                
            if i == len(wt)-1:  # 마지막 글자 추가
                new_wt.append(wt[i])
                
            to_add[tuple(new_wt)] = freq  # 추가 대상. 예) ('d', 'a', 't', 'e', 's_')
            to_delete.append(wt)  # 삭제 대상. 예) ('d', 'a', 't', 'e', 's_', '_')
    
    for key in to_delete:
        corpus.pop(key)  # 삭제
    
    if len(to_add) > 0:
        corpus.update(to_add)  # 사전 업데이트

########################################

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]} file(s)", file=sys.stderr)
        sys.exit()

    corpus = defaultdict(int)
    vocab = []

		# 입력 파일에 대해서 하나씩 실행
    for file in sys.argv[1:]:
    
        print(f"processing {file}", file=sys.stderr)

        with open(file) as fin:
        
			      # 입력 파일 -> 코퍼스 (token 튜플/빈도 사전에 넣기)
            for line in fin:
                for w in line.split():  # w = 'April'
                    corpus[tuple(w + '_')] += 1  # corpus[('A', 'p', 'r', 'i', 'l', '_')] += 1

    print("corpus size = %d types" % len(corpus), file=sys.stderr)

    k = 1
    while k <= 10000:  # 반복 횟수 설정 (10000회)
    
        # 토큰 쌍 빈도 계산
        pair_freqs = get_pair_frequency(corpus)
        
        # 가장 높은 빈도를 가진 토큰 쌍 찾기
        most_freq_pair = max(pair_freqs, key=pair_freqs.get)
        max_freq = pair_freqs[most_freq_pair]
        
        # pair 중 가장 높은 빈도가 임계값 이하이면 학습 종료
        if max_freq <= 1:
            break
        
        print(f"iteration: %d (max = %d, %s)" % (k, max_freq, ''.join(most_freq_pair)), file=sys.stderr)
        
        # 어휘 사전에 추가
        vocab.append(most_freq_pair)
        
        # 새로운 토큰 쌍을 코퍼스에 반영
        replace_corpus(corpus, most_freq_pair)
        
        k += 1

    ## 학습 완료
    for w, f in corpus.items():
        print(w, f)

    # 어휘 사전 출력
    print(vocab)

    # 어휘 사전 pickle 저장
    with open('vocab.pickle', 'wb') as fout:
        pickle.dump(vocab, fout)
