#coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def webscrape():
    print('## webscrape')
    base_url = "https://www.town.hokkaido-mori.lg.jp/"

    options = webdriver.ChromeOptions()
    # options = Options()
    options.binary_location = '/opt/headless-chrome/headless-chromium'
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")

    driver = webdriver.Chrome('/opt/headless-chrome/chromedriver', options=options)
    print('## driver make ok')
    driver.get(base_url)
    # driver.get("http://www.yomiuri.co.jp/")
    time.sleep(0.3)
    html = driver.page_source.encode("utf-8")
    # html = 'テスト投稿です'
    return shaping_data(base_url, html)


def shaping_data(base_url, html):

    # 以下にスクレイピングのコードを記載
    print('shapint_data')
    soup = BeautifulSoup(html, "html.parser")

    #get headlines
    mainNewsIndex = soup.find("ul", attrs={"class", "shinchaku"})
    mainNewsContent = mainNewsIndex.find("li")
    title = mainNewsContent.find("a").text
    link = urljoin(base_url, mainNewsContent.find("a").attrs["href"])
    date = mainNewsContent.find("span", attrs={"class", "date"}).text
    tweet_data = title + '\n' + date + '\n' + link
    print('## tweet_data')
    print(tweet_data)
    return tweet_data


# if __name__ == "__main__":
#     print(webscrape())
