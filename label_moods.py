"""
Roughly label moods in tweets (using regexes)

04/02/16
V
"""
from re import sub, split


"""Constants"""
common_path = "/home/bashlovk/code/world_mood"
unlabeled_fn = "sts_gold_v03/sts_gold_tweet.csv" 

def remove_handles(str):
    """ Remove twitter handles like @tweet_author from a string """
    return sub(r'@\w{1,15}', "", str)

def load_tweet_dict(fn):
    tweets = dict()
    try:
        with open(fn) as fp:
            fp.readline() # skip first line, the header "id;polarity;tweet"
            for line in fp:
                """ magic split respecting the quotes, from:
                http://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python """
                tweet_list = split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line)
                tweet_list = [x[1:-1] for x in tweet_list] # strip quotes
                assert(len(tweet_list) == 3) 
                tweet_list[2] = remove_handles(tweet_list[2])
                tweets[int(tweet_list[0])] = tweet_list[1:]
    except IOError as e:
        print("Can't open file " + fn)
    return tweets

if __name__ == '__main__':
    # load unlabeled data
    tweet_dict = load_tweet_dict(unlabeled_fn)
    for tweet in tweet_dict.items():
       print(tweet)
    # label?? 
    
