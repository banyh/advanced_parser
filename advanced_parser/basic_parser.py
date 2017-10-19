import re
import logging
from newspaper import Article
try:
    from urllib.parse import urljoin, urlparse
    from urllib.request import urlopen, Request
except:
    from urlparse import urljoin, urlparse
    from urllib2 import urlopen, Request
from .helper import (
    ParseError,
    ParsedContent,
    Result,
)


class BasicParser(object):
    PARSER_NAME = 'BasicParser'

    def extract_raw_data(self, url, **kwargs):
        article = Article(url)
        article.download()
        return article.html

    def _extract_content_by_article(self, raw_content, url, is_html=True, **kwargs):
        images = re.findall(r'http.*gliatype=image', raw_content)
        videos = re.findall(r'http.*gliatype=video', raw_content)
        images = [re.sub('\?gliatype=(image|video)', '', u) for u in images]
        videos = [re.sub('\?gliatype=(image|video)', '', u) for u in videos]

        logger = logging.getLogger(self.PARSER_NAME)
        logger.info('=' * 20 + 'IMAGES' + '=' * 20)
        for url in images:
            logger.info(url)
        logger.info('=' * 20 + 'VIDEOS' + '=' * 20)
        for url in videos:
            logger.info(url)
        logger.info('=' * 20 + 'CONTENT' + '=' * 20)
        logger.info(raw_content)

        parsed_content = ParsedContent(url=url,
                                       language=detect_supported_language(raw_content),
                                       content=raw_content,
                                       keywords=[],
                                       images=images,
                                       videos=videos)
        if len(images) >= 3:
            parsed_content.use_contained_media = True

        return Result(None, parsed_content)

    def extract_parsed_content(self, raw_content, url, is_html=True, **kwargs):
        if is_html:
            return self._extract_content_by_html(raw_content, url, **kwargs)
        else:
            return self._extract_content_by_article(raw_content, url, **kwargs)
