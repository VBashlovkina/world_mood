"""
Roughly label moods in tweets (using regexes)

04/02/16
V

Not super good with regexes, so some wisdom borrowed from StackOverflow (cited)
"""
from re import sub, split, compile


"""Constants"""
common_path = "/home/bashlovk/code/world_mood"
unlabeled_fn = "sts_gold_v03/sts_gold_tweet.csv" 


""" Pre-compiling regexes effectively generates the corresponding DFA,
    which makes matching faster
"""

""" Split respecting the quotes, from:
http://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
"""
split_RE = compile(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''')
def split_wrt_quotes(str):
    return split_RE.split(str)

""" Remove twitter handles like @tweet_author from a string """
handles_RE = compile(r'@\w{1,15}')
def remove_handles(str):
    return handles_RE.sub("", str)

""" Remove quotes """
quotes_RE = compile("&quot;")
def remove_quotes(str):
    return quotes_RE.sub("", str)

""" Remove urls, from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
"""
url_RE = compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
def remove_urls(str):
    return url_RE.sub("", str)

""" Concatenate contractions """
contraction_RE = compile("\w'\w")
def concat_contractions(str):
    return contraction_RE.sub("", str)

""" Replace punctuation with whitespace """
punctuation_RE = compile("[^a-zA-Z]")
def remove_punctuation(str):
    return punctuation_RE.sub(" ", str)

""" Replace all whitespace clusters with single spaces """
whitespace_RE = compile("\s+")
def remove_whitespace(str):
    return whitespace_RE.sub(" ", str)

""" Remove stopwords """
stopwords_RE = compile("(the|a|an|i|you|we|she|he|it|me)")
#TODO

""" Return a list of ngrams up to specified length
    Pre: str is stripped of leading and trailing whitespace
    Default ngram length is 3.

    Example:
    > get_ngrams('a b c d')
    ['a', 'b', 'c', 'd', 'a b', 'b c', 'c d', 'a b c', 'b c d']
"""
def get_ngrams(str, num=3):
    ngrams = []
    words = str.split(' ')
    for i in range(num):
        for j in range(len(words) - i):
            ngrams.append(' '.join(words[j:j+1+i]))
    return ngrams
        
def load_tweet_dict(fn):
    tweets = dict()
    try:
        with open(fn) as fp:
            fp.readline() # skip first line, the header "id;polarity;tweet"
            for line in fp:
                tweet_list = split_wrt_quotes(line)
                tweet_list = [x[1:-1] for x in tweet_list] # strip quotes
                assert(len(tweet_list) == 3)
                
                # Clean the tweet text
                clean = remove_handles(clean)
                clean = remove_quotes(clean)
                clean = remove_urls(clean)
                clean = concat_contractions(clean)
                clean = remove_punctuation(clean)
                clean = remove_whitespace(clean)
                clean = clean.strip()
                clean = clean.lowercase()
                #clean = remove_stopwords(clean) TODO
                # TODO: limit repeating letters to 1 or 2? eg "neeeeeeeeed"

                # Add ngrams
                tweet_list.append(get_ngrams(clean))
                tweets[int(tweet_list[0])] = tweet_list[1:]
    except IOError as e:
        print("Can't open file " + fn)
    return tweets

if __name__ == '__main__':
    # load unlabeled data
    tweet_dict = load_tweet_dict(unlabeled_fn) # id: [old_label, text, ngrams]
    for tweet in tweet_dict.items():
       print(tweet)

    # add approximate labeling   
    for key in tweet_dict.keys():
        tweets[key] = add_emotions(tweets[key][2]) # [4] = [happy, sad, blah]
        tweets[key] = add_classification(tweets[key][4])
        print(tweets[key][1])

    
        
    
