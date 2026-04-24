from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")


def gpt2(target_word,swapped_list):
    min_similarity = 1
    index = -1
    for i, word in enumerate(swapped_list):
        similarity = cosine(target_word, word)
        if similarity < min_similarity:
            min_similarity = similarity
            index = i + 1
    return index

def cosine(target_word, word):
    input_ids1 = tokenizer.encode(target_word, return_tensors="pt", max_length=512, truncation=True)
    input_ids2 = tokenizer.encode(word, return_tensors="pt", max_length=512, truncation=True)

    with torch.no_grad():
        outputs1 = model(input_ids1, output_hidden_states=True)
        outputs2 = model(input_ids2, output_hidden_states=True)

    last_hidden_state1 = outputs1.last_hidden_state
    last_hidden_state2 = outputs2.last_hidden_state

    vector_representation1 = torch.mean(last_hidden_state1, dim=1).squeeze()
    vector_representation2 = torch.mean(last_hidden_state2, dim=1).squeeze()


    def cosine_similarity(vector1, vector2):
        dot_product = torch.dot(vector1, vector2)
        magnitude1 = torch.norm(vector1)
        magnitude2 = torch.norm(vector2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    similarity = cosine_similarity(vector_representation1, vector_representation2)
    return similarity.item()










