# advanced_parser

## 如果你要使用寫好的Parser

```
pip install git+ssh://git@github.com/banyh/advanced_parser.git
```


### 使用方式

```python
from advanced_parser import auto_parse

result = auto_parse('http://www.oricon.co.jp/news/2099207/full/')

result.parsed_content.url  # URL
result.parsed_content.content  # 內文
result.parsed_content.images  # 夾在內文中的圖片
result.parsed_content.videos  # 夾在內文中的影片
result.parsed_content.keywords  # 網站給的關鍵字
result.parsed_content.use_contained_media  # 當圖片加影片超過3個，會設為True
result.cover_info.title  # 標題
result.cover_info.cover_image  # 封面照片
```

## 如果你要開發新的Parser

跟我要權限，然後clone下來。
```
git clone git@github.com:banyh/advanced_parser.git
```

### 新增parser的步驟

1. 新增`parser_xxxxx.py`，裡面定義`class XxxxxParser(AdvParser)`
2. 至少要設定`_starting_selectors, _ending_criteria, post_process_functions`
3. 在`__init__.py`中import，並修改`_parser_url_matcher`
