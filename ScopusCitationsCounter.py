import json

file = "scopus500articles201"
fileNumber = 5

citations = {}
for i in range(5,10):
    targetFile = file + str(i) + ".json"
    with open(targetFile, "r") as articles:
        articleData = json.load(articles)
        for article, data in articleData.items():
            year = "201" + str(i)
            if year not in citations.keys():
                citations[year] = int(data["citations"].strip("\n").strip("\t"))
            else:
                citations[year] += int(data["citations"].strip("\n").strip("\t"))
                

with open("ArticleCitationCountByYear.json", "w") as destination:
    citations = {k: v for k, v in sorted(citations.items(), key=lambda item: item[1], reverse=True)}
    json.dump(citations, destination)
    print("Dosya yazım işlemi başarıyla tamamlandı")
