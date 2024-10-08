# OSTEP-PDF

OSTEP即*Operating Systems: Three Easy Pieces*，是操作系统课的经典教材。这本书在其官网可以免费阅读，但是是以分章节的形式。可将这些拆开的章节重新组合成完整的一份pdf文档，并且带有完整的大纲。

### 获取url列表

首先要拿到所有的章节名称和对应的url，以供后续下载。通过python解析html的方法解决，用到`requests`和`beautifulsoup4`两个库，参见`get_urls.py`

### 整理

由于下载到的数据很难通过代码来整理，需要手动将这些章节信息整理好，得到structured_urls.txt

### 下载pdf

实际下载通过异步的方式缩短时间，用到`aiohttp`库，为了确保后续操作时章节文件有序，在文件名前添加了两位数字序号，参见`dl.py`

### 合并文件

现在得到了所有章节文件，把它们合并起来就完成了。使用Acrobat的合并文件工具，它在合并文件时会根据文件名自动生成大纲，这也是拿章节名做文件名的目的（伏笔回收）。首先合并各Chapter，得到Intro.pdf、Virtualization.pdf等，注意合并后的文件名还是改为章节名。然后再把各Chapter合并成全书，这样全书的大纲就具有了分级结构。