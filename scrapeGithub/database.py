import sqlite3
import pdb

def connectToDatabase(database):
    #Connect to database, create a table if it doesnot exist
    conn = sqlite3.connect(database, timeout=10)
    createTable = """
    CREATE TABLE IF NOT EXISTS "urls_to_be_scraped" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"url"	TEXT NOT NULL UNIQUE,
	"isScraped"	INTEGER DEFAULT 0,
    "isValidReadme" INTEGER DEFAULT 1,
    "readme" TEXT
    );
    """
    conn.execute(createTable)
    return conn

def parseRecord(s, isScraped):
    return f'("{s}", {isScraped})'

def getUrlFromOutput(s):
    return s[0]

def getAllUrlsToBeScraped(connection):
    #Get all github repo urls from database
    command = "SELECT url FROM urls_to_be_scraped WHERE isScraped==0 AND isValidReadme==1"
    urls = list(map(getUrlFromOutput,connection.execute(command).fetchall()))
    return urls

def addUrlsToBeScraped(connection,urls):
    #Add urls which needs to be scraped to database if not already present
    """urls is a list"""
    urlsToBeAdded = []
    if urls == []:
        return
    for u in urls:
        urlCheck = connection.execute(f'SELECT url FROM urls_to_be_scraped WHERE url=="{u}"').fetchall()
        if urlCheck == []:
            urlsToBeAdded.append(u)
    if len(urlsToBeAdded) > 0:
        records = ",".join(list(map(parseRecord,urlsToBeAdded, [False]*len(urlsToBeAdded))))
        insertCommand = f"INSERT INTO urls_to_be_scraped (url, isScraped) VALUES {records}"
        connection.execute(insertCommand)


def markUrlAsScraped(connection,url,readmeText):
    #Mark url as scraped so scraped doesnot visit this link again when its scraping
    """url is a string"""
    updateCommand = f'UPDATE urls_to_be_scraped SET isScraped=1,readme="{readmeText}" WHERE url=="{url}"'
    connection.execute(updateCommand)

def markUrlAsInvalid(connection,url):
    #Mark a github repo as invalid if readme is empty
    """url is a string"""
    updateCommand = f'UPDATE urls_to_be_scraped SET isValidReadme=0 WHERE url=="{url}"'
    connection.execute(updateCommand)



