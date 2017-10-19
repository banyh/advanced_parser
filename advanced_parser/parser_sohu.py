# -*- coding: utf8 -*-
from __future__ import unicode_literals
from .advanced_parser import AdvParser
from .helper import post_remove_oneline_link, post_remove_whitespaces


class SohuParser(AdvParser):
    PARSER_NAME = 'SohuParser'

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
        'span.CTexts',
    ]
    _starting_selectors = [
        'div#contentText',
    ]
    _ending_criteria = {
        'class': ['original-title'],
        'id': ['url']
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
    ]
