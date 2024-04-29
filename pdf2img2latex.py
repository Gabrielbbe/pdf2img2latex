'''
read me
 Running pix2text is computationally expensive, it is a good idea to
run it in a colab notebook, while doing it you may need to change the paths inside this code
so it can properly match the path of the pdf2image files properly inside google colab
'''
from pdf2image import convert_from_path, convert_from_bytes
import os 
import time
import cv2
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
import pickle
import os
import re
import copy 


def pdf2img(list_pdf):

    pdf_f = 0

    for path_df in list_pdf:
        
        os.mkdir(f'{os.getcwd()}/pdf2image_{pdf_f}')
        images = convert_from_path( path_df )

        i = 0
        for page in images:
            page.save(f'{os.getcwd()}/pdf2image_{pdf_f}/{i}.png')
            i = i + 1
        
        pdf_f = pdf_f + 1


def crop_image_by_half(image, left, top, right, bottom): # isso conta a img
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image


def img2texts(list_pdff_imgs):
    
    pages_outs = {}
    tempos = []

    for art in list_pdff_imgs:

        for i in range(len(os.listdir(f'{os.getcwd()}/{art}'))):

            image = cv2.imread(f'{os.getcwd()}/{art}/{i}.png')
            image = Image.fromarray(image)
            width, height = image.size
            blocos = height/3

            lts = []

            for j in range(3):

                bottom = (j+1)*blocos
                top = bottom-blocos
                cimg = crop_image_by_half(image, 0, top, width, bottom)
                p2t = Pix2Text()

                start_time = time.time()
                outs = p2t.recognize(cimg, resized_shape=608, return_text=True)  # You can also use `p2t(img_fp)` to get the same result
                tiempo = str(time.time() - start_time)
                tiempo = tiempo.encode('utf-8')
                tempos.append(tiempo)
                lts.append(outs)
                pages_outs[f'page{i}'] = lts

    pages_outs['title_authors'] = pages_outs['page0']

    with open(f'{os.getcwd()}/{art}/page_outs', 'wb') as fp:
        pickle.dump(pages_outs, fp)

def extract_text_between_symbols(texts, symbol='$'):

    matches = []

    for text in texts:

        pattern = re.compile(rf'{re.escape(symbol)}(.*)\{re.escape(symbol)}', re.DOTALL)
        #print(str(text))
        match = re.findall(pattern, str(text))
        matches.append(match)

    return matches

def detect_string(input_string, string_list):

    for s in string_list:

        if s in input_string:
            return True
        
    return False

def extract_text_in_symbols(input_string):
    return re.findall(r'\$ (.*?) \$', input_string)

def texts2latex(path_pages_texts):

    with open(path_pages_texts, 'rb') as f:
        pdf_teste = pickle.load(f)

    # Ler pagina por pagina extrair o codigo regex e e criar uma chave pagina_number_latex
    # 
    chaves_originais = list( pdf_teste.keys() )
    arit_op = ['=', '+', '-', '\\', '{', '}']

    for page in chaves_originais:

        latex_strings = []
        strings = pdf_teste[str(page)][0].split('$')

        for s in strings:

            if detect_string( s, arit_op ) == True:
                latex_strings.append(s)
            
            else:
                continue

        pdf_teste[f'{str(page)}_latex'] = latex_strings

    with open(f'{os.getcwd()}/dict_w_latex.pickle', 'wb') as file:
        pickle.dump(pdf_teste, file)
