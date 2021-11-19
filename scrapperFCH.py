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
            if link['href'].startswith('https://web.archive.org/web/201'):
                l = link['href']
                links.append(str(l))


def get_date():
    date = soup.find("div", {"class": "fecha"}).text.replace(" de","")
    #date = soup.find("div", {"id": "pres_fecha"}).text.replace(" de","")
    #date = soup.find("p", {"class": "presidencia_articulos_fecha"}).text.replace(" de","")
    #date = soup.find("div", {"class": "Fecha_listado"}).text

    YY = url[28:][:4]
    MM = date.split()[1]
    # MM = date.split()[2]
    MM = monthToNum2(MM)
    DD = date.split()[0]
    #DD = date.split()[1]
    if (int(DD)<10):
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

def monthToNum2(month):

    return {
            'ene' : "01",
            'feb' : "02",
            'mar' : "03",
            'abr' : "04",
            'may' : "05",
            'jun' : "06",
            'jul' : "07",
            'ago' : "08",
            'sep' : "09",
            'oct' : "10",
            'nov' : "11",
            'dic' : "12"
    }[month]


def get_title():
    title = soup.find("h2").text
    #title = soup.find("div", {"id": "pres_titulo"}).text
    #title = soup.find("p", {"class": "presidencia_subseccion"}).text
    return title

def get_body():
    body = soup.find("div", {"id": "nota_interna_contenido_sencillo"}).text
    #body = soup.find("div", {"id": "presidencia_contenidos_cuerpo"}).text
    #body = soup.find("div", {"class": "presidencia_contenidos_cuerpo"}).text
    body = body.replace('\xa0', '')  #remove \xa0 lines
    body = os.linesep.join([s for s in body.splitlines() if s])  #remove blank lines
    return body


url = "https://web.archive.org/web/20121013015154/http://www.presidencia.gob.mx/2012/10/diversas-intervenciones-durante-el-primer-aniversario-de-la-procuraduria-social-de-atencion-a-las-victimas-de-delitos/"

#https://web.archive.org/web/20121011085836/http://www.presidencia.gob.mx:80/prensa/discursos
linkPart = "https://web.archive.org/web/20121009195323/http://www.presidencia.gob.mx/prensa/discursos/page/"

links = []

#gets all links from all pages
for i in range(2, 10):
    http = "linkPart + str(i) + "/""
    if(get_links(http) != None):
        links.append(get_links(http))

#print(len(links)) #all links from all the speeches

for link in links:
    page = requests.get(link)
    soup = bs(page.content, "html.parser")
    try:
        #create .txt file
        save_path = 'FCH'
        file_name = str(get_date())+" - "+get_title()+".txt"
        completeName = os.path.join(save_path, file_name)
        f= open(completeName,"w+")
        f.write(get_body())
        f.close()
    except:
        pass
