import requests as r
from lxml import etree ##引入html处理库
##伪装用户头，第一步绕过浏览器查询
header={
    "User-Agent":("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0")
}
for c in range(1,10):
    res=r.get(f'https://books.toscrape.com/catalogue/page-{c}.html',headers=header)##发现链接是根据数字来的循环一个一个爬
    html2=etree.HTML(res.text)##把爬到的数据处理成树型结构方便下面xpath处理
    print(f'正在爬第{c}页')
    text_list=html2.xpath('//h3/a/@title')##提取h3大小再找下面子标签a下面的子标签title
    modify='\n'.join([i.strip()for i in text_list if i.strip()])##以换行符分割如果提取内容不为空
    writ=open('requests_file.txt','a+',encoding='utf8')
    writ.write(modify)
writ.close()