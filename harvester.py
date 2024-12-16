from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from time import sleep


driver = Chrome()

driver.get("https://tore.tuhh.de/search?configuration=tuhh_publication")
sleep(10)
soup = BeautifulSoup(driver.page_source, "lxml")

articles = soup.find_all('a', class_="lead item-list-title dont-break-out ng-star-inserted notruncatable")

papers = []
for article in articles:
    driver.get("https://tore.tuhh.de" + article.get('href'))

    out = {
        'title': article.text
    }
    sleep(5)
    article_soup = BeautifulSoup(driver.page_source, "lxml")
    #print(driver.page_source)
    data = article_soup.find_all('div', class_="d-flex flex-column w-100 col metadata-cell ng-star-inserted")
    for line in data:
        print(line.text)
        if line.text.find("Publikationstyp") != -1:
            out["publication_type"] = line.text.split(" ")[1]

        if line.text.find("Date Issued") != -1:
            year, month, day = line.text.replace("Date Issued", "").split("-")

            out["date"] = "{}/{}/{}".format(month, day, year)

        if line.text.find("Sprache") != -1:
            out["lang"] = line.text.split(" ")[1]

        if line.text.find("Author(s)") != -1:
            names_and_aff = line.text.replace("Author(s)", "").split("   ")
            autaff = []
            for i in range(0,len(names_and_aff)-2):
                if i == 0:
                    autaff.append([names_and_aff[i], names_and_aff[i+1]])
                else:
                    autaff.append([names_and_aff[i + 1], names_and_aff[i]])

            out['autaff'] = autaff

        if line.text.find("TORE-DOI") != -1:
            out["doi"] = line.text.replace("TORE-DOI", "")

        if line.text.find("TORE-URI") != -1:
            out["hdl"] = line.text.replace("TORE-URI", "TORE-URIhttps://hdl.handle.net")

        if line.text.find("Journal") != -1:
            out["journal"] = line.text.split(" ")[1]



    sleep(10)

sleep(10)