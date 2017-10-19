try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin
from .advanced_parser import AdvParser
from .helper import post_remove_whitespaces, post_remove_oneline_link


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
