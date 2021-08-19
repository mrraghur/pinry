from database import connectToDatabase, getAllUrlsToBeScraped, addUrlsToBeScraped, markUrlAsScraped
import sys


if len(sys.argv) > 2:
    print("Recieved more than 1 argument, required 1. Correct usage is python insertUrls.py <filename.txt>")
    exit()
urlsToBeAdded = open(sys.argv[1]).read().split()

conn = connectToDatabase("../db.sqlite3")
addUrlsToBeScraped(conn, urlsToBeAdded)
conn.commit()
conn.close()
