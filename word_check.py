from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import word_tokenize, pos_tag
import dataset as ds
import helpers

df = helpers.load_dataset(ds.dataset + ds.data)

negation_words = ["not"]
intensifier_words = ["really", "very", "always"]
deminisher_words = ["never"]
applicable_words = ["like", "dislike", "love", "hate", "good", "bad", "great", "awful", "better", "worse", "best", "worst"]

great   love
good    like
okay    okay
bad     dislike
awful   hate

I really hate this phone
         +3 intensify
I really dont hate this phone
         -3 deminish to bad
I like this phone
        -
I really don't like this phone
        intensify to love and flip to hate +3 - (total * 2)
I don't really like this phone
        deminish
def check_negation (word):
    if word in negation_words:
        return word, True
    else:
        return None, False

def check_intensifier (word):
    if word in intensifier_words:
        return word, True
    else:
        return None, False

def check_deminisher (word):
    if word in deminisher_words:
        return word, True
    else:
        return None, False

for index, row in df.iterrows():
    tweet_text = row.preprocessed_tweet_text
    tweet_text = word_tokenise(tweet_text)
    tweet_w_pos = pos_tag(tweet_text)
    for word, pos in tweet_w_pos:
        negation_word, negation_flag = check_negation(word)
        intensifier_word, intensifier_flag = check_intensifier(word)
        deminisher_word, deminisher_flag = check_deminisher(word)
    if negation_word != word and intensifier_word != word and deminisher_word != word:
        if intensifier_flag == True:
            sentiment += 1/2
        elif deminisher_flag == True:
            sentiment -= 1/3
        if negation_flag == True:
            sentiment






for word in applicable_words:
    print(word)
    synsets = wn.synsets(word, 'v')
    for synset in synsets:
        print(synset.lemma_names())
    print()
