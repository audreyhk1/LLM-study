import pandas as pf
from pypdf import PdfReader
import sys

def main():
    DATA = "data/Step_1_Sample_Items (1).pdf"
    TXT = "data/questions.txt"
    # pg 8 to 52
    
    pdf_to_txt(8, 52, filename=DATA, txt=TXT)

def pdf_to_txt(*pages: int, filename, txt):
    """
    Opens a PDF and reads it page by page
    Write string on text file
    """
    reader = PdfReader(filename)
    
    with open(txt, "w") as file:
        for i in range(*pages):
            print("hi")
            print(reader.pages[i].extract_text())
            file.write(str(reader.pages[i].extract_text()))
        
    
if __name__ == "__main__":
    main()