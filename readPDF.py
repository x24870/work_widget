import PyPDF2


FILE_NAME = 'CLCL-N_R100_20181127.pdf'

with open(FILE_NAME, 'rb') as pdf1:
    pdfReader = PyPDF2.PdfFileReader(pdf1)
    info = pdfReader.getDocumentInfo()
    print(info)
