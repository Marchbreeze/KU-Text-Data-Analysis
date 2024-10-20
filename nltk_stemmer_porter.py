#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

if __name__ == "__main__":
    
    stemmer = PorterStemmer()  # PorterStemmer 객체 생성

    # 각 파일에 대해
    for file in sys.argv[1:]:
        print("processing %s -> %s" %(file, file+".stem"), file=sys.stderr)

        with open(file, "rt") as fin:
            # 파일 내용 읽기
            text = fin.read()
            text = text.replace("\n", " ")

        with open(file+".stem", "wt") as fout:
            # 문장 분리 / 분리된 각 문장에 대해
            for sent in sent_tokenize(text):
                
                # 단어 분리
                for token in word_tokenize(sent):
                    # stemming: 단어를 스템으로 변환
                    stem = stemmer.stem(token)
                    
                    # 단어와 스템 결과를 탭으로 구분하여 파일에 출력
                    print(token, stem, sep='\t', file=fout)
                
                # 빈 라인 출력 (문장 경계 구분용)
                print("", file=fout)
