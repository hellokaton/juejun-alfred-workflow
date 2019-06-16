#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web, ICON_WEB

reload(sys)
sys.setdefaultencoding('utf8')

SEARCH_URL = "https://extension-ms.juejin.im/resources/gold"

CATEFORY_BANKEND = "bankend"
LIMIT = 30
ORDER_BY = "time"


def load_rencent_posts():
    """
    加载后端的最新 30 条文章
    :return:
    """
    param = {'category': CATEFORY_BANKEND,
             'order': ORDER_BY, 'offset': 0, 'limit': LIMIT}
    r = web.post(url=SEARCH_URL, data=param)
    result = r.json()
    posts = result['data']
    return posts


def add_item(post):
    """
    转换 post 为一个 workflow 的 item
    :return:
    """
    title = post[u'title']
    url = post['url']
    username = post[u'user']['username']
    viewcount = post['viewCount']

    subtitle = "作者: {user} | 阅读量: {viewCount}".format(
        user=username, viewCount=viewcount)
    wf.add_item(
        title=title,
        subtitle=subtitle,
        arg=url,
        valid=True,
        icon=ICON_WEB)


def main(wf):
    # 缓存 1 分钟
    posts = wf.cached_data('posts', load_rencent_posts, max_age=60*60)

    for post in posts:
        add_item(post)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
