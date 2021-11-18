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
    date = soup.findAll('dd')[1].text.replace(" de","")
    YY = date[-2:]
    MM = date[3:]
    MM = MM[:-5]
    MM = monthToNum(MM)
    DD = date[:2]
    return str(YY)+MM+str(DD)

def monthToNum(month):

    return {
            'enero' : "01",
            'febrero' : "02",
            'marzo' : "03",
            'abril' : "04",
            'mayo' : "05",
            'junio' : "06",
            'julio' : "07",
            'agosto' : "08",
            'septiembre' : "09",
            'octubre' : "10",
            'noviembre' : "11",
            'diciembre' : "12"
    }[month]


def get_title():
    return (soup.findAll('h1')[0].text + ".txt").replace("/","")

def get_category():
    return (soup.findAll('dd')[2].text)

def get_body():
    html = page.text
    tags = soup.findAll('p') #gets the page body

    ps = len(tags) #number of <p>'s in html
    res = ""

    for i in range(ps-6):
        for b in body:
            sub = b.find_all('p')
        res = res + sub[i].text + "\n"

    #print(res) #body page
    return res


linkPart1 = "https://www.gob.mx/epn/es/archivo/prensa?idiom=es&order=DESC&page="

links = []

#gets all links from all pages
for i in range(460, 567):
    http = linkPart1 + str(i)
    if(get_links(http) != None):
        links.append(get_links(http))

#print(links) #all links from all the speeches

#Geting data from links
for link in links:
    url = "https://www.gob.mx/" + str(link)
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    body = soup.find_all('div', "article-body")
    #print(body) #full page

    #create .txt file
    save_path = 'EPN2'
    file_name = str(get_date())+" - "+get_category()+" - "+get_title()
    completeName = os.path.join(save_path, file_name)
    f= open(completeName,"w+")
    f.write(get_body())
    f.close()
