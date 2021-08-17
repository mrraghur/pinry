import sqlite3
import pdb

def connectToDatabase(database):
    return sqlite3.connect(database, timeout=10)

def parseRecord(s, isScraped):
    return f'("{s}", {isScraped})'

def getUrlFromOutput(s):
    return s[0]

def getAllUrlsToBeScraped(connection):
    command = "SELECT url FROM urls_to_be_scraped WHERE isScraped==0"
    urls = list(map(getUrlFromOutput,connection.execute(command).fetchall()))
    return urls

def addUrlsToBeScraped(connection,urls):
    """urls is a list"""
    urlsToBeAdded = []
    if urls == []:
        return
    for u in urls:
        urlCheck = connection.execute(f'SELECT url FROM urls_to_be_scraped WHERE url=="{u}"').fetchall()
        if urlCheck == []:
            urlsToBeAdded.append(u)

    records = ",".join(list(map(parseRecord,urlsToBeAdded, [False]*len(urlsToBeAdded))))
    insertCommand = f"INSERT INTO urls_to_be_scraped (url, isScraped) VALUES {records}"
    connection.execute(insertCommand)

def updateUrlAsScraped(connection,url):
    """url is a string"""
    updateCommand = f'UPDATE urls_to_be_scraped SET isScraped=1 WHERE url=="{url}"'
    connection.execute(updateCommand)




con = connectToDatabase('../db.sqlite3')
updateUrlAsScraped(con,"https://github.com/0xAX/erlang-bookmarks")

# DeleteTable(con)

# createTable(con)


# githubUrls = open('scrapeGithub/githubUrls.txt').read().split()[:20]
# print(githubUrls[:20])

# insertRecords(con,githubUrls[:10])
# records = getRecords(con)
# print(records.fetchall())

# urls_to_be_scraped = list(map(lambda x:x[0],getAllUrlsToBeScraped(con)))
# print(urls_to_be_scraped)

# urls = ['https://github.com/anooj-gandham/blogSearch','https://github.com/anooj-gandham/wappalyzer_1','https://github.com/0x09AL','https://github.com']
# addUrlsToBeScraped(con,urls)

# records = getRecords(con)
# print(records.fetchall())
pdb.set_trace()

con.commit()
con.close()