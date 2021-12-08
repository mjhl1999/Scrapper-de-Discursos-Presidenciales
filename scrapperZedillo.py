from bs4 import BeautifulSoup as bs, SoupStrainer
import requests
import os
import json

def get_links(link):

    local_links = []

    hrefs = soup.findAll('a')
    for h in hrefs:
        if h.has_attr('href'):
            l = h['href']
            local_links.append(str(l))

    links_temp = []
    temp = ""

    pos = link.find('disc')+5
    link_temp = link[:pos]

    for l in local_links:
        temp = link_temp + str(l)
        if (temp.endswith("html")):
            links_temp.append(temp)

    return links_temp


def get_date():
    date = soup.find("b").text.replace("año","")
    YY = date.split()[-1].replace(".","")
    MM = monthToNum(date.split()[-3])
    DD = date.split()[-5]
    if (int(DD)<10):
        DD = "0" + str(int(DD))
    return YY + MM + DD

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
    title = soup.findAll("b")[1].text.replace('\n', ' ').replace('\r', ' ')
    while (title[-1] == "." or title[-1] == " "):
         title = title[:-1]
    if title.startswith("Versi"):
        if "presidente" in title:
            pos = title.find("presidente")+11
            title = title[pos:]
    return title[:230]

def get_body():
    body = soup.findAll("p")[2:]
    body_temp = ""
    for b in body:
        body_temp = body_temp + b.text
    return body_temp.replace("-oooooo-", "")


my_file_handle=open("calendar_grid_Zedillo.txt","r")
file = my_file_handle.read()

calendar_links = file.split();

json.dumps(calendar_links)

print(calendar_links)

links = []

for cal_link in calendar_links:
    link = cal_link
    page = requests.get(link)
    soup = bs(page.content, "html5lib")
    links += get_links(link)

print(links)

counter = 0
len = len(links)

for link in links:
    print(str(counter) + " " + str(len))
    page = requests.get(link)
    soup = bs(page.content, "html.parser")
    counter = counter+1
    try:
        print(link)
        #create .txt file
        save_path = 'Zedillo'
        file_name = get_date()+" - "+get_title()+".txt"
        completeName = os.path.join(save_path, file_name)
        f= open(completeName,"w+")
        f.write(get_body())
        f.close()
        print(file_name)
    except:
       pass
