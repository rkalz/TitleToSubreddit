import urllib.request
import json

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def reddit_elasticsearch_title(args):
    src = "https://elastic.pushshift.io/rs/submissions/_search?q=" + args
    res = []
    data = json.loads(AppURLopener().open(src).read().decode('utf-8'))['hits']['hits']
    for obj in data:
        res.append(obj['_source']['title'])
    return res