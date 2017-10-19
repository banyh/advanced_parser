# -*- coding: utf8 -*-
from __future__ import unicode_literals
import re
from .advanced_parser import AdvParser
from .helper import post_remove_oneline_link, post_remove_whitespaces


def post_remove_noise(parser, content, soup):
    return re.sub('新华社.*?[电）]', '', content)


class XinhuaParser(AdvParser):
    PARSER_NAME = 'XinhuaParser'

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
        'font[color]',
    ]
    _starting_selectors = [
        'div.content',
    ]
    _ending_criteria = {
        'class': [],
        'id': ['div_page_roll1']
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
        post_remove_noise,
    ]
