##目标：拿下标题自动分页,抓取内容与标题
import requests as r
from lxml import etree ##引入html处理库
from urllib.parse import urljoin
from random import uniform,choice
from  time import sleep
from re import sub
##伪装用户头，第一步绕过浏览器查询
User_Agents=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"

]
header={
    "User-Agent":(choice(User_Agents)),
    "Referer":"https://books.toscrape.com",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"

}

def Auto_splicing(html2,current_url,is_next=False):##只能用next_page传回来的
    #next_page = html2.xpath('//li[contains(@class, "next")]/a/@href')  ##xpath返回对应结果的列表，由于网站只有一个下一页所以就是[0]
    if html2:
        if is_next==True:
            return urljoin(current_url,html2[0])##第一个参数是下一次的url[要是列表形式]，第二是上一次(第一次url)
        ##xpath返回的是列表原本是这样但是第三页手动拼接少东西了 return 'https://books.toscrape.com/'+next_page[0]
        else:
            return [urljoin(current_url,i) for i in html2]#每一页书籍列表
    #else:
        #pass
def main():
    page='https://books.toscrape.com/catalogue/page-50.html'##测试最后一页
    books=[]
    while page:##如果有链接就开始
        res1=r.get(f'{page}',headers=header)
        title,next_page,url,text=modify_title(res1)#modify_s有返回值分别存储
        next_url= Auto_splicing(url, page)
        for i,j in zip(title,next_url):
            header["Referer"] = page
            res2=r.get(j,headers=header)
            text_p=modify_text(res2)
            #print("📖 书名：", i)
            #print("📝 内容：", text_p)
            #print("=" * 60)
            books.append({
                "title": i,
                "content": text_p,
                'url':j
            })

            #print(books)##[{'title': 'A Light in the Attic', 'content': "It's hard to imagine a world without...
        page=Auto_splicing(next_page,page,True)
        sleep(uniform(1, 3))
    return books
def modify_title(res):
    html2 = etree.HTML(res.text)  ##把爬到的数据处理成树型结构方便下面xpath处理
    title_list = html2.xpath('//h3/a/@title')  ##提取h3大小再找下面子标签a下面的子标签title
    title_url =html2.xpath('//h3/a/@href')
    text_list=html2.xpath('//div[@id=product_description]/following-sibling::p/text()')##内容
    next_page = html2.xpath('//li[contains(@class, "next")]/a/@href')  ##xpath返回对应结果的列表，由于网站只有一个下一页所以就是[0]
    '''
    preceding-sibling::p：找当前节点之前的同级兄弟节点 p
    following-sibling::*：找当前节点之后所有同级兄弟节点（不管标签是什么）
    following-sibling::a[1]：找当前节点之后第一个同级兄弟节点 <a>
    '''
    ##modify_title = '\n'.join([i.strip() for i in title_list if i.strip()])  ##以换行符分割如果提取内容不为空

    return title_list,next_page,title_url,text_list
def modify_text(res):
    html2 = etree.HTML(res.text)  ##把爬到的数据处理成树型结构方便下面xpath处理
    text_list = html2.xpath('//div[@id="product_description"]/following-sibling::p/text()')  ##内容
    if text_list:
        return text_list[0]
    else:
        return ''
#a=[{'title': 'Frankenstein', 'content':1}
def clean_text(text):
    ls=[]
    sum_title=0
    for i in text:
        if not i:
            continue
        title=sub(r'[\'!@#$%^&*().\-]','',i['title'])
        sum_title+=1
        content=sub(r'[^a-zA-Z\s!@#$%^&*().\'\-]','',i['content']).lower()
        url=i['url']
        ls.append({
            'id':sum_title,
            'title':title,
            'content':content,
            'url':url
        })
    return ls