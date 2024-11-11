#!/usr/bin/env python3
# coding: utf-8

import sys

###############################################################################
def get_morphs_tags(tagged):

    result = []
    
    # + 기준으로 분리
    splited_tag = tagged.split('+')
    
    for part in splited_tag:
        if part != "":
            # 어절 내 '+'나 '/' 문자가 있는 경우에 대한 처리
            if part[0] == "/" and part[1] != "/":
                part = "+" + part
        
        # '/' 기준으로 분리 후 저장
        splited_part = part.rsplit("/", 1)
        if len(splited_part) == 2:
            morph, tag = splited_part
            result.append((morph, tag))

    return result

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], encoding='utf-8') as fin:

        for line in fin:

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2:
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())

            for morph, tag in result:
                print(morph, tag, sep='\t')
