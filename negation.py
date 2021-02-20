negating_words = ['aint', 'cannot', 'cant', 'darent', 'didnt',
'doesnt', 'dont', 'hadnt', 'hardly', 'hasnt',
'havent', 'havnt', 'isnt', 'lack', 'lacking',
'lacks', 'neither', 'never', 'no', 'nobody',
'none', 'nor', 'not', 'nothing', 'nowhere',
'mightnt', 'mustnt', 'neednt', 'oughtnt', 'shant',
'shouldnt', 'wasnt', 'without', 'wouldnt', 'n t']

def check (word):
    if word in negating_words:
        return True
    return False
