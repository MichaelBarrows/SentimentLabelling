import helpers
import dataset as ds
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
import re
from operator import itemgetter
# import negation
import pandas as pd

stemmer = PorterStemmer()

# hold the counts for each sentiment category (overall)
score_counter = {"Positive": 0,
                 "Negative": 0,
                 "Neutral": 0}

# stemming()
# parameters:
#   word : string - the word to be stemmed
# returns:
#   word : string - the stemmed version of the word
# description:
#   This function stems a word using the NLTK Porter Stemmer and changes stemmed
#       words ending with 'i' to end with 'y' for compatibility with WordNet.
def stemming (word):
    global stemmer
    word = stemmer.stem(word)
    if word.endswith('i'):
        word = word[:-1]
        word = word + 'y'
    return word

# synset_matching()
# parameters:
#   word : string - the word for which synsets are to be found
#   pos : string - the part-of-speech tag (WordNet format) for the word
#   tweet_text : string - the preprocessed text of the tweet
#   original_text : string - the original unmodified text of the tweet
# returns:
#   synset_match_sorter() : function call - call to function to identify the
#       best match to be returned
# description:
#   This function looks up a word using wordnet to identify possible synsets of
#       the word. The correct synset is automatically determined. The word sense
#       disambiguation performed in ths function includes POS tagging (if
#       provided), and then by comparing the number of matches the synset
#       definition has with the original tweet text.
#   For a synset to be considered, the word must match either the name of the
#       synset, the lemma names of the synset or the stemmed word must match the
#       name of the synset.
#   The synset_match_sorter() function is then called to identify the best match
#       to be returned.
def synset_matching (word, pos, tweet_text, original_text):
    if pos != None:
        all_synsets = wn.synsets(word, pos)
    else:
        all_synsets = wn.synsets(word)
    if len(all_synsets) == 0:
        all_synsets = wn.synsets(word)
    matches = {}
    first_synset = None
    for synset in all_synsets:
        # default/fallback option
        if first_synset == None:
            first_synset = synset.name()
        synset_name = synset.name().split('.')[0]
        # check if the word is in the lemma names for this synset
        if word in synset.lemma_names():
            match_count, match_percentage = definition_match_checker(synset.definition().lower(), original_text)
            matches[synset.name()] = [match_percentage, match_count]
        # check if the word is the synset name (word part only)
        elif word == synset_name:
            match_count, match_percentage = definition_match_checker(synset.definition().lower(), original_text)
            matches[synset.name()] = [match_percentage, match_count]
        # check if the stemmed version of the word is the synset name (word part only)
        elif stemming(word) == synset_name:
            match_count, match_percentage = definition_match_checker(synset.definition().lower(), original_text)
            matches[synset.name()] = [match_percentage, match_count]
    return synset_match_sorter(matches, first_synset)

# synset_match_sorter()
# parameters:
#   matches : dict - dictionary containing the matches to be sorted
#   first_synset : string - the name of the first synset found (first synset is
#       most common occurance) - to be used as a fallback if there are no other
#       matches
# returns:
#   top_synset : string - the name of the best matched wordnet synset
# description:
#   This function sorts the matches and determines which match is the 'best'
#       for the given word.
#   The order for match priority is:
#       - highest percentage
#       - highest count
#       - default/fallback
def synset_match_sorter (matches, first_synset):
    if len(matches) == 0:
        return None
    matches_list = []
    for item in matches:
        matches_list.append([item, matches[item][0], matches[item][1]])
    matches = sorted(matches_list, key = lambda x: x[1], reverse = True)
    first = True
    top_match = [None, None, None]
    for match in matches:
        if first == True:
            top_match = [match[0], match[1], match[2]]
            first = False
            continue
        else:
            if match[1] > top_match[1]:
                top_match = [match[0], match[1], match[2]]
            elif match[1] == top_match[1]:
                if match[2] > top_match[2]:
                     top_match = [match[0], match[1], match[2]]
    return top_match[0]


    # matches = sorted(matches.items(), key=itemgetter(1), reverse=True)
    # top_match_percentage = None
    # top_match_count = None
    # top_synset = None
    # for match in matches:
    #     if top_match_count == None:
    #         top_match_percentage = match[1][0]
    #         top_match_count = match[1][1]
    #         top_synset = match[0]
    #     elif top_match_percentage == None and match[1][0] == 0.0:
    #         top_synset = first_synset
    #     elif top_match_percentage == match[1][0]:
    #         if match[1][1] > top_match_count:
    #             top_synset = match[0]
    #     else:
    #         break
    # return top_synset




# definition_match_checker()
# parameters:
#   definition : string - the definition for the synset
#   tweet_text : string - the text of the tweet to be compared against
# returns:
#   counter : integer - the number of matches identified
#   percentage : float - the number of matches (as a percentage of total word
#       in the definition)
# description:
#    This function compares each word in the synset definition to each word in
#       the tweet's text in an attempt to determine the best definition for the
#       word. The word comparison is completed using the stemmed version of the
#       words for consistency. The the original word is checked to see if it is
#       in the definition word and vice versa. The number of matches and the
#       percentage is returned.
def definition_match_checker (definition, tweet_text):
    tweet_text = remove_special_chars(tweet_text)
    tweet_text = word_tokenize(tweet_text)
    definition = remove_special_chars(definition)
    definition = word_tokenize(definition)
    counter = 0
    for d_word in definition:
        for t_word in tweet_text:
            if stemming(d_word) == stemming(t_word):
                counter += 1
            elif d_word in t_word or t_word in d_word:
                counter += 1
    percentage = counter / len(definition)
    return counter, percentage

# remove_special_chars()
# parameters:
#   text : string - the text to be checked and modified
# returns:
#   text : string - the modified text
# description:
#   This function checks a given piece of text for a given set of special
#       characters, and removes them, returning the given text.
def remove_special_chars (text):
    special_chars_list = [['"'],
                          ["'"],
                          ['.', '\.'],
                          ['!'],
                          ['?', '\?'],
                          [','],
                          ['-'],
                          ['_'],
                          ['`'],
                          ['(', '\('],
                          [')', '\)'],
                          ['&amp;', '\&amp;'],
                          ['amp '],
                          ['rt '],
                          ['&gt;', '\&gt;'],
                          ['&lt;', '\&lt;'],
                          ['&', '\&'],
                          ['\n', '\\n'],
                          ['$', '\$'],
                          [':', ':']]
    for special_char in special_chars_list:
        if special_char[0] in text:
            text = re.sub(special_char[-1], ' ', text)
    return text

# pos_tag_conversion()
# parameters:
#   pos : string - the part-of-speech tag to be converted
# returns:
#   wn.NOUN : string - the WordNet pos tag for a noun ('n')
#   wn.VERB : string - the WordNet pos tag for a verb ('v')
#   wn.ADJ : string - the WordNet pos tag for an adjective ('a')
#   wn.ADV : string - the WordNet pos tag for an adverb ('r')
def pos_tag_conversion (pos):
    if pos.startswith("NN"):
        return wn.NOUN
    if pos.startswith("VB"):
        return wn.VERB
    if pos.startswith("JJ"):
        return wn.ADJ
    if pos.startswith("RB"):
        return wn.ADV

# sentiwordnet_processing()
# parameters:
#   synsets : list - a list containing all synsets identified for the given
#       tweet
# returns:
#   high_name : string - string containing the name of the highest category
#   pos_score : float - the positive sentiment score (mean)
#   neg_score : float - the negative sentiment score (mean)
#   obj_score : float - the objectivity score (mean)
# description:
#   This function obtains the sentiment and objectivity scores for a list of
#       synsets to determine the overall positivity/neutrality/negativity of a
#       given tweet.
def sentiwordnet_processing (synsets):
    global score_counter
    pos_score, neg_score, obj_score = 0, 0, 0
    negate_flag = False
    if len(synsets) == 0:
        return
    for wn_synset in synsets:
        synset = swn.senti_synset(wn_synset)
        pos_score += synset.pos_score()
        neg_score += synset.neg_score()
        obj_score += synset.obj_score()
    pos_score = pos_score / len(synsets)
    neg_score = neg_score / len(synsets)
    obj_score = obj_score / len(synsets)
    high_score = 0
    high_score -= 1
    high_name = None
    if pos_score > high_score:
        high_score = pos_score
        high_name = "Positive"
    if neg_score > high_score:
        high_score = neg_score
        high_name = "Negative"
    # positive and negative scores are equal = a tie
    if pos_score == neg_score:
        high_score = pos_score
        high_name = "Neutral"
    # print(high_name, round(high_score,2), "Objective", round(obj_score,2))
    score_counter[high_name] += 1
    return high_name, pos_score, neg_score, obj_score

# dataset_processing()
# parameters:
#   None
# returns:
#   None
# description:
#   This function imports the dataset of tweets, iterates over them, tokenises
#       and gets POS tags (and converts to WordNet POS tags) for each word and
#       calls functions to identify the WordNet synset of the word
#       (synset_matching()). The synset is then stored, and the sentiments for
#       the synsets are retrieved using the sentiwordnet_processing() function.
#       The sentiment scores, objectivity score and sentiment classification is
#       added to the dataframe and stored. The totals for each sentiment
#       category are printed.
def dataset_processing ():
    global score_counter
    df = helpers.load_dataset(ds.dataset)
    df['sentiment_class'] = ""
    df['positive_score'] = ""
    df['negative_score'] = ""
    df['objective_score'] = ""
    df['stemmed_preprocessed_text'] = ""
    df['words_matched_percentage'] = ""
    word_dict = {}
    pos_dict = {}
    for index, row in df.iterrows():
        if index % 100 == 0:
            print("    -", str(index), "/", str(len(df)))
        stemmed_preprocessed_text = []
        synsets = []
        tweet_text = str(row.preprocessed_tweet_text)
        tweet_text = word_tokenize(tweet_text)
        words_with_pos = pos_tag(tweet_text)
        for word, pos in words_with_pos:
            word_synset = synset_matching(word, pos_tag_conversion(pos), tweet_text, row.tweet_text)
            if word_synset != None:
                synsets.append(word_synset)
            stemmed_preprocessed_text.append(stemming(word))
        if len(synsets) > 0:
            sent_class, pos_score, neg_score, obj_score = sentiwordnet_processing(synsets)
            df.sentiment_class.at[index] = sent_class
            df.positive_score.at[index] = pos_score
            df.negative_score.at[index] = neg_score
            df.objective_score.at[index] = obj_score
        stemmed_preprocessed_text = " ".join(stemmed_preprocessed_text)
        df.stemmed_preprocessed_text.at[index] = stemmed_preprocessed_text
        if len(tweet_text) != 0:
            df.words_matched_percentage.at[index] = round(100 * len(synsets) / len(tweet_text), 2)
        else:
            df.words_matched_percentage.at[index] = 0

    for ix in score_counter:
        print(ix, score_counter[ix])
    helpers.path_checker(ds.output_data)
    helpers.dataframe_to_csv(df, ds.output_data + "/sentiwordnet_labelled.csv")

# run()
# parameters:
#   None
# returns:
#   None
# description:
#   This function prints a message explaining what is happening and calls the
#       dataset_processing() function to execute the code
def run ():
    print("Running SentiWordNet Labelling")
    dataset_processing()

# Execute the code
run()
