import requests
import json
from bs4 import BeautifulSoup #HTML sayfasını parse etmek için gereken kütüphane
from time import sleep 

offset = 1 # URL'de offset parametresi sayfanın başında hangi makalenin yer alacağını belirler. Örneğin offset 41 olduğu zaman sayfada 41-60 arası makaleler listelenir.
pubyear = 2019
scopus_1 = "https://www.scopus.com/results/results.uri?sort=cp-f&src=s&st1=%22human-computer+interaction%22&nlo=&nlr=&nls=&sid=f65b0436cf4718bd9b60238fd65a4454&sot=b&sdt=b&sl=78&s=TITLE-ABS-KEY%28%22human-computer+interaction%22%29+AND+DOCTYPE%28ar%29+AND+PUBYEAR+%3d+"
scopus_2 = "&cl=t&offset="
scopus_3 = "&origin=resultslist&ss=cp-f&ws=r-f&ps=r-f&cs=r-f&cc=10&txGid=7575ff4e603f1469d35288c9add1ab14"
articles = {}
#totalArticleCount = 100


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

for k in range(25): #Range * 20 = Elde edilecek makale sayısı. Her sayfada 20 makale yer almakta
    myURL = scopus_1 + str(pubyear) + scopus_2 + str(offset) + scopus_3
    r = requests.post(url=myURL, headers=hdr)
    parsedPage = BeautifulSoup(r.text, "lxml")
    searchAreas = parsedPage.find_all("tr", attrs={"class":"searchArea"})
    print(len(searchAreas))
    for i in range(len(searchAreas)):
        #Her makalenin belirli bazı verileri elde edilir
        searchArea = searchAreas[i].find("a", attrs={"class":"ddmDocTitle"})
        docTitle = searchArea.get_text()
        docLink = searchArea.attrs["href"]
        citations = searchAreas[i].find_all("td", attrs={"class":"textRight"})[1].get_text()
        keywords = []

        
        print(str(offset+i) + ".ci makalenin sayfasından etiketler çekiliyor")

        #Makalenin anahtar kelimelerini elde etmek için makalenin sayfasına gidilir
        try:
            r2 = requests.post(url=docLink, headers=hdr)
            parsedArticle = BeautifulSoup(r2.text, "lxml")
            #print("parsedArticle BeautifulSoup nesnesi oluşturuldu")
            authorKeywords = parsedArticle.find("section", attrs={"id":"authorKeywords"})
            #print("Keyword'lerin yer aldığı section elde edildi")
            badges = authorKeywords.find_all("span", attrs={"class":"badges"})
            #print("Bütün badge'ler bulundu")
            keywords = []
            for j in range(len(badges)):
                keywords.append(badges[j].get_text())
            print(str(offset+i) +".ci makalenin bütün anahtarlar kelimeleri elde edildi")
            print("------------------------------------")
        except:
            print(str(offset+i) +".ci makalenin yazar tarafından verilen etiketleri yok ---------!!!")
            print("------------------------------------")
        
        
        #Bulgular dictionary'nin uygun alanlarına yerleştirilir
        
        articles["article" + str(offset+i)] = {}
        articles["article" + str(offset+i)]["docTitle"] = docTitle
        articles["article" + str(offset+i)]["docLink"] = docLink
        articles["article" + str(offset+i)]["citations"] = citations.strip("\n")
        articles["article" + str(offset+i)]["keywords"] = keywords
    offset+= 20
print("Bütün bulgular dictionary'e yerleştirildi")


    
print("JSON Yazım işlemleri başlıyor")
with open("scopus500articles2019.json", "w", encoding="utf-8") as jsonFile:
    #json.dump(complaints, jsonFile, ensure_ascii=False).encode("utf8")
    json.dump(articles, jsonFile)
    print("Dosya yazım işlemi başarıyla tamamlandı")
