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
        print(q)
        # df.loc[len(df)] = get_ChatGPT_rewording(q)
        chatgpt_df = pd.concat([chatgpt_df, pd.DataFrame([get_ChatGPT_rewording(q)])], ignore_index=True)
        break

    return chatgpt_df

def get_ChatGPT_rewording(question):
    print("RUN")
    # create a client to access model
    client = OpenAI(api_key=OPENAI_API_KEY)
                
    # create a conversation
    # https://chatgpt.com/share/6768fd9f-a84c-8010-8510-549990049789/
    completion = client.chat.completions.create(
        # cheaper model for testing: gpt-4o-mini
        # real model for testing: gpt-4o
        model="gpt-4o-mini",
        messages=[
            # Reading levels used by the National Assessment of Adult Literacy to assess English language literacy skils
            # https://nces.ed.gov/naal/perf_levels.asp
            {
                "role": "developer", 
                "content": "Your task as a National Assessment of Adult Literacy (NAAL) Question Converter is to transform a given question into four distinct versions, each aligning with one of NAAL's four proficiency levels (Below Basic, Basic, Intermediate, Proficient). For each version: 1. Preserve the original meaning of the question, retaining all numbers and important words. 2. Ensure the phrasing is clear and suitable for the target literacy level. 3. Use diverse and inclusive language to accommodate varied interpretations and challenge literacy skills appropriately. Your goal is to produce diverse versions that maintain the integrity of the original question while adapting complexity and style for each level."
            },
            {
                "role": "user",
                "content": f"""
                1. Generate four rephrased versions of the question, tailored to each proficiency level (Below Basic, Basic, Intermediate, Proficient). 
                2. Ensure the question's meaning and key elements (numbers, critical terms) are preserved across all versions. 
                3. Maintain comprehensibility for the target literacy level while using inclusive and varied phrasing. 
                
                Transform this question: {question}
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
                            "description": "Reworded question for Proficient level"
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