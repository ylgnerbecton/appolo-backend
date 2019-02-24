# importing required modules 
import PyPDF2 

# def read_pdf(doc):
#     # creating a pdf file object 
#     pdfFileObj = open(doc, 'rb') 

#     # creating a pdf reader object 
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

#     # printing number of pages in pdf file 
#     print(pdfReader.numPages) 

#     # creating a page object 
#     pageObj = pdfReader.getPage(0) 

#     # extracting text from page 
#     strig_pdf = pageObj.extractText()
#     pdfFileObj.close() 
#     return strig_pdf
def read_pdf(doc):
    pdfFileObject = open(doc, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    string = ''
    for i in range(count):
        page = pdfReader.getPage(i)
        string = string+page.extractText()
    return string
