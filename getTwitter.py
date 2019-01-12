import json, os, urllib
import os.path
from requests_oauthlib import OAuth1Session
from pprint import pprint
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

CK = os.environ.get('CONSUMER_KEY')
CS = os.environ.get('CONSUMER_SECRET')
AT = os.environ.get('ACCESS_TOKEN')
ATS = os.environ.get('ACCESS_TOKEN_SECRET')

twitter = OAuth1Session(CK, CS, AT, ATS)

timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
follow_endpoint = "https://api.twitter.com/1.1/friends/ids.json"
search_endpoint = "https://api.twitter.com/1.1/search/tweets.json"

def exstract_texts(timeline):
    tweet_list = []
    for tweet in timeline:
        if tweet['text'].find('\n'):
            tweet['text'] = tweet['text'].replace('\n','')
        tweet_list.append(tweet['text'])
    return tweet_list


def get_follow_ids(screen_name):
    follow_list = []
    params = {
        'screen_name': screen_name,
        'stringify_ids': True,
        'count': 500
    }
    res = twitter.get(follow_endpoint, params=params)
    if res.status_code == 200:
        fl = json.loads(res.text)
        follow_list = fl['ids']
        pprint(follow_list)
        print('フォロー数', len(follow_list))
        return follow_list


def get_tweets_by_userlist(name, follow_list):
    if not os.path.exists('./text/{}'.format(name)):
        os.mkdir('./text/{}'.format(name))
    for uid in follow_list:
        print('='*100)
        print('user id：', uid)
        timelines = []
        append_timelines = []
        params = {}
        max_id = None
        new_max_id = None
        for i in range(3):
            if i == 0:
                # print('最初のリクエスト')
                params = {
                    'count': 200,
                    'user_id': uid,
                    'exclude_replies': True,
                    'include_rts': False
                }
            else:
                # print('%d番目のリクエスト' % i)
                params = {
                    'count': 200,
                    'user_id': uid,
                    'max_id': max_id,
                    'exclude_replies': True,
                    'include_rts': False
                }

            res = twitter.get(timeline_endpoint, params=params)

            if res.status_code == 200:
                append_timelines = json.loads(res.text)
                print('append tweets：', len(append_timelines))
                if len(append_timelines) > 0:
                    new_max_id = append_timelines[-1]['id']
                    if max_id != new_max_id:
                        timelines = timelines + append_timelines
                        max_id = new_max_id
                    else:
                        break
                else:
                    break;
            else:
                print('*** status error ***')
                break
        tl = exstract_texts(timelines)
        if len(tl) > 100:
            tweets_txt = './text/{}/{}.txt'.format(name,uid)
            with open(tweets_txt, 'w', encoding='utf-8') as fp:
                fp.write('\n'.join(tl))
            print('total tweets：', len(timelines))
        else:
            print('too few data')


def get_tweets_by_search(input_dic):
    timeline = []
    tag = input_dic['tag']
    sdate = input_dic['sdate']
    udate = input_dic['udate']
    stime = input_dic['stime']
    utime = input_dic['utime']

    since = sdate + '_' + stime + '_JST'
    until = udate + '_' + utime + '_JST'

    if not os.path.exists('./text/{}'.format(tag)):
        os.mkdir('./text/{}'.format(tag))
    for i in range(20):
        if i == 0:
            print('request 0')
            params = {
                'q': tag,
                'result_type': 'mixed',
                'count': 100,
                'exclude': 'retweets',
                'since': since,
                'until': until
            }
        else:
            print('request {}'.format(i))
            params = {
                'q': tag,
                'max_id': max_id,
                'result_type': 'mixed',
                'count': 100,
                'exclude': 'retweets',
                'since': since,
                'until': until
            }
        res = twitter.get(search_endpoint, params=params)
        if res.status_code == 200:
            append_timelines = json.loads(res.text)
            atl = exstract_texts(append_timelines['statuses'])
            timeline = timeline + atl
            next_results = append_timelines['search_metadata'].get('next_results')
            if next_results != None:
                max_id = urllib.parse.parse_qs(append_timelines['search_metadata']['next_results'])['?max_id'][0]
            else:
                break

    tweets_txt = './text/{}/{}.txt'.format(tag,sdate)
    with open(tweets_txt, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(timeline))
