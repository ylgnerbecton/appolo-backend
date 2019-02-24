# importing required modules 
import PyPDF2 

def read_pdf(filename):
    # creating a pdf file object 
    pdfFileObj = open(filename, 'rb') 

    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

    # printing number of pages in pdf file 
    print(pdfReader.numPages) 

    # creating a page object 
    pageObj = pdfReader.getPage(0) 

    # extracting text from page 
    strig_pdf = pageObj.extractText()
    pdfFileObj.close() 
    return string_pdf

