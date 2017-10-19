# -*- coding: utf8 -*-
from __future__ import unicode_literals
try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin
from .advanced_parser import AdvParser, GorgeousSoup
from .helper import post_remove_whitespaces, post_remove_oneline_link



class ExciteParser(AdvParser):
    PARSER_NAME = 'ExciteParser'

    def multi_page_article(self, soup, main_url):
        pages = [(soup, main_url)]
        if soup.select_one(selector='div#storyPager') is None:
            return pages  # single page article

        pager = soup.select_one(selector='div#storyPager')
        page_urls = sorted(list(set([a.attrs['href'] for a in pager.find_all('a')])))
        page_urls = [urljoin(main_url, u) for u in page_urls]
        for url in page_urls:
            soup = GorgeousSoup(self.extract_raw_data(url),
                                unwanted_selectors=soup.unwanted_selectors,
                                starting_selectors=soup.starting_selectors,
                                ending_criteria=soup.ending_criteria)
            pages.append((soup, url))
        return pages

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
    ]
    _starting_selectors = [
        'div.story',
    ]
    _ending_criteria = {
        'class': ['inner'],
        'id': ['storyPager']
    }

    special_case_functions = []
    image_case_functions = []
    video_case_functions = []
    header_case_functions = []
