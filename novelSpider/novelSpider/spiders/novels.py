import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from novelSpider.items import NovelspiderItem
import re

def clean_novel_content(content: str) -> str:
    # 清洗数据
    content = content.replace("<br><br>", "\n")
    content = content.replace("<br>", "")
    content = content.replace("&nbsp;", " ")

    clean = re.compile('<.*?>')
    content =  re.sub(clean, '', content)

    return content.split("请收藏本站")[0]



class ExampleSpider(scrapy.Spider):
    name = "novelSpider"
    allowed_domains = []
    start_urls = ["https://www.bqgka.com/book/148135/"]

    def parse(self, response: HtmlResponse):
        # 提取下一个页面的链接
        print("开始爬小说啦！！！")
        # todo: 提取list需要修改
        next_pages = response.css('a::attr(href)').getall()
        for next_page in next_pages:
            if ".html" not in next_page:
                continue
            if next_page is not None:
                # 请求下一个页面
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse_chapter)


    def parse_chapter(self, response: HtmlResponse):
        item = NovelspiderItem()

        # todo: 不同的网站这里不同
        chapter_head = response.css('h1.wap_none::text').get()
        chapterinfo_ary = chapter_head.split(" ")

        # todo: 不同的网站这里不同
        chapter_content_selector = 'div#chaptercontent.Readarea.ReadAjax_content'
        chapter_content = response.css(chapter_content_selector).get()
        # 清洗数据
        chapter_content = clean_novel_content(chapter_content)

        item['chapterNum'] = chapterinfo_ary[0]
        item['chapterTitle'] = chapterinfo_ary[1]
        item['chapterContent'] = chapter_content

        print(f"第{item['chapterNum']}章 {item['chapterTitle']} 爬取完毕！")

        yield item
        


        

