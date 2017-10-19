try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin
from .advanced_parser import AdvParser, GorgeousSoup
from .helper import (parse_keywords_meta, post_remove_whitespaces, post_remove_oneline_link,
    parse_cover_info_basic)



class OriconParser(AdvParser):
    PARSER_NAME = 'OriconParser'

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
    ]
    _starting_selectors = [
        'div.mod-p',
    ]
    _ending_criteria = {
        'class': ['block-photo-preview'],
        'id': ['div-gpt-ad-ON-PC-InreadContent1-1']
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
    ]
    _parse_cover_info = parse_cover_info_basic
    _parse_keywords = parse_keywords_meta
