from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped
import sys
import random

#python insertUrls.py githubUrls.txt
if len(sys.argv) > 2:
    print("Recieved more than 1 argument, required 1. Correct usage is python insertUrls.py <filename.txt>")
    exit()
urls = open(sys.argv[1]).read().split()
#If all urls need to be inserted into db use this, 
nUrls = len(urls)
#else change nUrls appropriately and use
# nUrls = 100
urlsToBeAdded = random.sample(urls,nUrls)

conn = connectToDatabase("../db.sqlite3")
addUrlsToBeScraped(conn, urlsToBeAdded)
urlsAdded = conn.execute("SELECT * FROM urls_to_be_scraped").fetchall()
conn.commit()
conn.close()
print(urlsAdded)