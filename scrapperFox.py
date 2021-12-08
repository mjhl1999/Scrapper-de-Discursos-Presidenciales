from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import os
import re

# my_file_handle=open("Fox_links_2008.txt","r")
# file = my_file_handle.read()
#
# soup = bs(file, "html.parser")
#
# links = []
#
#
# def get_links():
#     pages = str(soup.find("div", {"id": "chart"}))
#     while (len(pages) > 20):
#         init = pages.find('https:')
#         pages = pages[init:]
#         fin = pages.find('><path')
#         link = pages[:fin]
#         #print(link)
#         links.append(link)
#         link = []
#         pages = pages[init+fin:]
#
# get_links()
# print(links)



def get_pags():
    pags = []
    for link in links:
        if 'contenido=' in link:
            pags.append(link)
    return pags


def make_txts():
    counter = 0
    for pag in pags:
        try:
            print(counter)
            print(pag)
            counter = counter+1
            #create .txt file
            save_path = 'Fox2017'
            file_name = str(get_date(pag))+" - "+get_title(pag)+".txt"
            completeName = os.path.join(save_path, file_name)
            f= open(completeName,"w+")
            f.write(get_body(pag))
            f.close()
            print(file_name)
        except:
           pass

def get_date(pag):
    page = requests.get(pag)
    soup = bs(page.content, "html.parser")
    date = soup.find("p", {"class": "presidencia_actividades_fecha2"}).text.replace(" de","")
    YY = date.split()[-1]
    MM = monthToNum(date.split()[2])
    DD = date.split()[1]
    if (int(DD)<10):
        DD = "0" + str(int(DD))
    return YY + MM + DD

def monthToNum(month):
    return {
            'Enero' : "01",
            'Febrero' : "02",
            'Marzo' : "03",
            'Abril' : "04",
            'Mayo' : "05",
            'Junio' : "06",
            'Julio' : "07",
            'Agosto' : "08",
            'Septiembre' : "09",
            'Octubre' : "10",
            'Noviembre' : "11",
            'Diciembre' : "12"
    }[month]

def get_title(pag):
    page = requests.get(pag)
    soup = bs(page.content, "html.parser")
    title = soup.find("p", {"class": "presidencia_actividades_titulo2"}).text.replace('\n', ' ').replace('\r', ' ').replace('INICIO','').replace('Actividades','').replace('Orden y Respeto', '').replace('Buen Gobierno', '')
    title = re.sub('\W+',' ', title )
    return title

def get_body(pag):
    page = requests.get(pag)
    soup = bs(page.content, "html.parser")
    body = soup.find("p", {"class": "presidencia_actividades_cuerpo"}).text
    body = re.sub('\W+',' ', body)
    return body


my_file_handle=open("fox_links_2008.txt","r")
file = my_file_handle.read()

links = file.split();

pags = get_pags()

print(len(pags))

make_txts()
