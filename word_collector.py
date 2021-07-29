import os
import pandas as pd
import numpy as np
import pymorphy2

#params
batch_patch = 'data/batch_1/'
model_words_path = '/media/alex/nvme-a/vosk-model-ru-0.10/graph/words.txt'


def get_files(path):
    result = []
    for root, dirs, files in os.walk(path):
        files.sort()
        for file in files:
            result.append(path+file)
        return result


def row_strip(s):
    return s.strip()


def word_data(path, split_spaces, correct_symbols = ''):
    
    with open(path, 'rt', encoding="utf8", errors='ignore') as file:
        words = file.read()
    words = words.lower()

    correct = '\nйцукеёнгшщзхъфывапролджэячсмитьбю- '+correct_symbols
    used = ''.join(list(set(words)))
    for u in used:
        if u not in correct:
            words = words.replace(u, ' ')
    while '  ' in words:
        words = words.replace('  ', ' ')
    if split_spaces:
        words = words.replace(' ', '\n')

    words = pd.DataFrame([x.split('\n') for x in words.split('\n')])
    words.columns = ['word']
    #words.drop_duplicates(inplace=True)
    #words.word = words.word.apply('')
    words.word = words.word.apply(row_strip)
    words.word.replace('', np.nan, inplace=True)
    words = words.dropna()
    return words


def words_in_path(path, correct_symbols = ''):
    result = pd.DataFrame()
    new_words_path = get_files(path)
    for path in new_words_path:
        new_word_data = word_data(path, split_spaces = False, correct_symbols = correct_symbols)
        result = pd.concat([result, new_word_data], axis = 0)
    result.reset_index(inplace = True)
    result.drop('index', axis=1, inplace=True)
    result.drop_duplicates(inplace=True)
    result.dropna(inplace=True)
    return result


def drop_waste(s):
    s = ' '+s+' '
    waste_words = [
        'ул.',
        'ш.',
        'пос.',
        '-я',
        'пр-кт',
        'пр.',
        'пл.',
        'ул',
        'б-р',
        'пл',
        'мкрн',
        '-й',
        'шоссе',
        'пер.',
        'пер',
        'москва',
        'б.',
        'м.',
        'проезд',
        'дер.',
        'м-н',
        'пр-д',
        'жк.',
        'микр-н',
        'нов.',
        'стар.',
        'туп.',
        'тер.',
        'г.',
        '-а',
        'вал',
        'кв-л',
        'с.',
        'свх.',
        'бьвар',
        'ж-д',
        'в.о.',
        'п.с.',
        'наб',
        'ый',
        'пр-т.',
        'пр-т.',
        ' наб',
        'мал.',
        'бол.',
        'нов.',
        ' нов ',
        ' сан ',
        'мкр.',
        ' р-н ',
        ' ниж. ',
        ' верхн. ',
        ' линия ',
        ' мкр-он ',
        ' летия ',
        ' -к ',
        ' м-он ',
        ' м-рн ',
        ' ст ',
        ' ст. ',
        ' нижн ',
        ' тер ',
        ' а. '
    ]
    for waste in waste_words:
        if waste in s:
            s = s.replace(waste,'')
    s = s.strip()
    if len(s) and s[0]=='-':
        s = s[1:]
    if len(s)>2 and s[-3]==' пр':
        s = s[:2]
    s = s.strip()
    return s


def drop_single(s):
    s = ' '+s+' '
    result = s
    for i in range(1,len(s)-1):
        #print(s, len(s), i-1, i+1)
        if len(s)>2 and s[i-1]==' ' and s[i+1]==' ':            
            result = s[:(i-1)]+s[(i+1):]
    s = result.strip()
    return s


def multiple_words(s):
    return s if ' ' in s else np.nan


def alone_word(s):
    return np.nan if ' ' in s else s


def replace_e(s):
    return s.replace('ё', 'е')


def replace_minus(s):
    return s.replace('-', ' ')


def replace_dot(s):
    return s.replace('.', ' ')


def replace_double_spaces(s):
    while '  ' in s:
        s = s.replace('  ', ' ')
    s = s.strip()
    return s

model_words_df = pd.read_csv(model_words_path, sep=" ")
model_words_df.columns = ['line', 'id']

# regular
regular = words_in_path(batch_patch+'regular/')

# declined
declined_source = words_in_path(batch_patch+'declined/')
morph = pymorphy2.MorphAnalyzer()
declined_list = []
for ids, missing in declined_source.iterrows():
    original = morph.parse(missing.word)[0]
    for lex in original.lexeme:
        declined_list.append(lex.word)
declined = pd.DataFrame(sorted(set(declined_list)))
declined.columns = ['word']

# mixed
mixed_source = words_in_path(batch_patch+'mixed/', correct_symbols = '.')
mixed_source.word = mixed_source.word.apply(drop_waste)
mixed_source.word = mixed_source.word.apply(drop_single)
mixed_source.word = mixed_source.word.apply(drop_single)
mixed_source.word = mixed_source.word.apply(drop_single)
mixed_source.word.replace('', np.nan, inplace=True)
mixed_source.dropna(inplace=True)
mixed_source.columns = ['word']
mixed_source = pd.DataFrame(set(mixed_source.word))
mixed_source.columns = ['mixed']

mixed_source.mixed = mixed_source.mixed.apply(replace_minus)

mixed_source['alone'] = mixed_source.mixed
mixed_source.alone = mixed_source.alone.apply(alone_word)
mixed_source['multiple'] = mixed_source.mixed
mixed_source.multiple = mixed_source.multiple.apply(multiple_words)

mixed_alone = pd.DataFrame(mixed_source.alone.dropna())
mixed_alone.columns = ['word']
mixed_multiple = pd.DataFrame(mixed_source.multiple.dropna())
mixed_multiple.columns = ['word']

# alone decline
declined_list = []
for ids, missing in mixed_alone.iterrows():
    original = morph.parse(missing.word)[0]
    for lex in original.lexeme:
        declined_list.append(lex.word)
alone_declined = pd.DataFrame(sorted(set(declined_list)))
alone_declined.columns = ['word']

# merge to corpus
corpus = pd.concat([regular, declined, mixed_multiple, alone_declined], axis = 0)
corpus.columns = ['word']
print('corpus merged', len(corpus))
corpus = pd.DataFrame(set(corpus.word))
corpus.columns = ['word']
print('corpus unique', len(corpus))

# replace e
corpus.word = corpus.word.apply(replace_e)

# replace dot
corpus.word = corpus.word.apply(replace_dot)

# replace -
corpus.word = corpus.word.apply(replace_minus)
corpus = pd.DataFrame(sorted(list(corpus.word)))
corpus.columns = ['word']

# drop single
corpus.word = corpus.word.apply(drop_single)

# replace spaces
corpus.word = corpus.word.apply(replace_double_spaces)

# debug++
#corpus = pd.DataFrame(np.array(corpus.word)[:20000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:30000]) # bad
#corpus = pd.DataFrame(np.array(corpus.word)[20000:22000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:23000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:24000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:25000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:26000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:27000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:28000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:29000]) # bad
#corpus = pd.DataFrame(np.array(corpus.word)[28000:29000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[28000:30000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[21000:29000]) # good
#corpus = pd.DataFrame(np.array(corpus.word)[20000:20000]) # good
#corpus.columns = ['word']
# debug--

# missing words
missing = pd.DataFrame(corpus[corpus.word.isin(model_words_df.line)==False])
print('missing', len(missing))
missing.to_csv('corpus.txt', header=None, index = False)
print('corpus.txt', 'build successfully')
