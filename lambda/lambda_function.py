#coding:utf-8

from requests_oauthlib import OAuth1Session
from webscrape import getMoriHpNewsList
from webscrape import getMoriHpScreenshot
from subprocess import call
import urllib3
import os
import sys
import logging
import rds_config
import pymysql
import tweepy

CK = os.environ['CK']
CS = os.environ['CS']
AT = os.environ['AT']
AS = os.environ['AS']

URL = 'https://api.twitter.com/1.1/statuses/update.json'

rds_host = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    connection = pymysql.connect(rds_host,
                                 user=name,
                                 passwd=password,
                                 db=db_name,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def lambda_handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    getDataInMoriHpSql = "SELECT title,date,url FROM new_info_in_mori_hp ORDER BY id DESC LIMIT 10"
    putDataToMoriHpSql = "INSERT INTO new_info_in_mori_hp (title,date,url) VALUES (%s,%s,%s)"
    imageUrl = "/tmp/screenshot.png"

    # 過去データの取得
    with connection.cursor() as cur:
        updateData = []
        base_url = "https://www.town.hokkaido-mori.lg.jp/"
        cur.execute(getDataInMoriHpSql)
        pastData = cur.fetchall()
        print("### DBから取得したpastData")
        print(pastData)
        newData = getMoriHpNewsList(base_url)
        print("### Webから取得したnewData")
        print(newData)
        # updateData = set(newData) - set(pastData)

        for newRows in (reversed(newData)):
            duplicateFlg = 0
            for pastRows in pastData:
                if newRows == pastRows:
                    duplicateFlg = 1
            if duplicateFlg == 0:
                updateData.append(newRows)
                cur.execute(
                    putDataToMoriHpSql,
                    (newRows["title"], newRows["date"], newRows["url"]))

    connection.commit()
    connection.close()
    if not updateData:
        return "更新はありません"
    print("### WebにしかないupdateData")
    print(updateData)

    # print(tweet)
    # session = OAuth1Session(CK, CS, AT, AS)
    print('## tweepyの処理 auth = tweepy.OAuthHandler(CK, CS)')
    auth = tweepy.OAuthHandler(CK, CS)
    print('## tweepyの処理 auth.set_access_token(AT, AS)')
    auth.set_access_token(AT, AS)
    print('## tweepyの処理 api = tweepy.API(auth, wait_on_rate_limit=True)')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # params = {"status": tweet}
    # twitter = OAuth1Session(CK, CS, AT, AS)

    for tweet_data in updateData:
        tweet = tweet_data["title"] + '\n' + tweet_data[
            "date"] + '\n' + tweet_data["url"]
        print('### スクリーンショットの取得')
        getMoriHpScreenshot(tweet_data["url"])
        # params = {"status": tweet}
        # req = twitter.post(URL, params=params)
        status = api.update_with_media(filename=imageUrl, status=tweet)
        call('rm -rf /tmp/*', shell=True)

    return 'SUCCESS'
