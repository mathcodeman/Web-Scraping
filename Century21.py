
import requests
from bs4 import BeautifulSoup
import pandas
#r = requests.get("https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

r=requests.get("https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=0.html")
c = r.content
soup=BeautifulSoup(c,"html.parser")
page_nb=soup.find_all("a",{"class":"Page"})[-1].text


MLS=[]
for page in range(0,int(page_nb)*10,10):
    base_url=f"https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s={page}.html"
    print(base_url)
    r=requests.get(base_url)
    c = r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})

    
    for i in range(len(all)):
        d={}
        price=all[i].find("h4",{"class":"propPrice"}).text.replace("\n"," ").replace(" ","")
        address=all[i].find("div",{"class":"primaryDetails"}).text.replace("\n"," ").strip(" ")
        d["Price"]=price
        d["Address"]=address
        try:
            beds=all[i].find("span",{"class":"infoBed"}).find("b").text

            d["Beds"]=beds
        except:

            d["Beds"]=None
        try:
            Sqft=all[i].find("span",{"class":"infoSqFt"}).find("b").text

            d["Sqft"]=Sqft
        except:

            d["Sqft"]=None
        try:
            baths=all[i].find("span",{"class":"infoValueFullBath"}).find("b").text

            d["Baths"]=baths
        except:

            d["Baths"]=None
        try:
            hbaths=all[i].find("span",{"class":"infoValueHalfBath"}).find("b").text

            d["Hbaths"]=hbaths
        except:

            d["Hbaths"]=None

        for col_group in all[i].find_all("div",{"class":"columnGroup"}):
            for features,names in zip(col_group.find_all("span",{"class":"featureGroup"}),col_group.find_all("span",{"class":"featureName"})):
                #print(features.text,names.text)
                if "Lot Size" in features.text:
                    d["LotSize"]=names.text
        MLS.append(d)


df=pandas.DataFrame(MLS)
print(df)
