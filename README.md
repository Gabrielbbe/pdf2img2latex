Pipeline that uses Python scripts to transform pdf to images and images to English text and latex code.

Made with the intention to extract latex code from scientific articles, there's a lot to improve in these scripts.

Running the script pdfimg2texts.py is computationally expensive because it uses OCR models, I recommend running it in a google colab notebook.

first download your pdf file then run

```
python pdf2img.py
```

It will ask the path to your pdf file, then it will put the pdf to image in a folder in the directory where you left the pdf2image.py file

```
python pdfimg2texts.py
```

Put the path to the folder containing the images of the pdf (this part takes time according to the size of the pdf ) 

```
python pdf2img2latex.py
```

Provide the path to the folder containing the images of the pdf
In the folder containing the images of the pdf it will create a pickle file containing a dict with the text the models were able to detect per page.
