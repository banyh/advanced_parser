# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re
from .advanced_parser import AdvParser
from .helper import post_remove_oneline_link, post_remove_whitespaces


def post_clear_noise(parser, content, soup):
    content = re.sub('正文已结束.*', '', content)
    content = re.sub('腾讯体育[^ ]*', '', content)
    return content


class QQSportParser(AdvParser):
    PARSER_NAME = 'QQSportParser'

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
        'div.a_Info',
        'div.a_share',
        'span.a_commentNum',
        'span.a_ilike',
        'div.rv-root-v2',
        'p[align=center]',
    ]
    _starting_selectors = [
        'div.Cnt-Main-Article-QQ',
    ]
    _ending_criteria = {
        'class': ['qq_articleFt', 'qq_editor'],
        'id': []
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
        post_clear_noise,
    ]
