#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import hanja2hangeul_table

h2h_table = hanja2hangeul_table.hanja2hangeul_table

def help(arg):
    print("\n%s Option file(s)"%arg, file=sys.stderr)
    print("\n[Option]", file=sys.stderr)
    print("\t-h1: hangeul", file=sys.stderr)
    print("\t-h2: hangeul(hanja)", file=sys.stderr)
    print("\t-h3: hanja(hangeul)\n", file=sys.stderr)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 1)
# ex) 聖經에 -> 성경에
def hanja2hangeul_str1(str):
    result = []
    
    for ch in str:
        if ch in h2h_table: 
            result.append(h2h_table[ch][0])
        else:
            result.append(ch)
        
    return ''.join(result)
    
###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 2)
# ex) 聖經에 -> 성경(聖經)에
def hanja2hangeul_str2(str):
    word_count = 0
    word = []
    result = []
    
    for ch in str:
        if ch in h2h_table: 
            result.append(h2h_table[ch][0])
            word_count += 1
            word.append(ch)
            
        else:
            if(word_count > 0):
                result.append('(')
                for i in word:
                    result.append(i)
                result.append(')')
                
                word_count = 0
                word = []
                
            result.append(ch)
        
    return ''.join(result)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 3)
# ex) 聖經에 -> 聖經(성경)에
def hanja2hangeul_str3(str):
    word_count = 0
    word = []
    result = []
    
    for ch in str:
        if ch in h2h_table: 
            result.append(ch)
            word_count += 1
            word.append(ch)
            
        else:
            if(word_count > 0):
                result.append('(')
                for i in word:
                    result.append(h2h_table[i][0])
                result.append(')')
                
                word_count = 0
                word = []
                
            result.append(ch)
        
    return ''.join(result)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 3:
        help(sys.argv[0])
        sys.exit()
        
    if sys.argv[1] == '-h1':
        func = hanja2hangeul_str1

    elif sys.argv[1] == '-h2':
        func = hanja2hangeul_str2

    elif sys.argv[1] == '-h3':
        func = hanja2hangeul_str3

    else:
        help(sys.argv[0])
        sys.exit()
        
    for filename in sys.argv[2:]:

        with open(filename, "r", encoding="utf-8") as infp, open(filename+".out", "w", encoding="utf-8") as outfp:

            print("%s -> %s"%(filename, filename+".out"), file=sys.stderr)

            for line in infp:
                
                result = func(line.rstrip())
                
                print(result, file=outfp)
