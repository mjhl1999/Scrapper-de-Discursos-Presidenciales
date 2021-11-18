from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import httplib2
from datetime import datetime
import os


def get_links(link):
    http = httplib2.Http()
    status, response = http.request(link)

    for link in bs(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            if link['href'].startswith('/epn/prensa/'):
                l = link['href']
                links.append(str(l))


def get_date():
    date = soup.findAll('p')[4].text.replace(" de","")
    #soup.findAll('p')[4].text
    YY = url[28:][:4]
    MM = date.split()[2]
    MM = monthToNum(MM)
    DD = date.split()[1]
    if (int(DD)<9):
        DD = "0" + str(DD)
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


def get_title():
    return (soup.findAll('p')[3].text).replace("/","")

def get_category():
    return (soup.findAll('dd')[2].text)

def get_body():
    return soup.findAll('div')[16].text


url = "https://web.archive.org/web/20070213004358/http://www.presidencia.gob.mx/prensa/discursos/?contenido=28314"
page = requests.get(url)
soup = bs(page.content, "html.parser")
body = soup.findAll('div')[16].text
print(get_date()) #full page

#create .txt file
save_path = 'FCH'
file_name = str(get_date())+" - "+get_title()
completeName = os.path.join(save_path, file_name)
f= open(completeName,"w+")
f.write(get_body())
f.close()
