# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from bs4 import BeautifulSoup, NavigableString
import re
import logging
try:
    unicode = unicode
except:
    unicode = str
from .helper import (
    parse_cover_info_basic,
    parse_keywords_empty,
    post_remove_whitespaces,
    post_remove_oneline_link,
    parse_img_tag,
    parse_youtube_iframe_tag,
    parse_h1_to_h4_tag,
    ParseError,
    ParsedContent,
    Result,
)
from .detectlang import detect_supported_language
from .basic_parser import BasicParser


__all__ = ['AdvParser', 'GorgeousSoup']


class GorgeousIterable(object):
    '''GorgeousIterable 與 GorgeousSoup 共用同一個 sequence (_all_items)。
    當呼叫 GorgeousIterable.next() 或是 GorgeousSoup.consume() 時，都會使 _all_items 數量減少。
    '''
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return self

    def __next__(self):  # Python 3 compatible
        if self.items:
            return self.items.pop(0)
        raise StopIteration

    def next(self):  # Python 2 compatible
        if self.items:
            return self.items.pop(0)
        raise StopIteration


class GorgeousSoup(BeautifulSoup):
    '''GorgeousSoup 的功能與 BeautifulSoup 大致相同，但多了下列功能：
    * raw_content 會作前處理，將HTML註解拿掉，並增加換行
    * unwanted_selectors 用來刪除不需要的HTML elements
    * starting_selectors 用來決定文章從那個 element 開始
    * ending_criteria 用來決定文章到那個 element 結束
    * all_items 會將 starting 到 ending 之間的 elements 包裝成 iterable
    * consume 可以刪除某個 element 及其 sub-elements
    '''
    def __init__(self, raw_content, unwanted_selectors=[], starting_selectors=[], ending_criteria=[]):
        raw_content = re.sub('<!--.*?-->', '', raw_content, flags=re.MULTILINE | re.DOTALL)
        raw_content = re.sub('<(br|p)', '\n<\\1', raw_content, flags=re.IGNORECASE)
        raw_content = re.sub('</p>', '</p>\n', raw_content, flags=re.IGNORECASE)
        super(GorgeousSoup, self).__init__(markup=raw_content, features='lxml')

        self.unwanted_selectors = unwanted_selectors
        self.starting_selectors = starting_selectors
        self.ending_criteria = ending_criteria
        self._remove_unwanted()
        self.all_items

    def _remove_unwanted(self):
        for selector in self.unwanted_selectors:
            for item in self.select(selector):
                item.extract()

    def _find_starting_element(self):
        for selector in self.starting_selectors:
            if self.select_one(selector) is not None:
                return self.select_one(selector)
        raise ValueError

    def _is_ending_element(self, item):
        if isinstance(item, NavigableString):
            return False
        ending_class = self.ending_criteria.get('class')
        ending_id = self.ending_criteria.get('id')
        for item_class in item.attrs.get('class', []):
            if item_class in ending_class:
                return True
        if item.attrs.get('id', '') in ending_id:
            return True
        return False

    def consume(self, consumed_item):
        while self._all_items:
            if all([parent is not consumed_item for parent in self._all_items[0].parents]):
                break
            self._all_items.pop(0)

    @property
    def all_items(self):
        if self._all_items:
            return GorgeousIterable(self._all_items)

        starting = self._find_starting_element()
        self._all_items = []
        for item in starting.next_elements:
            if self._is_ending_element(item):
                break
            self._all_items.append(item)
        return GorgeousIterable(self._all_items)


class AdvParser(BasicParser):
    #
    # ------------ Override following attributes --------------
    #
    PARSER_NAME = 'AdvParser'

    def multi_page_article(self, soup, main_url):
        pages = [(soup, main_url)]  # single page article
        # page_urls = [...]  # multi-page article
        # for url in page_urls:
        #     raw_content = self.extract_raw_data(url)
        #     soup = GorgeousSoup(raw_content,    # you must use GorgeousSoup to parse the content
        #                         unwanted_selectors=soup.unwanted_selectors,
        #                         starting_selectors=soup.starting_selectors,
        #                         ending_criteria=soup.ending_criteria)
        #     pages.append((soup, url))
        return pages

    _unwanted_selectors = [
        'script',  # <script>...</script>
        'style',  # <style>...</style>
        'div.story_bar',  # a <div> element with class="story_bar"
        'div#story_bar',  # a <div> element with id="story_bar"
    ]
    _starting_selectors = [
        'div.article',  # a <div> element with class="article"
        'div#article',  # a <div> element with id="article"
    ]
    _ending_criteria = {
        'class': ['subscribe', 'article_tags'],
        'id': ['article_bottom_ad', 'story_also']
    }

    special_case_functions = []  # func(parser, item)
    image_case_functions = [  # func(parser, item)
        parse_img_tag,
        # parse_fbimage_div_tag,  # not implmented yet
        # parse_instgram_blockquote_tag,  # not implmented yet
    ]
    video_case_functions = [  # func(parser, item)
        parse_youtube_iframe_tag,
        # parse_fbvideo_div_tag,  # not implmented yet
        # parse_vimeo_iframe_tag,  # not implmented yet
        # parse_dailymotion_iframe_tag,  # not implmented yet
    ]
    header_case_functions = [  # func(parser, item)
        parse_h1_to_h4_tag,
    ]
    post_process_functions = [  # func(parser, content, soup)
        post_remove_whitespaces,
        post_remove_oneline_link,
    ]
    _parse_cover_info = parse_cover_info_basic
    _parse_keywords = parse_keywords_meta

    #
    # ------------ Don't Override following attributes --------------
    #
    def special_case(self, item):
        return any([func(self, item) for func in self.special_case_functions])

    def image_case(self, item):
        return any([func(self, item) for func in self.image_case_functions])

    def video_case(self, item):
        return any([func(self, item) for func in self.video_case_functions])

    def header_case(self, item):
        return any([func(self, item) for func in self.header_case_functions])

    def post_process(self, content, soup):
        content = ''.join(content)
        for func in self.post_process_functions:
            content = func(self, content, soup)
        return content

    def _extract_content_by_html(self, raw_content, url, **kwargs):
        try:
            soup = GorgeousSoup(raw_content,
                                unwanted_selectors=self._unwanted_selectors,
                                starting_selectors=self._starting_selectors,
                                ending_criteria=self._ending_criteria)
        except ValueError:
            raise ParseError('{} cannot parse {}'.format(self.PARSER_NAME, url))

        logger = logging.getLogger(self.PARSER_NAME)
        self.url = url
        self.cover_info = self._parse_cover_info(soup)
        self.keywords = self._parse_keywords(soup)
        self.images, self.videos, self.page_content = [], [], []

        for soup, url in self.multi_page_article(soup, url):
            self.content = []
            for item in soup.all_items:
                if isinstance(item, NavigableString):
                    self.content.append(unicode(item))
                elif any([self.special_case(item),
                          self.image_case(item),
                          self.video_case(item),
                          self.header_case(item)]):
                    soup.consume(item)
            self.page_content.append(self.post_process(self.content, soup))
        self.content = '\n'.join(self.page_content)

        parsed_content = ParsedContent(url=url, language=detect_supported_language(self.content),
                                       content=self.content, keywords=self.keywords,
                                       images=self.images, videos=self.videos)
        parsed_content.use_contained_media = (len(self.images) + len(self.videos)) >= 4

        logger.info('=' * 20 + 'TITLE' + '=' * 20 + '\n' + self.cover_info.title)
        logger.info('=' * 20 + 'COVER' + '=' * 20 + '\n' + self.cover_info.cover_image)
        logger.info('=' * 20 + 'IMAGES' + '=' * 20 + '\n' + '\n'.join(self.images))
        logger.info('=' * 20 + 'VIDEOS' + '=' * 20 + '\n' + '\n'.join(self.videos))
        logger.info('=' * 20 + 'CONTENT' + '=' * 20 + '\n' + self.content)
        logger.info('=' * 20 + 'use_contained_media={}'.format(parsed_content.use_contained_media) + '=' * 20)

        return Result(self.cover_info, parsed_content)
