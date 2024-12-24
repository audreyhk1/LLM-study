import pandas as pd
from openai import OpenAI
import json
from SECRET_KEYS.secret import OPENAI_API_KEY
NAAL_LEVELS = ["Below Basic", "Basic", "Intermediate", "Advanced"]

def main():
    # get all medical questions
    qdf = pd.read_csv("data/qdf.csv")
    
    # get all language translations 
    
    # get all ChatGPT rewordings 
    rewordings_df = get_all_ChatGPT_rewordings(qdf)
    
    # save a csv of new rewordings
    rewordings_df.to_csv("chatgpt-rewordings/second-rewordings.csv")
    
    # calculate rouge-1 score 

def get_all_ChatGPT_rewordings(df):
    global NAAL_LEVELS
    chatgpt_df = pd.DataFrame(columns=NAAL_LEVELS)
    
    for q in df["question"]:
        df.loc[len(df)] = get_ChatGPT_rewording(q)

    return chatgpt_df

def get_ChatGPT_rewording(question):
    # create a client to access model
    client = OpenAI(api_key=OPENAI_API_KEY)
                
    # create a conversation
    # https://chatgpt.com/share/6768fd9f-a84c-8010-8510-549990049789/
    completion = client.chat.completions.create(
        model="gpt-3",
        messages=[
            # Reading levels used by the National Assessment of Adult Literacy to assess English language literacy skils
            # https://nces.ed.gov/naal/perf_levels.asp
            {
                "role": "National Assessment of Adult Literacy Question Converter", 
                "content": "Your task is to transform a given question into four diverse phrasings, each designed to align with one of NAAL's four proficiency levels (Below Basic, Basic, Intermediate, Proficient). Focus on creating varied and inclusive wording that ensures comprehensive assessment across all levels. Each version must challenge the expected literacy skills while remaining clear and understandable for the target level. Emphasize diverse phrasing to capture nuanced interpretations."
            },
            {
                "role": "user",
                "content": f"""
                1. Generate four diverse phrasings of the question, each targeting the chosen level. (Below Basic, Basic, Intermediate, Proficient)
                2. Use diverse and inclusive wording to evaluate varied literacy interpretations.
                3. Be comprehensible while challenging literacy skills appropriate for the target level.
                4. Return the response as a Python dictionary.
                
                Transform this question: {question}
                
                Output format: 
                {{
                    'Below Basic': 'Reworded question for Below Basic level', 
                    'Basic': 'Reworded question for Basic level', 
                    "Intermediate": 'Reworded question for Intermediate level', 
                    "Proficient": "Reworded question for Proficient level"
                }}
                """
            }
        ]
    )
    res = json.loads(completion.choices[0].message)
    return str(res)
    

    
if __name__ == "__main__":
    main()