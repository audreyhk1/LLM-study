import pandas as pd
# from get_translations.translate_libraries.final_translate import lang_translation
from get_translations.translate_libraries import get_translation
from openpyxl.workbook import Workbook
from global_variables import get_languages

global LANGUAGES
LANGUAGES = get_languages()

def main():
    global LANGUAGES
    
    print(len(LANGUAGES))
def stop():
    global LANGUAGES
    
    qdf = pd.read_csv("data/qdf.csv")
    # selects only the questions where "questions" is a series
    questions = qdf["question"]
    
    # create a translated quetion dataframe (seperate from the qdf but linked through the index)
    translated_qdf = pd.DataFrame(columns=LANGUAGES)
    
    # for question 
    for index, value in questions.items():
        translated_qdf = translated_qdf._append(retrieve_10_translations(number=index, text=value, languages=LANGUAGES[1:]), ignore_index=True)

    translated_qdf.to_csv("get_translations/new_question_translations.csv")
    

def retrieve_10_translations(number: int, text: str, languages):
    # a dictionary of all the translations
    temp = {}
    temp["en"] = text
    
    for lan in languages:
        temp[lan] = get_translation(question=text, lan=lan)
        print(f"Question {number} -- {lan} DONE ✅")
    
    return temp


if __name__ == "__main__":
    main()