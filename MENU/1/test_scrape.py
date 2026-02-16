from scraper import scrape_kapook
 
url = "https://cooking.kapook.com/view273026.html"
 
data = scrape_kapook(url)
 
print("ชื่อสูตร:", data["name"])
print("วัตถุดิบ:")
for ing in data["ingredients"]:
    print("-", ing)