import json

file = "scopus500articles201"
fileNumber = 5

keywords = {}
for i in range(5,10):
    targetFile = file + str(i) + ".json"
    with open(targetFile, "r") as articles:
        articleData = json.load(articles)
        for article, data in articleData.items():
            for keyword in data["keywords"]:
                if len(data["keywords"]) < 1:
                       keywords["noKeywords"] += 1
                if keyword not in keywords:
                    keywords[keyword] = 1
                else:
                    keywords[keyword] += 1

    destinationFile = "500ArticleKeywords201" + str(i) + ".json"
    with open(destinationFile, "w") as destination:
        keywords = {k: v for k, v in sorted(keywords.items(), key=lambda item: item[1], reverse=True)}
        json.dump(keywords, destination)
        print("Dosya yazım işlemi başarıyla tamamlandı")
        
print("Bütün dosya yazım işlemleri başarıyla tamamlandı")
    
