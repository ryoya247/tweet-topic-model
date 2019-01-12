from getTwitter import get_tweets_by_search
from datetime import datetime

today = datetime.today()
s_today = datetime.strftime(today, '%Y-%m-%d')

input_dic = {
    'tag': '#バンドリ2期',
    'sdate': s_today,
    'udate': s_today,
    'stime': '23:00:00',
    'utime': '23:59:00'
}

get_tweets_by_search(input_dic)
