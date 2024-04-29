'''
read me
 Running pix2text is computationally expensive, it is a good idea to
run it in a colab notebook, while doing it you may need to change the paths inside this code
so it can properly match the path of the pdf2image files properly inside google colab
'''

import time
import cv2
from PIL import Image
from pix2text import Pix2Text, merge_line_texts
import pickle
import os

def crop_image_by_half(image, left, top, right, bottom): # isso conta a img
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

tempos = []
pages_outs = {}
inputs = input("Insert the path to pdf2image_pdfname files : ")
inputs = inputs.split()
pdfs = inputs
# pdfs = ['pdf0', 'pdf1', 'pdf2']

for art in pdfs:

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
        pages_outs[f'pagina{i}'] = lts


  with open(f'{os.getcwd()}/{art}/page_outs', 'wb') as fp:
    pickle.dump(pages_outs, fp)

