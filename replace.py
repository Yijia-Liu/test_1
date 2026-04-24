import string
from keybert import KeyBERT
from getIndex import swap_words


def replace_characters(sentence):
    replacements = {
        'a': 'а',   #0430
        'b': 'Ꮟ',   #13CF
        'c': '∁',   #2201
        'd': 'ԁ',   #0501
        'e': 'е',   #0435
        'f': 'ƒ',   #0192
        'g': 'ց',   #0261
        'h': 'һ',   #04BB
        'i': 'Ꭵ',    #13A5
        'j': 'ϳ',   #03F3
        'k': '𝑘',   #D835
        'l': 'ا',   #0627
        'n': 'ո',   #0578
        'm': 'rn',
        'o': '𐓪',   #D801
        'p': 'ⲣ',   #2CA3
        'q': 'ԛ',   #051B
        'r': 'г',   #0433
        's': 'ꮪ',   #ABAA
        't': 'ʈ',   #0288
        'u': 'ս',   #057D
        'v': 'ν',   #03BD
        'w': 'ꮃ',   #AB83
        'x': 'х',   #0445
        'y': 'у',   #0443
        'z': 'ꮓ'    #AB93
    }

    for old, new in replacements.items():
        sentence = sentence.replace(old, new)

    return sentence


def keyword_del(sentence, keywords_low):
    words_in_sentence = sentence.translate(str.maketrans('', '', string.punctuation)).split()
    new_keywords = []
    for keyword, value in keywords_low:
        for word in words_in_sentence:
            if keyword != word and keyword.lower() == word.lower():
                new_keywords.append((word.capitalize(), value))
            elif keyword == word:
                new_keywords.append((keyword, value))
    return new_keywords



model_path = "D:/Bert"
kw_model = KeyBERT(model=model_path)


with open("Oxford_Word_List.txt", "r") as f:
    word_set = set(f.read().splitlines())
i = 1
# Read questions and sentences from files
with open('premise.txt', 'r', encoding='utf-8') as q_file, \
        open('hypothesis.txt', 'r', encoding='utf-8') as s_file, \
        open('premise_replace.txt', 'w', encoding='utf-8') as q_replace_file, \
        open('hypothesis_replace.txt', 'w', encoding='utf-8') as s_replace_file:
    for premise, hypothesis in zip(q_file, s_file):
        # Extract keywords from sentences
        keywords_premise_low = kw_model.extract_keywords(premise, keyphrase_ngram_range=(1, 1))
        keywords_hypothesis_low = kw_model.extract_keywords(hypothesis, keyphrase_ngram_range=(1, 1))
        keywords_premise = keyword_del(premise, keywords_premise_low)
        keywords_hypothesis = keyword_del(hypothesis, keywords_hypothesis_low)
        # Find common words between question and sentence
        common_words = set(premise.split()) & set(hypothesis.split())

        # Replace common words in sentence
        for word in common_words:
            premise = swap_words(premise, word, word_set)
            premise = premise.replace(word, replace_characters(word))
        for word in common_words:
            hypothesis = swap_words(hypothesis, word, word_set)
            hypothesis = hypothesis.replace(word, replace_characters(word))
        # Replace keywords in sentence
        for keyword, _ in keywords_premise:
            premise = swap_words(premise, keyword, word_set)
            premise = premise.replace(keyword, replace_characters(keyword))

        # Replace keywords in question
        for keyword, _ in keywords_hypothesis:
            hypothesis = swap_words(hypothesis, keyword, word_set)
            hypothesis = hypothesis.replace(keyword, replace_characters(keyword))

        # Write replaced sentences to files
        q_replace_file.write(premise)
        s_replace_file.write(hypothesis)
        i+=1
        print(i)