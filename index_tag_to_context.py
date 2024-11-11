#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf

###############################################################################
# 명사, 복합명사 추출
def get_index_terms(mt_list):
    
    nouns = []
    current_phrase = []
    
    # 기존 명사 태그 집합
    valid_tags = {'NNG', 'NNP', 'NR', 'NNB', 'SL', 'SH', 'SN'}
    # 결과로 처리할 태그 집합
    single_noun_tags = {'NNG', 'NNP', 'SH', 'SL'}

    # 현재 구성이 단일 명사인지 복합 명사인지에 따라 단어를 추가하는 함수
    def add_to_nouns(phrase):
        
        # 복합 명사일 경우
        if len(phrase) > 1:
            # 복합 명사 전체를 하나의 단어로 결합
            compound = ''.join(word for word, tag in phrase)
            # 복합 명사에 포함된 단일 명사 태그만 별도로 추가
            for word, tag in phrase:
                if tag in single_noun_tags and tag != 'SL':
                    nouns.append(word)
            # 결합된 복합 명사 전체 추가
            nouns.append(compound)
            
        # 단일 명사일 경우
        elif phrase:
            word, tag = phrase[0]
            if tag in single_noun_tags:
                nouns.append(word)

    # 형태소 분석 결과 리스트에서 각 형태소와 태그를 처리
    for morph, tag in mt_list:
        # 유효한 명사 태그인 경우 현재 구성을 이어서 만듦
        if tag in valid_tags:
            current_phrase.append((morph, tag))
        else:
            # 유효하지 않은 태그가 등장하면 현재 구성 단어를 처리하고 초기화
            add_to_nouns(current_phrase)
            current_phrase = []

    # 루프 종료 후 남은 현재 구성 처리
    add_to_nouns(current_phrase)
    
    return nouns

###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):

    with open( input_file, "r", encoding='utf-8') as fin, open( output_file, "w", encoding='utf-8') as fout:

        for line in fin:

            # 빈 라인 (문장 경계)
            if line[0] == '\n':
                print(file=fout)
                continue

            try:
                ej, tagged = line.split(sep='\t')
            except:
                print(line, file=sys.stderr)
                continue

            # 형태소, 품사 추출
            # result : list of tuples
            result = mf.get_morphs_tags(tagged.rstrip())

            # 색인어 추출
            terms = get_index_terms(result)

            # 색인어 출력
            for term in terms:
                print(term, end=" ", file=fout)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)

        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)
