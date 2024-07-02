from pypdf import PdfReader
import pandas as pd
import sys
import re

global df
df = pd.DataFrame(columns=["question", "choices", "answer"])

def main():
    read_pdf("data/Step_1_Sample_Items (1).pdf", 8, 9)
    print(df)
    
# read pages and extract them into dataframe
def read_pdf(filename, spg, epg):
    reader = PdfReader(filename)
    
    # store the previous page (questions can go off the page)
    ppage = ""
    num_list = []
    start = 1

    
    for i in range(spg, epg + 1, 1):
        page = reader.pages[i]
        ppage = ppage + "$" + page.extract_text()
        ppgage = ppage.replace("$", "")
        
        # finds number of questions on page
        num_p_page = find_num_questions(ppage, start)
        num_list.extend(num_p_page)
        end = num_p_page[-1]
        # loops through each question
        for n in range(start, end + 1, 1):
            # answers at the top of the page
            if old := find_choices(ppage, num_p_page): 
                if n == num_list[n - 1]:
                    find_answers(ppage, old)

            find_question(ppage, n) # -> stores questions into df
            find_answers(ppage, n) # -> stores choices into df

            
        # split to continue to next problem
        first, second = ppage.split("$")
        ppage = second
        start = end + 1

def find_question(txt, num):
    ntxt = break_text(txt, num)
    
    # # break question, answer choices
    # # sometimes answers on the next page
    try:
        problem = ntxt.split("\n(A) ")
    except ValueError:
        pass
    df.loc[num, "question"] = problem[0]
    # df._append({"question": problem[0], "choices": None, "answer": None}, ignore_index=True)
    return 

# find all the answer choices
def find_answers(txt, num):
    ntxt = break_text(txt, num)
    
    try:
        problem = ntxt.split("\n(A) ")
        choices_dict = split_choices("(A) " + problem[1])
        df.at[num, "choices"] = [choices_dict]
    except (ValueError, IndexError) as _:
        pass
    
    return 
# find if choices is at the top of page
def find_choices(txt, list_questions): 
    n_questions = len(list_questions)
    
    n_choices = len(re.findall(r"(\n\(A\) )", txt))
    if n_questions < n_choices:
        return list_questions[n_questions - 1]
    return None
    
                        
def search_string(current_char, schar, string, n):
    if current_char == str(schar) and len(string) == n:
        return string + current_char
    return ""

def break_text(txt, qn):
    before, broken_text = txt.split(f"\n{qn}. ")

    try:
        broken_text, second_text = broken_text.split(f"\n{qn + 1}. ")
        return broken_text
    except ValueError:
        return broken_text

# splits it by " )" -> shoots an error if there is an exception
def split_choices(choices):
    multiple_choice = {}
    choice = choices.split("\n")
    
    for i in range(len(choice)):
        letter, atext = choice[i].split(") ")

        try:
            letter = letter.replace("(", "")

            if letter.isalpha and len(letter) == 1:
                multiple_choice[letter] = atext
        except ValueError:
            raise Exception("Multiple Choice split with a wrong value")
    
    return multiple_choice

def find_num_questions(txt, start):
    question_num = []
    while True:
        if f"\n{start}. " in txt:
            question_num.append(start)
        else:
            return question_num
        start += 1

if __name__ == "__main__":
    main()