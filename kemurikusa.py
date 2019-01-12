from getTwitter import get_tweets_by_search
from datetime import datetime, date

today = datetime.today()
s_today = datetime.strftime(today, '%Y-%m-%d')

input_dic = {
    'tag': '#ケムリクサ',
    'sdate': s_today,
    'udate': s_today,
    'stime': '22:30:00',
    'utime': '23:30:00'
}

get_tweets_by_search(input_dic)
