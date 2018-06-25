'''#html中需加入这一句中文才不会乱码“<math http-equiv="Content-Type content="text/html; charset=utf-8" />"
SpiderMain 爬虫中的调度器，面向对象写法，调度器负责从 urlmanager 获取爬取链接，
然后交给 HtmlDownLoader 下载，然后把下载内容交给 HtmlParser 解析，然后把有价值的数据输出给
HtmlOutput 进行应用。
'''
#from AndroidSpider
import url_manager, html_downloader, html_parser, html_output

'''
爬取百度百科 Android 关键词相关词及简介并输出为一个HTML tab网页

Extra module:
BeautifulSoup
'''
class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.parser = html_parser.HtmlParser()
        self.out_put = html_output.HtmlOutput()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("craw %d : %s" % (count, new_url))
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
                }
                html_content = self.downloader.download(new_url, retry_count=2, headers=headers)
                new_urls, new_data = self.parser.parse(new_url, html_content, "utf-8")
                self.urls.add_new_urls(new_urls)
                self.out_put.collect_data(new_data)
                #默认爬取深度 30，不然太慢，自己可以修改。
                if count >= 30:
                    break
                count = count + 1
            except Exception as e:
                print("craw failed!\n"+str(e))
        self.out_put.output_html()

if __name__ == "__main__":
    rootUrl = "http://baike.baidu.com/item/Android"
    objSpider = SpiderMain()
    objSpider.craw(rootUrl)
