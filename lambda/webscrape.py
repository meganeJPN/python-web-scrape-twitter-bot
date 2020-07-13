#coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def getMoriHpNewsList(base_url):
    print('## webscrape')

    # driver = makeDriver(base_url)
    print('## driver make ok')
    print('## driver get ok')
    # driver.get("http://www.yomiuri.co.jp/")
    time.sleep(0.3)
    html = makeDriver(base_url).page_source.encode("utf-8")
    # html = 'テスト投稿です'
    print('## GetTweetList')
    return shapingMoriHpNewsList(base_url, html)


def shapingMoriHpNewsList(base_url, html):
    moriHpNewsList = []
    # 以下にスクレイピングのコードを記載
    print('shapingMoriHpNewsList')
    soup = BeautifulSoup(html, "html.parser")

    #get headlines
    mainNewsIndex = soup.find("ul", attrs={"class", "shinchaku"})
    mainNewsContentList = mainNewsIndex.find_all("li")

    for mainNewsContent in mainNewsContentList:
        title = mainNewsContent.find("a").text
        url = urljoin(base_url, mainNewsContent.find("a").attrs["href"])
        date = mainNewsContent.find("span", attrs={"class", "date"}).text
        moriHpNews = {'title': title, 'date': date, 'url': url}
        # tweet_data = title + '\n' + date + '\n' + link
        print(moriHpNews)
        moriHpNewsList.append(moriHpNews)
    return moriHpNewsList


def getMoriHpScreenshot(base_url):
    print('getMoriHpScreenshot')
    time.sleep(0.3)
    driver = makeDriver(base_url)
    driver.get_screenshot_as_file('/tmp/screenshot.png')


def makeDriver(base_url):
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/headless-chrome/headless-chromium'
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")

    driver = webdriver.Chrome('/opt/headless-chrome/chromedriver',
                              options=options)
    driver.get(base_url)
    return driver


# if __name__ == "__main__":
#     print(webscrape())
