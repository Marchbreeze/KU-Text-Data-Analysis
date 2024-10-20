#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
import MeCab  # 형태소 분석기

# MeCab 형태소 분석기 선언
mecab = MeCab.Tagger("-d /opt/homebrew/lib/mecab/dic/mecab-ko-dic")

# MeCab 품사와 SJ-RIKS 품사 매핑 테이블
mecab_to_sjriks_pos_map = {
    'NNG': 'NNG',  # 일반명사
    'NNP': 'NNP',  # 고유명사
    'NNB': 'NNB',  # 의존명사
    'NP': 'NP',    # 대명사
    'NR': 'NR',    # 수사
    'VV': 'VV',    # 동사
    'VA': 'VA',    # 형용사
    'VX': 'VX',    # 보조용언
    'VCP': 'VCP',  # 지정사
    'MM': 'MM',    # 관형사
    'MAG': 'MAG',  # 일반부사
    'MAJ': 'MAJ',  # 접속부사
    'IC': 'IC',    # 감탄사
    'JKS': 'JKS',  # 주격조사
    'JKG': 'JKG',  # 관형격조사
    'JKO': 'JKO',  # 목적격조사
    'JKB': 'JKB',  # 부사격조사
    'JKV': 'JKV',  # 호격조사
    'JKQ': 'JKQ',  # 인용격조사
    'JX': 'JX',    # 보조사
    'EP': 'EP',    # 선어말어미
    'EF': 'EF',    # 종결어미
    'EC': 'EC',    # 연결어미
    'ETN': 'ETN',  # 명사형전성어미
    'ETM': 'ETM',  # 관형형전성어미
    'XPN': 'XPN',  # 명사파생접두사
    'XSN': 'XSN',  # 명사파생접미사
    'XSV': 'XSV',  # 동사파생접미사
    'XSA': 'XSA',  # 형용사파생접미사
    'SF': 'SF',    # 마침표,물음표,느낌표
    'SP': 'SP',    # 쉼표,가운뎃점,콜론,빗금
    'SS': 'SS',    # 따옴표,괄호표
    'SE': 'SE',    # 줄임표
    'SO': 'SO',    # 불임표
    'SL': 'SL',    # 외국어
    'SH': 'SH',    # 한자
    'SW': 'SW',    # 기타기호
    'SN': 'SN',    # 숫자
    'SC': 'SP',    # 쉼표 다시 매핑
    'EC': 'EM',    # 연결 어미 -> 어말어미
    'EF': 'EM',    # 종결 어미 -> 어말어미
    'SSO': 'SS',
    'SSC': 'SS',
    'NA': 'VV'
}

if len(sys.argv) != 3:
    print(f"[Usage] {sys.argv[0]} sample_file trn_file", file=sys.stderr)
    sys.exit(1)

# 인자로 받은 파일 경로
sample_file_path = sys.argv[1]  # 예: sample01.txt
trn_file_path = sys.argv[2]  # 예: trn.txt

# trn.txt 파일로부터 어절 -> 형태소 분석 결과의 매핑 딕셔너리 생성
convert = defaultdict(str)
with open(trn_file_path, 'r', encoding='UTF-8') as trn_file:
    for line in trn_file.readlines():
        split_line = line.split()
        if len(split_line) == 2:
            word, analysis = split_line
            convert[word] = analysis  # 어절과 분석 결과 매핑

# MeCab의 분석 결과에서 형태소와 품사를 추출하고 SJ-RIKS 품사로 변환하는 함수
def parse_morphs_and_pos_with_sjriks(mecab_result):
    lines = mecab_result.strip().split("\n")
    morphs_with_pos = []
    for line in lines:
        if "\t" in line:
            morph, info = line.split("\t")  # 형태소와 정보 분리
            pos = info.split(",")[0]  # MeCab 품사 정보 추출
            # MeCab 품사를 SJ-RIKS 품사로 매핑 (없으면 NA로 설정)
            sjriks_pos = mecab_to_sjriks_pos_map.get(pos, 'NA')
            morphs_with_pos.append(f"{morph}/{sjriks_pos}")  # 형태소/품사 형식으로 저장
    return "+".join(morphs_with_pos)  # 형태소+품사 형식으로 연결

# sample.txt 파일 읽기 및 결과 파일 쓰기
with open(sample_file_path, 'r', encoding='UTF-8') as test_file, \
     open('result.txt', 'w', encoding='UTF-8') as result_file:

    write_list = []
    
    for line in test_file.readlines():
        line = line.strip()  # 앞뒤 공백 제거
        if line in convert:  # 어절이 trn.txt에 있는 경우
            result_file.writelines(line + '\t' + convert[line] + '\n')
        elif line == '':  # 빈 줄은 문장 경계이므로 그대로 유지
            result_file.writelines('\n')
        else:  # trn.txt에 없는 어절은 형태소 분석을 통해 처리
            mecab_result = mecab.parse(line)
            morph_analysis_with_pos = parse_morphs_and_pos_with_sjriks(mecab_result)  # 형태소/SJ-RIKS 품사 추출
            result_file.writelines(line + '\t' + morph_analysis_with_pos + '\n')

# 결과 파일 포맷 수정 (형태소 분석된 파일 형식으로 변환)
with open('result.txt', 'r', encoding='UTF-8') as file, \
     open('result_form.txt', 'w', encoding='UTF-8') as result:

    for line in file.readlines():
        split_line = line.split()
        if len(split_line) == 2:
            result.writelines(split_line[0] + '\t' + split_line[1] + '\n')  # 어절과 분석 결과
        else:
            result.writelines('\n')  # 빈 줄은 그대로 유지