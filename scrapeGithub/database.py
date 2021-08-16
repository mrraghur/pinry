import sqlite3
import pdb
def connect():
    return sqlite3.connect('./db.sqlite3', timeout=10)

def createTable(connection):
    with connection:
        connection.execute("""CREATE TABLE "urls_to_be_scraped" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"url"	TEXT NOT NULL UNIQUE,
	"isScraped"	BOOLEAN NOT NULL DEFAULT 0);""")

def parseRecord(s, isScraped):
    return f'("{s}", {isScraped})'

def insertRecords(connection,records):
    records = ",".join(list(map(parseRecord,records, [False]*len(records))))
    insertCommand = f"INSERT INTO urls_to_be_scraped (url, isScraped) VALUES {records}"
    # print(insertCommand)
    connection.execute(insertCommand)

def getRecords(connection):
    getCommand = f"SELECT * from urls_to_be_scraped"
    return connection.execute(getCommand)

def DeleteTable(connection):
    with connection:
        connection.execute("DROP TABLE urls_to_be_scraped")

def getAllUrlsToBeScraped(connection):
    command = "SELECT url FROM urls_to_be_scraped WHERE isScraped==0"
    return connection.execute(command).fetchall()

def addUrlsToBeScraped(connection,urls):
    """urls is a list"""
    urlsToBeAdded = []
    for u in urls:
        urlCheck = connection.execute(f'SELECT url FROM urls_to_be_scraped WHERE url=="{u}"').fetchall()
        if urlCheck == []:
            connection.execute("")
            urlsToBeAdded.append(u)

    records = ",".join(list(map(parseRecord,urlsToBeAdded, [False]*len(urlsToBeAdded))))
    insertCommand = f"INSERT INTO urls_to_be_scraped (url, isScraped) VALUES {records}"
    connection.execute(insertCommand)

def updateUrlAsScraped(connection,url):
    """url is a string"""
    updateCommand = f'UPDATE urls_to_be_scraped SET isScraped=1 WHERE url=="{url}"'
    connection.execute(updateCommand)




con = connect()

# DeleteTable(con)

# createTable(con)


# githubUrls = open('scrapeGithub/githubUrls.txt').read().split()[:20]
# print(githubUrls[:20])

# insertRecords(con,githubUrls[:10])
records = getRecords(con)
print(records.fetchall())

urls_to_be_scraped = list(map(lambda x:x[0],getAllUrlsToBeScraped(con)))
print(urls_to_be_scraped)

urls = ['https://github.com/anooj-gandham/blogSearch','https://github.com/anooj-gandham/wappalyzer_1','https://github.com/0x09AL','https://github.com']
addUrlsToBeScraped(con,urls)

records = getRecords(con)
print(records.fetchall())


con.commit()
con.close()