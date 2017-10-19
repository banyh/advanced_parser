# -*- coding: utf8 -*-
from __future__ import unicode_literals
from .advanced_parser import AdvParser
from .helper import post_remove_oneline_link, post_remove_whitespaces


class SinaParser(AdvParser):
    PARSER_NAME = 'SinaParser'

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
        'div.nw-main-photo-text',
        'div.nw-main-photo-text-mobile',
        'div.nw-main-photo-text-extended',
        'div.nw-ctrl-text-size',
    ]
    _starting_selectors = [
        'div.nw-body',
    ]
    _ending_criteria = {
        'class': ['pre'],
        'id': []
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
    ]
