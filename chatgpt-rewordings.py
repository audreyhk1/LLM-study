import pandas as pd
from openai import OpenAI

# Reading levels used by the National Assessment of Adult Literacy to assess English language literacy skils
# https://nces.ed.gov/naal/perf_levels.asp
# level (key): Key abilities associated with level (value)
READING_LEVELS = {
    "Below Basic": 
        """
        - locating easily identifiable information in short, commonplace prose texts
        - locating easily identifiable information and following written instructions in simple documents (e.g., charts or forms)
        - locating numbers and using them to perform simple quantitative operations (primarily addition) when the mathematical information is very concrete and familiar
        """, 
    "Basic": 
        """
        - reading and understanding information in short, commonplace prose texts
        - reading and understanding information in simple documents
        - locating easily identifiable quantitative information and using it to solve simple, one-step problems when the arithmetic operation is specified or easily inferred
        """, 
    "Intermediate":
        """
        - reading and understanding moderately dense, less commonplace prose texts as well as summarizing, making simple inferences, determining cause and effect, and recognizing the author’s purpose
        - locating information in dense, complex documents and making simple inferences about the information
        - locating less familiar quantitative information and using it to solve problems when the arithmetic operation is not specified or easily inferred
        """, 
    "Advanced":
        """
        - reading lengthy, complex, abstract prose texts as well as synthesizing information and making complex inferences
        - integrating, synthesizing, and analyzing multiple pieces of information located in complex documents
        - locating more abstract quantitative information and using it to solve multistep problems when the arithmetic operations are not easily inferred and the problems are more complex
        """}


def main():
    # get all medical questions
    qdf = pd.read_csv("data/qdf.csv")
    
    # get all language translations 
    
    # get ChatGPT rewordings 

def get_ChatGPT_rewordings(question, rlevel, description):
    # create a client to access model
    client = OpenAI()
    
    # create a conversation
    # https://chatgpt.com/share/6768fd9f-a84c-8010-8510-549990049789/
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "National Assessment of Adult Literacy Question Converter", 
         "content": "Your task is to transform a given question into four diverse phrasings, each designed to align with one of NAAL's four proficiency levels (Below Basic, Basic, Intermediate, Proficient). Focus on creating varied and inclusive wording that ensures comprehensive assessment across all levels. Each version must challenge the expected literacy skills while remaining clear and understandable for the target level. Emphasize diverse phrasing to capture nuanced interpretations."
        },
        {
            "role": "user",
            "content": f"""
            1. Generate four diverse phrasings of the question, each targeting the chosen level. (Below Basic, Basic, Intermediate, Proficient)
            2. Use diverse and inclusive wording to evaluate varied literacy interpretations.
            3. Be comprehensible while challenging literacy skills appropriate for the target level.
            Transform this question: {question}
            """
        }
    ]
)
    

    
if __name__ == "__main__":
    main()