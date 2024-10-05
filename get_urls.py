"""
拿到需要的章节名和对应的url, 输入为urls.txt
"""

from bs4 import BeautifulSoup
import requests

a = BeautifulSoup(
    requests.get('https://pages.cs.wisc.edu/~remzi/OSTEP/').content,
    'html.parser'
    ).find('table').find_all('a')

pdfs: list[tuple[str]] = []
for elem in a:
    url: str | None = elem.get('href')
    if url is not None and url.endswith('.pdf'):
        pdfs.append((elem.text, url))

with open('urls.txt', 'x') as f:
    for section, url in pdfs:
        f.write(f'{section.strip()},{url}\n')