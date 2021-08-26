from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped
import sys

#python insertUrls.py githubUrls.txt

if len(sys.argv) > 2:
    print("Recieved more than 1 argument, required 1. Correct usage is python insertUrls.py <filename.txt>")
    exit()
urlsToBeAdded = open(sys.argv[1]).read().split()[1250:1285]

conn = connectToDatabase("../db.sqlite3")
addUrlsToBeScraped(conn, urlsToBeAdded)
urls = conn.execute("SELECT * FROM urls_to_be_scraped").fetchall()
conn.commit()
conn.close()
print(urls)

