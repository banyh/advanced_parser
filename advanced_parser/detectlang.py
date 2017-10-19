# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from langdetect import detect
from zhconvert._conv2tw_data import trad, simp

simp_to_trad = dict((ord(s), ord(t)) for s, t in zip(simp, trad))
trad_to_simp = dict((ord(t), ord(s)) for t, s in zip(trad, simp))

ja_only_words = '乗亜仏値仮働価倹児両剰剤剣効勅労勲勧匁巻呉咲啓単厳圏囲円図団増圧塁壊壱奨姉姫娯嬢実' \
                '寛専対峠巣帯廃広庁弾従徴徳恵悪悩応懐戦戯戸払抜拝掲揺捜択撃拠挙拡摂収晩暦暁査栄楽様' \
                '検桜権歓歩歳歴帰毎気氷汚渉涙浄渇満渋沢済滝瀬焼営犠猟獣産畑畳疎発碁砕稲穂穏窓粧粋絶' \
                '経緑縁県縦総絵継続繊聴粛脳臓舎舗荘菓薫蔵薬処衆裏覚覧観説謡訳読変譲弐売頼賛軽転込逓' \
                '遅辺郷酔醸釈鋭録銭錬鉄鋳鉱閲関陥隣険隠隷雑霊顔顕騒駆験駅髄髪闘鶏塩黒黙斎歯齢'


def detect_supported_language(text):
    text = text.lower()
    english = ''.join([ch for ch in text if ord(ch) < 0x7F])
    latin = ''.join([ch for ch in text if ord(ch) < 0x200 and ord(ch) > 0x7F])
    nonlatin = ''.join([ch for ch in text if ord(ch) > 0x200])
    len_all = float(len(text))
    len_english = float(len(english))
    len_latin = float(len(latin))
    len_nonlatin = float(len(nonlatin))

    if (len_english + len_latin) / len_all > 0.95:
        return detect(text)

    if sum([ord(ch) >= 0x3040 and ord(ch) <= 0x30FF for ch in nonlatin]) / len_nonlatin > 0.1 or \
       sum([ch in ja_only_words for ch in nonlatin]) / len_nonlatin > 0.02:
        return 'ja'  # Japenese
    if sum([ord(ch) >= 0xAC00 and ord(ch) <= 0xD7AF for ch in nonlatin]) / len_nonlatin > 0.3:
        return 'ko'  # Korean
    if sum([ord(ch) >= 0x400 and ord(ch) <= 0x4FF for ch in nonlatin]) / len_nonlatin > 0.3:
        return 'ru'  # Russian

    tw_prop = sum([ch == cht for ch, cht in zip(nonlatin, nonlatin.translate(simp_to_trad))]) / len_nonlatin
    cn_prop = sum([ch == chs for ch, chs in zip(nonlatin, nonlatin.translate(trad_to_simp))]) / len_nonlatin
    if tw_prop > cn_prop:
        return 'zh-tw'
    else:
        return 'zh-cn'
