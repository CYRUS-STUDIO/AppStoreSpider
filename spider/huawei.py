# -*- coding: utf-8 -*-
from typing import List

import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import pandas as pd
from time import sleep


@dataclass_json
@dataclass
class Comment:
    accountId: str
    accountName: str
    approveCounts: str
    cipherVersion: str
    commentAppId: str
    commentId: str
    commentInfo: str
    commentType: str
    id: str
    isAmazing: int
    isModified: int
    levelUrl: str
    logonId: str
    nickName: str
    phone: str
    operTime: str
    photoUrl: str
    rating: str
    replyComment: str
    replyCounts: int
    serviceType: str
    stars: str
    title: str
    versionName: str


@dataclass_json
@dataclass
class CommentPage:
    totalPages: int
    count: int
    devWords: List[str]
    list: List[Comment]
    encoding: str = 'utf-8'


class HuaweiSpider:

    @staticmethod
    def commentPage(page) -> CommentPage:
        """
        评论分页
        :param page: 页码，从1开始
        :return:
        """
        url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=%s&maxResults=25&appid=C10763864&version=10.0.0&zone=&locale=zh" % page
        print(url)
        r = requests.get(url, headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,ko;q=0.8,und;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4',
            'Connection': 'keep-alive',
            'Host': 'web-drcn.hispace.dbankcloud.cn',
            'Referer': 'https://appgallery.huawei.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }, verify=False)
        r.encoding = r.apparent_encoding
        if r and r.status_code == 200:
            print(r.content)
            content = CommentPage.from_json(r.content)
            content.encoding = r.encoding
            return content


if __name__ == '__main__':

    page = 1

    columns = ['用户名', '评论', '评分', '评论时间', '版本号', '设备']
    data = []

    while True:
        commentPage = HuaweiSpider().commentPage(page)

        if len(commentPage.list) > 0:
            print(commentPage)
            for row in commentPage.list:
                data.append([row.nickName, row.commentInfo, row.stars, row.operTime, row.versionName, row.phone])
            page += 1

            sleep(2)
        else:
            break

    df = pd.DataFrame(data, columns=columns)
    df.to_excel('华为应用商店评论.xlsx', index=False)
