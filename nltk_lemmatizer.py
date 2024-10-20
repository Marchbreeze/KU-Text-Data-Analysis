#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize

if __name__ == "__main__":
    #nltk.download('averaged_perceptron_tagger')
    #nltk.download('wordnet')

    wnl = WordNetLemmatizer()

    # 각 파일에 대해
    for file in sys.argv[1:]:
        print(f"processing %s -> %s" %(file, file+".lemma"), file=sys.stderr)

        with open(file, "rt") as fin:
            # 파일 내용 읽기
            text = fin.read()
            text = text.replace("\n", " ")

        with open(file+".lemma", "wt") as fout:

            # 문장 분리 / 분리된 각 문장에 대해
            for sent in sent_tokenize(text):

                # 단어 분리
                tokens = word_tokenize(sent)

                # POS tagging
                pos_tags = pos_tag(tokens)

                # lemmatizing
                for word, pos in pos_tags:
                    if pos.startswith('N'):
                        # 명사일 경우 'n'을 사용
                        lemma = wnl.lemmatize(word, 'n')
                    elif pos.startswith('V'):
                        # 동사일 경우 'v'를 사용
                        lemma = wnl.lemmatize(word, 'v')
                    elif pos.startswith('R'):
                        # 부사일 경우 'r'을 사용
                        lemma = wnl.lemmatize(word, 'r')
                    elif pos.startswith('J'):
                        # 형용사일 경우 'a'를 사용
                        lemma = wnl.lemmatize(word, 'a')
                    else:
                        # 그 외의 경우는 명사로 처리
                        lemma = wnl.lemmatize(word, 'n')

                    print(word, lemma, pos, sep='\t', file=fout)
