# Open label.txt & answer.txt
with open('labels.txt', 'r',encoding="utf-8") as f_label, open('answer.txt', 'r',encoding="utf-8") as f_answer:

    labels = f_label.readlines()
    answers = f_answer.readlines()

    # Count the number of unequal rows
    count_diff = 0
    # Compare the contents of the two files
    for label, answer in zip(labels, answers):
        answer = answer.strip()
        label=label.strip()
        if(answer == '1' or answer== "paraphrase"):
            answer = '1'
        if(answer == '0' or answer== "not_paraphrase"):
            answer = '0'
        if label != answer:
            count_diff += 1

print("Unequal numbers of lines：", count_diff)
