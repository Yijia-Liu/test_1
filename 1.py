import time

import openai
import requests
import os
# OpenAI API Key
openai.api_key = 'sk-'

os.environ["HTTP_PROXY"] = "http://127.0.0.1:xxxx"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:xxxx"

def ask_gpt(question1,question2):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "For the QQP task, I'll give you questions1 and questions2,reply with 'paraphrase' for paraphrases and 'not_paraphrase' for non-paraphrases."}, {"role": "user", "content": "question1:"+question1 +"\n question2:" +question2}],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def main(i):
    with open('question1_replace.txt', 'r',encoding="utf-8") as q_file:
        question1s = q_file.readlines()
    with open('question2_replace.txt', 'r',encoding="utf-8") as s_file:
        question2s = s_file.readlines()

    with open('answer.txt', 'w',encoding="utf-8") as a_file:
        for question1,question2 in zip(question1s,question2s):
            answer = ask_gpt(question1.strip(),question2.strip())
            i+=1
            time.sleep(0.5)
            print(i)
            print(answer)
            a_file.write(answer + '\n')

if __name__ == "__main__":
    i=0
    main(i)
