from getTwitter import get_tweets_by_search

input_data = {}

print('input hash tag')
input_data['tag'] = input('>> ')
print('input date ( yyyy-mm-dd )')
input_data['target_date'] = input('>> ')
print('='*60)
print('next, input since time... ( hh:mm:ss )')
input_data['stime'] = input('>> ')
print('next, input until time... ( hh:mm:ss )')
input_data['utime'] = input('>> ')

get_tweets_by_search(input_data)
