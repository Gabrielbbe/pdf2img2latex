from pdf2image import convert_from_path, convert_from_bytes
import os 

inputs = input("Insert the path to the pdf file : ")
inputs = inputs.split()
list_df = inputs
# list_df = ['pdf2.pdf', 'pdf3.pdf', 'pdf4.pdf']
pdf_f = 0

for path_df in list_df:
    
    os.mkdir(f'{os.getcwd()}/pdf2image_{pdf_f}')
    images = convert_from_path( path_df )

    i = 0
    for page in images:
        page.save(f'{os.getcwd()}/pdf2image_{pdf_f}/{i}.png')
        i = i + 1
    
    pdf_f = pdf_f + 1

