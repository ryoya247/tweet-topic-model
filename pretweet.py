from getTwitter import get_tweets_by_userlist, get_follow_ids

print('user name')
name = input('>> ')

get_tweets_by_userlist(name, get_follow_ids(name))
