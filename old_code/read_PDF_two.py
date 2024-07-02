from pypdf import PdfReader
import sys

def main():
    open_PDF("data/Step_1_Sample_Items (1).pdf",  8, 8)
    
def open_PDF(filename, start, end):
    pdf = []
    num_list = []
    start_bookmark = 1
    reader = PdfReader(filename)
    
    # open pdf file -> txt file
    for i in range(start, end + 1, 1):
        page = reader.pages[i]
        ppage = page.extract_text() # -> temp variable stores 
        print(ppage)
        
        # txt.split -> list (with indexes = problem)
        
        # num_p_page = find_num_questions(ppage, start_bookmark)
        # num_list.extend(num_p_page)
        # end_bookmark = num_p_page[-1]
        
        # for n in range(start_bookmark, end_bookmark + 1, 1):
        #     pdf.append(ppage.extract_text())
        
        # start_bookmark = end_bookmark + 1
            
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