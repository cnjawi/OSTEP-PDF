"""
手动将 urls.txt 排序为 structured_urls.txt 后, 再下载所有pdf文件
"""

# Note: 章节名 I/O Devices 不能作为文件名，被修改为 IO Devices

import asyncio
import os
import aiohttp

def gen_cnt():
    cnt = 0
    def cnter():
        nonlocal cnt
        res = f'0{cnt}' if cnt < 10 else str(cnt)
        cnt += 1
        return res
    return cnter

cnt = gen_cnt()

book: dict[str, list] = {}
chapters = []
with open('structured_urls.txt') as f:
    for line in f.readlines():
        if line == '\n':
            continue
        if line.startswith('- '):
            chapter = line[2:-1]
            chapters.append(chapter)
            book[chapter] = []
            continue
        filename, url = line.split(',')
        filename = f'{cnt()} {filename}'
        url = 'https://pages.cs.wisc.edu/~remzi/OSTEP/' + url
        book[chapter].append((filename, url))

# for c in chapters:
#     print(c)
#     for i in book[c]:
#         print(i)

if not os.path.exists('OSTEP'):
    os.mkdir('OSTEP')

for c in chapters:
    if os.path.exists(f'OSTEP/{c}'):
        raise Exception('Directory is not empty!')
    os.mkdir(f'OSTEP/{c}')

async def download(session: aiohttp.ClientSession, chapter: str, file: tuple[str]):
    filename, url = file
    print(f'Downloading: {filename}')

    async with session.get(url) as res:
        if res.status != 200:
            print(f'Unable to download {filename}, status {res.status}')
            return
        with open(f'OSTEP/{chapter}/{filename}.pdf', 'wb') as f:
            f.write(await res.content.read())
    print(f'Finish downloading {filename}')

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for c in chapters:
            for f in book[c]:
                tasks.append(download(session, c, f))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
