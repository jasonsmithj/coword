# -*- coding: utf-8 -*-

import MeCab
import unicodedata
import re

from app import app


class MorphologicalAnalysis():
    def _unicode_normalize(self, cls, s):
        pt = re.compile('([{}]+)'.format(cls))

        def norm(c):
            return unicodedata.normalize('NFKC', c) if pt.match(c) else c

        s = ''.join(norm(x) for x in re.split(pt, s))
        s = re.sub('－', '-', s)
        return s

    def _remove_extra_spaces(self, s):
        s = re.sub('[ 　]+', ' ', s)
        blocks = ''.join(('\u4E00-\u9FFF',  # CJK UNIFIED IDEOGRAPHS
                          '\u3040-\u309F',  # HIRAGANA
                          '\u30A0-\u30FF',  # KATAKANA
                          '\u3000-\u303F',  # CJK SYMBOLS AND PUNCTUATION
                          '\uFF00-\uFFEF'   # HALFWIDTH AND FULLWIDTH FORMS
                          ))
        basic_latin = '\u0000-\u007F'

        def remove_space_between(cls1, cls2, s):
            p = re.compile('([{}]) ([{}])'.format(cls1, cls2))
            while p.search(s):
                s = p.sub(r'\1\2', s)
            return s

        s = remove_space_between(blocks, blocks, s)
        s = remove_space_between(blocks, basic_latin, s)
        s = remove_space_between(basic_latin, blocks, s)
        return s

    def _remove_numeric(self, s):
        s = re.sub('[0-9]', '', s)
        return s

    def _normalize_neologd(self, s):
        s = s.strip()
        s = self._unicode_normalize('０-９Ａ-Ｚａ-ｚ｡-ﾟ', s)

        def maketrans(f, t):
            return {ord(x): ord(y) for x, y in zip(f, t)}

        s = re.sub('[˗֊‐‑‒–⁃⁻₋−]+', '-', s)  # normalize hyphens
        s = re.sub('[﹣－ｰ—―─━ー]+', 'ー', s)  # normalize choonpus
        s = re.sub('[~∼∾〜〰～]', '', s)  # remove tildes
        s = s.translate(
            maketrans(
                '!"#$%&\'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣',
                '！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」'
            )
        )

        s = self._remove_extra_spaces(s)
        # keep ＝,・,「,」
        s = self._unicode_normalize('！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜', s)
        s = re.sub('[’]', '\'', s)
        s = re.sub('[”]', '"', s)
        s = self._remove_numeric(s)
        return s

    def parse(self, doc):

        if not doc:
            return ''

        tagger = MeCab.Tagger('-Ochasen -d %s' % app.config['NEOLOGD_PATH'])

        words = tagger.parse(self._normalize_neologd(doc)).split('\n')

        val = []
        for word in words:
            if word == 'EOS' or word == '':
                continue

            word_info = word.split('\t')

            if word_info[3][0:2] in ['名詞']:
                val.append(word_info[2])
        return val

