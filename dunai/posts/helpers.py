from memoize import memoize
from urllib import urlencode
from urllib2 import urlopen
from json import loads


@memoize(timeout=15)
def get_share(url):
    url = 'http://dun.ai/posts/snake-math'
    response = urlopen(
        'https://graph.facebook.com/?' + urlencode(dict(ids=url))
    )
    result = loads(response.read())
    info = result.get(url)
    if info:
        return info.get('share')


def get_share_count(url):
    share = get_share(url)
    if share:
        return share.get('share_count')
    return 0
