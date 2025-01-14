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
    counter = 1
    
    for q in df["question"]:
        print(f"{counter} out of 95 questions completed")
        chatgpt_df = pd.concat([chatgpt_df, pd.DataFrame([get_ChatGPT_rewording(q)])], ignore_index=True)
        counter += 1;

    return chatgpt_df

def get_ChatGPT_rewording(question):
    # create a client to access model
    client = OpenAI(api_key=OPENAI_API_KEY)
                
    # create a conversation
    # https://chatgpt.com/share/6768fd9f-a84c-8010-8510-549990049789/
    completion = client.chat.completions.create(
        # cheaper model for testing: gpt-4o-mini
        # real model for testing: gpt-4o
        model="gpt-4o",
        messages=[
            # Reading levels used by the National Assessment of Adult Literacy to assess English language literacy skils
            # https://nces.ed.gov/naal/perf_levels.asp
            {
                "role": "developer", 
                "content": """
                Your task as a National Assessment of Adult Literacy (NAAL) Question Converter is to transform a given question into four distinct versions, each aligning with one of NAAL's four proficiency levels (Below Basic, Basic, Intermediate, Advanced). 
                
                For each version: 
                1. Fully preserve the original meaning of the question. This includes retaining **all numbers, critical words, and key phrases** from the original question without omission or simplification. 
                2. Adapt minor, stylistic elements such as sentence structure or connective words to align with the literacy level's complexity.
                3. Ensure each rephrased version remains clear and faithful to the original context while testing literacy skills suitable for its target level. 
                4. Avoid introducing new information, changing the meaning, or omitting any part of the question that conveys vital details or context.
                """
            },
            {
                "role": "user",
                "content": f"""
                1. Generate four rephrased versions of the question, tailored to each proficiency level (Below Basic, Basic, Intermediate, Proficient). 
                2. Retain **all numbers, critical terms, and key phrases** from the original question without any changes, omissions, or substitutions. 
                3. Adjust only minor wording or sentence structure to make the question suitable for the target literacy level. 
                4. Ensure every version accurately reflects the original question’s meaning and includes all relevant details. 
                
                Transform this question: '''{question}'''
                """
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "openai_rewording_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "Below Basic": {
                            "description": "Reworded question for Below Basic level" 
                        },
                        "Basic": {
                            "description": "Reworded question for Basic level"
                        },
                        "Intermediate": {
                            "description": "Reworded question for Intermediate level"
                        },
                        "Advanced": {
                            "description": "Reworded question for Advanced level"
                        }
                    }
                }
            }
        }
    )
    # convert json to dictionary (function returns a dictioanry)
    return json.loads(completion.choices[0].message.content)
    
    

    
if __name__ == "__main__":
    main()