from getTwitter import get_tweets_by_search
from datetime import datetime, date, timedelta

today = datetime.today()
s_today = datetime.strftime(today, '%Y-%m-%d')

input_dic = {
    'tag': '#wataten',
    'sdate': s_today,
    'udate': s_today,
    'stime': '00:30:00',
    'utime': '01:30:00'
}

get_tweets_by_search(input_dic)
