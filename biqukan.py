import sys
import time
import random
import re
import requests
from bs4 import BeautifulSoup


class Biqukan:
    def __init__(self, path, url, headers=""):
        self.novel_name = None
        self.path = path
        self.url = url
        self.headers = headers
        self.tag = 0

    def get_chapter_url(self):
        response = requests.get(self.url)  #
        response.encoding = "gbk"
        directory_content_html = response.text
        chapter_soup = BeautifulSoup(directory_content_html, "html.parser")
        chapters = chapter_soup.select_one("div.listmain").select("dd")[12:]
        self.novel_name = chapter_soup.select_one("div.info > h2").text
        for chapter in chapters:
            chapter_url = "https://www.bqkan8.com" + chapter.a["href"]
            chapter_name = chapter.text
            content_list = self.get_content(chapter_url)
            self.download(chapter_name, content_list)
            time.sleep(random.randint(5, 10))

    def get_content(self, chapter_url):
        """
        chapter_url ----> chapter_part
        :param chapter_url: 每一个章节的url
        :return: 每一章以段落为分隔符的列表
        """
        chapter_object = requests.get(url=chapter_url, headers=self.headers)
        if chapter_object.status_code != 200:
            print(chapter_url, "ERR!")
            print("status_code:", chapter_object.status_code)
            sys.exit()
        chapter_object_html = chapter_object.text
        chapter_soup_object = BeautifulSoup(chapter_object_html, "html.parser")
        # TODO 用来取章节名用的正则
        # title = chapter_soup_object.select_one("div.content > h1").text
        # title_pattern = re.compile(r"(第?(.*)章 *)?(.*)")
        # title_name = re.search(title_pattern, title).group(3)
        chapter_content = chapter_soup_object.select_one("div#content").strings
        return chapter_content

    def download(self, chapter_name, chapter_content):
        """
        :param chapter_name: 章节名字
        :param chapter_content: 章节以段落为分割的列表
        :return: None
        """
        if self.tag == 200:
            self.tag = 0
            time.sleep(7200)
        save_path = self.path + self.novel_name + ".txt"
        with open(save_path, "a+", encoding="utf-8") as f:
            print(chapter_name, "downloading...")
            f.write(chapter_name + "\n\n")
            for paragraph in chapter_content:
                domain_pattern = re.compile(r"((https?)?:\/\/)?\S+\.(com|cn|top|xyz)")
                if re.search(domain_pattern, paragraph):
                    continue
                paragraph = re.sub("\s", "", paragraph)
                f.write("       " + paragraph + "\n")
            f.write("\n\n\n")
            print(chapter_name, "download success!")
        self.tag += 1


if __name__ == '__main__':
    yinianyongheng = "https://www.bqkan8.com/1_1094/"
    # douluodaluo = "https://www.bqkan8.com/1_1496/"
    # yuanzun = "https://www.bqkan8.com/0_790/"
    p = "../data/novel/"
    b = Biqukan(p, yinianyongheng)
    b.get_chapter_url()
