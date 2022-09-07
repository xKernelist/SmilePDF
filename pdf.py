from pathlib import Path
from PyPDF2 import PdfFileReader,PdfFileWriter
import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from zipfile import ZipFile

def downloadAll(url):
    folder_location = r'C:\Users\sefa\Desktop\workspace\smilePDFweb\static\downloadAll'
    if not os.path.exists(folder_location):os.mkdir(folder_location)
    
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser") 
    x=1
    for link in soup.select("a[href$='.pdf']"):
        #filename = os.path.join(folder_location,link['href'].split('/')[-1])
        filename = os.path.join(folder_location,str(x)+".pdf")
        x+=1

        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin(url,link['href'])).content)

    zipobj = ZipFile(f"./static/downloadAll/0.zip","w")
    for i in range(len(os.listdir("./static/downloadAll"))):
        if i == len(os.listdir("./static/downloadAll"))-1:
            break
        else:
            zipobj.write(f"./static/downloadAll/{i+1}.pdf")
        
    # for i in dosya
    #zipobj.write(f"./static/{directory}/first_page.pdf")
    #zipobj.write(f"./static/{directory}/second_page.pdf")
    zipobj.close()
    

def pdf_printer(pdf,directory):

    pdf = PdfFileReader(pdf)

    pdfwriter2pages = []
    pdfwriter1 = PdfFileWriter()

    pdfwriter2 = PdfFileWriter()

    for i in range(int(pdf.getNumPages())):
        if i %2==0:
            pdfwriter2pages.append(pdf.getPage(i))
        else:
            pdfwriter1.addPage(pdf.getPage(i))

    pdfwriter2pages = pdfwriter2pages[::-1]
    for i in pdfwriter2pages:
        pdfwriter2.addPage(i)
        
    directory = directory
    #klasör varsa alttaki kodu çalıştırma
    if not os.path.exists(f"./static/{directory}"):
        os.mkdir(f"./static/{directory}")
    with Path(f"./static/{directory}/first_page.pdf").open(mode="wb") as output_file:
        pdfwriter2.write(output_file)

    with Path(f"./static/{directory}/second_page.pdf").open(mode="wb") as output_file:
        pdfwriter1.write(output_file)

    zipobj = ZipFile(f"./static/{directory}/0.zip","w")
    zipobj.write(f"./static/{directory}/first_page.pdf")
    zipobj.write(f"./static/{directory}/second_page.pdf")
    zipobj.close()