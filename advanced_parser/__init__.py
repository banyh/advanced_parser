import re
from .helper import ParsedContent, CoverInfo, ParseError
from .basic_parser import BasicParser
from .advanced_parser import AdvParser, GorgeousSoup
from .detectlang import detect_supported_language

from .parser_excite import ExciteParser
from .parser_oricon import OriconParser
from .parser_qq import QQSportParser
from .parser_sohu import SohuParser
from .parser_sina import SinaParser
from .parser_xinhua import XinhuaParser


_parser_url_matcher = [
    ('.*excite\.co\.jp.*', ExciteParser),
    ('.*oricon\.co\.jp.*', OriconParser),
    ('.*sports\.qq\.com.*', QQSportParser),
    ('.*sports\.sohu\.com.*', SohuParser),
    ('.*sina\.com.*', SinaParser),
    ('.*xinhuanet\.com.*', XinhuaParser),
]


def auto_parse(url):
    parser = None
    for pattern, cls in _parser_url_matcher:
        if re.match(pattern, url, flags=re.IGNORECASE):
            parser = cls()
            break

    if parser:
        raw = parser.extract_raw_data(url)
        result = parser.extract_parsed_content(raw, url)
        return result
    return None
