from GPT2 import gpt2

def swap_words(sentence, target_word, word_set):
    if len(target_word) <= 5:
        return sentence

    if not any((target_word.lower() in word.lower() or word.lower() in target_word.lower()) for word in word_set):
        return sentence

    base_index = -(-len(target_word) // 2)


    swapped_list = []
    for i in range(base_index, len(target_word) - 2):
        swapped_words = list(target_word)
        swapped_words[i], swapped_words[i + 1] = swapped_words[i + 1], swapped_words[i]
        swapped_list.append(''.join(swapped_words))

    target_index = base_index + gpt2(target_word,swapped_list)
    try:
        start_index = sentence.index(target_word)
    except:
        return sentence



    total_index = sum(len(word) + 1 for word in sentence[:start_index].split()) + target_index -1

    before_index = sentence[:total_index]
    letter1 = sentence[total_index]
    letter2 = sentence[total_index + 1]
    after_index = sentence[total_index + 2:]

    return before_index + letter2 + letter1 + after_index


