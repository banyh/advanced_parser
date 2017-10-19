# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import re
from PIL import ImageFile
from collections import namedtuple
try:
    from urllib.parse import urljoin, urlparse
    from urllib.request import urlopen, Request
except:
    from urlparse import urljoin, urlparse
    from urllib2 import urlopen, Request
try:
    unicode = unicode
except:
    unicode = str


class ParseError(Exception):
    pass


class ParsedContent(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        if name == 'videos':
            return []
        elif name == 'images':
            return []
        elif name == 'keywords':
            return []
        elif name == 'use_contained_media':
            return False
        else:
            return ''


class CoverInfo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return ''


Result = namedtuple('Result', ['cover_info', 'parsed_content'])


def is_youtube(path):
    if not path:
        return False
    return urlparse(path).netloc in (
        'youtube.com', 'www.youtube.com', 'm.youtube.com', 'gaming.youtube.com',
        'youtu.be', 'www.youtu.be',  # Shortened video links
    )


def parse_cover_info_basic(parser, soup):
    article_title = soup.find_all('meta', property='og:title')[0].attrs['content']
    article_title = re.sub(' \| .*', '', article_title)
    try:
        cover_image = soup.find_all('meta', property='og:image')[0].attrs['content']
        cover_info = CoverInfo(title=article_title, cover_image=cover_image)
    except:
        cover_info = CoverInfo(title=article_title)
    return cover_info


def parse_keywords_empty(parser, soup):
    return []


def parse_keywords_meta(parser, soup):
    meta_tags = soup.find_all('meta', {'name': 'keywords'})
    if meta_tags:
        meta = meta_tags[0]
        kws = meta.attrs.get('content', '').split(',')
        return [kw.strip() for kw in kws]
    return []


def post_remove_whitespaces(parser, content, soup):
    lines = re.sub('\n\n+', '\n\n', content.replace('\r', '').replace('\t', ' ')).split('\n')
    lines = [ln.strip() for ln in lines]
    return '\n'.join(lines)


def post_remove_oneline_link(parser, content, soup):
    lines = content.split('\n')
    atext = [item.text for item in soup.find_all('a') if len(item.text)]
    new_lines = []
    for ln in lines:
        link_text_length = list(map(len, filter(lambda t: t in ln, atext)))
        if link_text_length:
            relative_diff = float(max(link_text_length)) / len(ln)
            if len(ln) < 80 and relative_diff > 0.7:
                continue  # remove this line
            elif len(ln) < 60 and relative_diff > 0.65:
                continue  # remove this line
            elif len(ln) < 40 and relative_diff > 0.6:
                continue  # remove this line
        new_lines.append(ln)
    return '\n'.join(new_lines)


def check_image_resource(url):
    '''reference: https://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
    '''
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    connection = urlopen(req)
    assert connection.code == 200
    p = ImageFile.Parser()
    for i in range(100):  # at most read 100KB data
        # 根據實際測試的結果，jpeg大部分在i=0讀到size，最多看過i=27才能讀到的情況
        # png則大部分在i=0~5會讀到size，最多看過i=28才讀到的情況
        data = connection.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            connection.close()
            return p.image.size
    connection.close()
    return (0, 0)


def parse_img_tag(parser, item):
    if item.name != 'img':
        return False
    src = item.attrs.get('src', item.attrs.get('data-src', None))
    if not src:
        return False

    if src.startswith('//'):
        src = urlparse(parser.url).scheme + ':' + src
    if not src.startswith('http'):  # relative path
        src = urljoin(parser.url, src)

    # if it's reachable, urlopen will instantly return code == 200
    # and we'll read partial file to get the size of the image
    # if it's unreachable, urlopen may raise Exception or Error
    try:
        width, height = check_image_resource(src)
        if width < 100 or height < 100:
            return False
    except:
        return False

    title = item.attrs.get('title', item.attrs.get('alt', ''))
    if re.match('.*\.(jpg|png|bmp)', title.lower()):
        title = ''
    elif re.match('^[A-Za-z0-9_\-]+$', title.lower()):
        title = ''
    parser.content.append('\n' + src + '?gliatype=image\n')
    parser.images.append(src)
    if title:
        parser.content.append('\n▲' + title + '\n')
    return True


def parse_youtube_iframe_tag(parser, item):
    src = item.attrs.get('src', item.attrs.get('data-src', ''))
    if item.name == 'iframe' and is_youtube(src):
        parser.content.append('\n' + src + '?gliatype=video\n')
        parser.videos.append(src)
        return True
    else:
        return False


def parse_h1_to_h4_tag(parser, item):
    if item.name not in ('h1', 'h2', 'h3', 'h4'):
        return False
    if 'font-size' in item.attrs.get('style', ''):  # real header should not have font-size
        return False
    text = item.text.replace('\n', ' ').strip()
    if not text:
        return False
    parser.content.append('<b>{}</b>'.format(text))
    return True
