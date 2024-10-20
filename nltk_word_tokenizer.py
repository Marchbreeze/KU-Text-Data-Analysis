#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from nltk.tokenize import word_tokenize, sent_tokenize

if __name__ == "__main__":
    
    # 명령줄 인수로 전달된 파일을 처리
    for file in sys.argv[1:]:
		    # 처리할 파일에 대한 로그 메시지
        print("processing %s -> %s" %(file, file+".tok"), file=sys.stderr)

        with open(file, "rt") as fin:
            # 파일 내용 읽기
            text = fin.read()
            # 줄 바꿈을 공백으로 대체하여 문장 전체를 하나의 긴 문자열로 설정
            text = text.replace("\n", " ")

        with open(file+".tok", "wt") as fout:
            # 문장 분리 / 분리된 각 문장에 대해
            for sent in sent_tokenize(text):
                
                # 단어 분리
                for token in word_tokenize(sent):
                    print(token, file=fout)
                
                # 빈 라인 출력 (문장 경계 구분용)
                print("", file=fout)
