#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web, ICON_WEB


reload(sys)
sys.setdefaultencoding('utf8')


def load_rencent_posts():
    url = 'https://extension-ms.juejin.im/resources/gold'
    param = {'category': 'backend',
             'order': 'time', 'offset': 0, 'limit': 30}
    r = web.post(url=url, data=param)
    result = r.json()
    posts = result['data']
    return posts


def main(wf):
    posts = wf.cached_data('posts', load_rencent_posts, max_age=60*60)

    for post in posts:
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

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
